# -*- coding: utf-8 -*-
import datetime
import json
import sqlite3
import time

import grequests

import command_functions as commands
import config
import giveaway
import guess

lastsent = 0
queue = []


def chat(sock, msg):
    # Queues the message
    global queue
    queue.append([sock, msg])


# All command responses are send to a queue
def chatEnQ():  # UnQueues the message and sends it
    global lastsent
    global queue
    if time.time() - lastsent > (1.0 / config.MODRATE) and len(queue) > 0:
        sockthis, msgthis = queue.pop(0)
        sockthis.send(("PRIVMSG {} :{}\r\n".format(config.CHAN, msgthis)).encode("utf-8"))
        lastsent = time.time()
    # print(":sprout_bot!sprout_bot@sprout_bot.tmi.twitch.tv PRIVMSG {} :{}\r\n".format(config.CHAN, msgthis))


def ban(sock, user):
    # Ban a user from the current channel.
    # Keyword arguments:
    # sock -- the socket over which to send the ban command
    # user -- the user to be banned

    chat(sock, ".ban {}".format(user))


def timeout(sock, user, secs=300):
    # Time out a user for a set period of time.
    # Keyword arguments:
    # sock -- the socket over which to send the timeout command
    # user -- the user to be timed out
    # secs -- the length of the timeout in seconds (default 600)

    chat(sock, "/timeout {} {}".format(user, secs))


# TODO: guess
def func_command(sock, user, message):
    userLevel = user.get_user_level()
    username = user.userName
    if (commands.is_valid_command(message) or commands.is_valid_command(message.split(' ')[0])) and (
            commands.check_access_level(userLevel, message.split(' ')[0]) or commands.check_access_level(userLevel,
                                                                                                         message)):
        command = message
        if commands.check_returns_function(command.split(' ')[0]):
            if commands.check_has_correct_args(command, command.split(' ')[0]):
                # TODO: CHANGE this or AND QUERY FLAG TO FUNCTION
                args = command.split(' ')
                del args[0]
                command = command.split(' ')[0]

                if commands.is_on_cooldown(command):
                    print('Command is on cooldown. (%s) (%s) (%ss remaining)' % (
                        command, username, commands.get_cooldown_remaining(command)))

                else:
                    print('Command is valid an not on cooldown. (%s) (%s)' % (command, username))
                    result = commands.pass_to_function(command, args)
                    print("command resault was posted back")
                    commands.update_last_used(command)

                    if result:
                        resp = '@%s > %s' % (username, result)
                        print(resp)
                        chat(sock, command_formatter_message(result, username))
            else:
                chat(sock, command_formatter_message(commands.pass_to_function(command.split(' ')[0], ('', '')),
                                                     username))  # Print out command usage!

        elif commands.check_returns_giveaway(command.split(' ')[0]) or commands.check_returns_enter(
                command.split(' ')[0]):
            # GIVEAWAY COMMAND SECTION
            args = command.split(' ')
            if len(args) == 1 and commands.check_returns_giveaway(command.split(' ')[0]):
                if commands.is_on_cooldown(command.split(' ')[0]):
                    return
                if giveaway.giveawayRunning:
                    chat(sock, giveaway.message)
                    commands.update_last_used(command.split(' ')[0])
                else:
                    chat(sock, "/me No giveaway running at this moment.")
                    commands.update_last_used(command.split(' ')[0])
            elif len(args) > 1 and userLevel >= 2 and commands.check_returns_giveaway(command.split(' ')[0]):
                giveaway.giveaway(sock, args, username)
            elif commands.check_returns_enter(command.split(' ')[0]):

                if giveaway.giveawayRunning:
                    giveaway.enter(sock, user, args)
                else:
                    # timeout(sock,username,5)
                    return
        elif commands.check_returns_guessing(command.split(' ')[0]) or commands.check_returns_guess(
                command.split(' ')[0]):
            # GUESSING COMMAND SECTION
            args = command.split(' ')
            if len(args) > 1 and userLevel >= 2 and commands.check_returns_guessing(command.split(' ')[0]):
                guess.guessStartEnd(sock, args, user)
            elif commands.check_returns_guess(command.split(' ')[0]):
                if guess.canEnter or guess.canCheck:
                    guess.guess(sock, user, args)
                else:
                    return
        else:
            if commands.is_on_cooldown(command.split(' ')[0]):
                print('Command is on cooldown. (%s) (%s) (%ss remaining)' % (
                    command, username, commands.get_cooldown_remaining(command)))
            elif commands.check_has_args(command.split(' ')[0]):  # TODO: Make this a seperate function
                args = command.split(' ')
                del args[0]
                command = command.split(' ')[0]
                # print('empty')
                chat(sock, command_formatter(user, command, args))

            elif commands.check_has_return(command):
                print('Command is valid an not on cooldown. (%s) (%s)' % (command, username))

                resp = '@%s > %s' % (username, commands.get_return(command))
                commands.update_last_used(command)

                print(resp)
                chat(sock, command_formatter(user, command, []))


# Point System
def try_giving_points():
    try:
        req = grequests.get(config.VIEWERAPI)
        res = grequests.map([req])

        viewersDict = json.loads(res[0].content)
        viewers = viewersDict['chatters']['moderators']
        viewers.extend(viewersDict['chatters']['staff'])
        viewers.extend(viewersDict['chatters']['admins'])
        viewers.extend(viewersDict['chatters']['global_mods'])
        viewers.extend(viewersDict['chatters']['viewers'])

        give_points_all(viewers)
    except Exception as e:
        print("Error in utility.try_giving_points")
        print(e)


def take_points(viewer, howMuch):  # Takes a certian amout of points from a specific viewer
    try:
        conn = sqlite3.connect('pointsDB.db')
        cursor = conn.cursor()

        print(viewer)
        argc = {'viewer': viewer, 'points': howMuch}
        # cursor.execute("SELECT EXISTS(SELECT Viewer from Points WHERE Viewer = '{viewer}')".format(**argc))
        # fetch, = cursor.fetchone() #Checks if the viewer is already in the database
        # if(fetch is 0):
        #	#print("inserts!")
        #	cursor.execute("INSERT INTO Points(Viewer, Points) VALUES('{viewer}', {points})".format(**argc))#inserts the viewer to the database
        # else:
        #	#print("updates!")
        cursor.execute(
            "UPDATE Points SET Viewer = '{viewer}', Points = Points - {points} WHERE Viewer = '{viewer}'".format(
                **argc))  # updates points of the viewer

        conn.commit()
        cursor.close()
        conn.close()
        print("\n")
    except Exception as e:
        print("In utility.take_points -> Database Error: ")
        print(e)


def give_points_all(viewers):
    print("Points are being given:")
    # TODO: Subs get more points
    try:
        conn = sqlite3.connect('pointsDB.db')
        cursor = conn.cursor()
        for viewer in viewers:
            print(viewer)
            argc = {'viewer': viewer, 'points': config.POINTAMOUNT}
            cursor.execute("SELECT EXISTS(SELECT Viewer from Points WHERE Viewer = '{viewer}')".format(**argc))
            fetch, = cursor.fetchone()  # Checks if the viewer is already in the database
            if fetch == 0:
                # print("inserts!")
                cursor.execute("INSERT INTO Points(Viewer, Points) VALUES('{viewer}', {points})".format(
                    **argc))  # inserts the viewer to the database
            else:
                # print("updates!")
                cursor.execute(
                    "UPDATE Points SET Viewer = '{viewer}', Points = Points + {points} WHERE Viewer = '{viewer}'".format(
                        **argc))  # updates points of the viewer
        conn.commit()
        cursor.close()
        conn.close()
        print("\n")
    except Exception as e:
        print("In utility.give_points_all -> Database Error: ")
        print(e)


def give_points_all_points(viewers, points):
    # TODO: Subs get more points
    try:
        conn = sqlite3.connect('pointsDB.db')
        cursor = conn.cursor()
        for viewer in viewers:
            print(viewer)
            argc = {'viewer': viewer, 'points': points}
            cursor.execute("SELECT EXISTS(SELECT Viewer from Points WHERE Viewer = '{viewer}')".format(**argc))
            fetch, = cursor.fetchone()  # Checks if the viewer is already in the database
            if fetch == 0:
                # print("inserts!")
                cursor.execute("INSERT INTO Points(Viewer, Points) VALUES('{viewer}', {points})".format(
                    **argc))  # inserts the viewer to the database
            else:
                # print("updates!")
                cursor.execute(
                    "UPDATE Points SET Viewer = '{viewer}', Points = Points + {points} WHERE Viewer = '{viewer}'".format(
                        **argc))  # updates points of the viewer
        conn.commit()
        cursor.close()
        conn.close()
        print("\n")
    except Exception as e:
        print("In utility.give_points_all -> Database Error: ")
        print(e)


def get_user_points(user):
    points = 0
    if len(user) > 0:
        try:
            print("User: " + user)
            conn = sqlite3.connect('pointsDB.db')
            cursor = conn.cursor()
            cursor.execute("SELECT Points from Points WHERE Viewer = '{}'".format(user))
            # Checks if the viewer is already in the database
            points = cursor.fetchone()[0]
            print("Points: {} \n".format(points))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            print("in utility.get_user_points -> Database Error: ")
            print(e)
        return points
    return points


# Formating

def command_formatter_message_without_points(message, username):  # Used for message formating( Manual strings)
    points = 0
    argc = {'user': username, 'points': points}
    return str(message.format(**argc))


def command_formatter_message(message, username):  # Used for message formatting( Manual strings)
    points = get_user_points(username)
    argc = {'user': username, 'points': points}
    return str(message.format(**argc))


def command_formatter(user, command,
                      args):  # formats the string of a given command (formats the string that the command returns)
    try:
        username = user.userName
        followage = user.get_followage()
    except:
        username = ''
        followage = ''
    points = get_user_points(username)
    argc = {}
    if len(args) < 1:
        argc = {'user': username, 'target': username, 'points': points, 'follow': followage}  # creats dict
    else:
        argc = {'user': username, 'target': args[0], 'points': points, 'follow': followage}

    return str(commands.get_return(command)).format(**argc)  # replaces values with dict values


def check_timers(sock):  # Checks for timers
    command = commands.return_commands()
    for key in command:
        if commands.check_is_timed(key):
            # print(commands.get_last_used(key))
            if commands.get_last_used(key) >= commands.get_timer_repeat(key):
                if commands.get_return(key) == 'command':  # if the timer is a seperate command -> execute this
                    result = commands.pass_to_function(key, [])
                    chat(sock, command_formatter_message(result, ""))  # formats result from command
                else:
                    result = command_formatter('', key, [])  # formats result from timer
                    chat(sock, result)
                commands.update_last_used(key)


def createDBs():
    try:
        conn = sqlite3.connect('pointsDB.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE Points(Viewer TEXT, Points INT)''')
        cursor.close()
        conn.close()
    except Exception as e:
        print(e)


def get_access_token():
    try:
        if is_access_token_valid() is False:
            req = grequests.post("https://id.twitch.tv/oauth2/token?"
                                 "client_id=jktjplv8zqdnj0xbn3i8gag8y7tzg3&"
                                 "client_secret=%s&"
                                 "grant_type=client_credentials" % config.CLIENT_SECRET)
            res = grequests.map([req])
            config.APP_ACCESS_TOKEN = json.loads(res[0].content)["access_token"]
        else:
            print("Access_token is already valid")
    except Exception as e:
        print("Error getting access_token")
        print(e)


def is_access_token_valid():
    try:
        if config.APP_ACCESS_TOKEN != "":
            req = grequests.get("https://id.twitch.tv/oauth2/validate",
                                headers={'Authorization': 'Bearer %s' % config.APP_ACCESS_TOKEN})
            res = grequests.map([req])
            if res[0].status_code == 200:
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        print("Error validating access_token")
        print(e)
        return False


################################

def convert_enddate_to_seconds(ts):
    try:
        utc_dt = datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%SZ')
        # Convert UTC datetime to seconds since the Epoch
        timestamp = (utc_dt - datetime.datetime(1970, 1, 1)).total_seconds()
        # smth = (datetime.datetime.utcnow() - utc_dt).month
        # print(smth)
        return timestamp
    except():
        return time.time()
