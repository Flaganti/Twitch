# -*- coding: utf-8 -*-
import config
import command_functions as commands
import time

import sqlite3
import grequests

import json

import giveaway
lastsent = 0
queue = []

def chat(sock, msg):
	#Queues the message
	global queue
	queue.append([sock,msg])

# All command responses are send to a queue
def chatEnQ(): #UnQueues the message and sends it
	global lastsent
	global queue
	if (time.time()-lastsent > (1/config.MODRATE) and len(queue)>0):
		sockthis,msgthis = queue.pop(0)
		sockthis.send(("PRIVMSG {} :{}\r\n".format(config.CHAN, msgthis)))
		lastsent=time.time()

def ban(sock, user):
	"""
	Ban a user from the current channel.
	Keyword arguments:
	sock -- the socket over which to send the ban command
	user -- the user to be banned
	"""
	chat(sock, ".ban {}".format(user))

def timeout(sock, user, secs=300):
	"""
	Time out a user for a set period of time.
	Keyword arguments:
	sock -- the socket over which to send the timeout command
	user -- the user to be timed out
	secs -- the length of the timeout in seconds (default 600)
	"""
	chat(sock, "/timeout {} {}".format(user, secs))

def func_command(sock, username, message):
	if (commands.is_valid_command(message) or commands.is_valid_command(message.split(' ')[0])) and (commands.check_access_level(username,message.split(' ')[0]) or commands.check_access_level(username,message)):
		command = message
		if commands.check_returns_function(command.split(' ')[0]):
			if commands.check_has_correct_args(command, command.split(' ')[0]): #TODO: CHANGE this or ANND QUERRY FLAG TO FUNCTION
				args = command.split(' ')
				del args[0]
				command = command.split(' ')[0]

				if commands.is_on_cooldown(command):
					print('Command is on cooldown. (%s) (%s) (%ss remaining)' % (command, username, commands.get_cooldown_remaining(command)))

				else:
					print('Command is valid an not on cooldown. (%s) (%s)' % (command, username))
					result = commands.pass_to_function(command, args)
					commands.update_last_used(command)

					if result:
						resp = '@%s > %s' % (username, result)
						print(resp)
						chat(sock, command_formatter_message(result,username))
			else:
				chat(sock, command_formatter_message(commands.pass_to_function(command.split(' ')[0], ('','')),username))#Print out command usage!
		elif commands.check_returns_giveaway(command.split(' ')[0]) or commands.check_returns_enter(command.split(' ')[0]):
			userLevel = commands.get_user_level(username)
			args = command.split(' ')
			if(len(args) == 1 and commands.check_returns_giveaway(command.split(' ')[0])):
				if(giveaway.giveawayRunning):
					chat(sock,giveaway.message)
				else:
					chat(sock,"/me There is currently now giveaway running.")

			elif(len(args) > 1 and userLevel >= 3 and commands.check_returns_giveaway(command.split(' ')[0])):
				giveaway.giveaway(sock,args,username)

			elif(commands.check_returns_enter(command.split(' ')[0])):
				if(giveaway.giveawayRunning):
					giveaway.enter(username,args)
				else:
					timeout(sock,username,5)

		else:
			if commands.is_on_cooldown(command.split(' ')[0]):
				print('Command is on cooldown. (%s) (%s) (%ss remaining)' % (command, username, commands.get_cooldown_remaining(command)))
			elif(commands.check_has_args(command.split(' ')[0])):#TODO: Make this a seperate function
				args = command.split(' ')
				del args[0]
				command = command.split(' ')[0]
				#print('empty')
				chat(sock,command_formatter(username,command,args))

			elif commands.check_has_return(command):
				print('Command is valid an not on cooldown. (%s) (%s)' % (command, username))

				resp = '@%s > %s' % (username, commands.get_return(command))
				commands.update_last_used(command)

				print(resp)
				chat(sock,command_formatter(username,command,[]))

#Region Point System
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

		give_points(viewers)
	except Exception as e:
		print("Error in utility.try_giving_points")
		print(e)

def give_points(viewers):
	try:
		conn = sqlite3.connect('pointsDB.db')
		cursor = conn.cursor()
		for viewer in viewers:
			print(viewer)
			argc={'viewer':viewer,'points':config.POINTAMOUNT}
			cursor.execute("SELECT EXISTS(SELECT Viewer from Points WHERE Viewer = '{viewer}')".format(**argc))
			fetch, = cursor.fetchone() #Checks if the viewer is already in the database
			if(fetch is 0):
				#print("inserts!")
				cursor.execute("INSERT INTO Points(Viewer, Points) VALUES('{viewer}', {points})".format(**argc))#inserts the viewer to the database
			else:
				#print("updates!")
				cursor.execute("UPDATE Points SET Viewer = '{viewer}', Points = Points + {points} WHERE Viewer = '{viewer}'".format(**argc)) #updates points of the viewer
		conn.commit()
		cursor.close()
		conn.close()
	except Exception as e:
		print("In utility.give_points -> Database Error: ")
		print(e)

def get_user_points(user):
	points =0
	if(len(user)>0):
		try:
			print("User: " + user)
			conn = sqlite3.connect('pointsDB.db')
			cursor = conn.cursor()
			cursor.execute("SELECT Points from Points WHERE Viewer = '{}'".format(user))
			points, = cursor.fetchone() #Checks if the viewer is already in the database
			print(points)
			conn.commit()
			cursor.close()
			conn.close()
		except Exception as e:
			print("in utility.get_user_points -> Database Error: ")
			print(e)
		return points
	return points

#Formating

def command_formatter_message_without_points(message,username=''): #Used for message formating( Manual strings)
	points=0
	argc={'user':username,'points':points}
	return str(message.format(**argc))

def command_formatter_message(message,username=''): #Used for message formating( Manual strings)
	points = get_user_points(username)
	argc={'user':username,'points':points}
	return str(message.format(**argc))

def command_formatter(username,command,args): # formats the string of a given command (formats the string that the command returns)
	points = get_user_points(username)
	argc={}
	if(len(args)<1):
		argc={'user':username,'target':username,'points':points} #creats dict
	else:
		argc={'user':username,'target':args[0],'points':points}

	return str(commands.get_return(command)).format(**argc) #replaces values with dict values



def check_timers(sock): #Checks for timers
	command = commands.return_commands()
	for key in command:
		if(commands.check_is_timed(key)):
			#print(commands.get_last_used(key))
			if(commands.get_last_used(key) >= commands.get_timer_repeat(key)):
				if(commands.get_return(key)=='command'): #if the timer is a seperate command -> execute this
					result = commands.pass_to_function(key,[])
					chat(sock, command_formatter_message(result)) #formats result from command
				else:
					result = command_formatter('',key,[]) #formats result from timer
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
