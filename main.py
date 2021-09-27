#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config
import utility
import socket
import time
import re
import threading
import giveaway
import guess
import sys
from user_functions import UserClass

point_timer = 0
CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

try:
    s = [socket.socket(), socket.socket()]
    s[0].connect((config.HOST, config.PORT))
    s[0].send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
    s[0].send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
    s[0].send("USER {} 8 * :{}\r\n".format(config.NICK, config.NICK).encode("utf-8"))

    s[0].send("CAP REQ :twitch.tv/membership\r\n".encode("utf-8"))
    s[0].send("CAP REQ :twitch.tv/commands\r\n".encode("utf-8"))
    s[0].send("CAP REQ :twitch.tv/tags\r\n".encode("utf-8"))
    s[0].send("JOIN {}\r\n".format(config.CHAN).encode("utf-8"))
    # Set timeout for socket
    s[0].settimeout(0)
    # Socket successfully connected
    connected = True
    print("Bot connected")
    utility.chat(s[0], "Do not fear, as I is here!")
except Exception as e:
    print(str(e))
    # Socket failed to connect
    connected = False


def bot_loop():  # TODO: Change to a queueing system so spamm gets proccessed more quickly -> Sending will be restricted to MODRATE or RATE
    while connected:
        try:
            # TODO: Add timer commands (messages that get executed on a set interval)
            # TODO: Giveaway system
            response = s[0].recv(1024).rstrip().decode("utf-8")
            if response == "PING :tmi.twitch.tv":
                print(response + "\r\n")
                print("this response?")
                s[0].send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
                print("Pong")
            else:
                try:
                    tags = ""
                    if response.startswith("@"):
                        tags, response = response.split(" ", 1)

                    username = re.search(r"\w+", response).group(0)
                    message = CHAT_MSG.sub("", response)
                    print("TAGS:" + tags + "\n" + username + ": " + message + "\r\n")
                    if message.startswith("!", 0, 1):
                        print("message starts with !")
                        user = UserClass(tags, username)
                        utility.func_command(s[0], user, message)
                        del user
                    if giveaway.giveawayRunning and giveaway.isDrawn:
                        giveaway.look_for_name(username)
                    if guess.isDrawn:
                        guess.look_for_name(username)
                except Exception as ef:
                    print("An Exception has happened when trying to get user message")
                    print(ef)
        # If no message is sent, this exception occurs (recV.response.decode...)
        except Exception:
            global point_timer
            try:
                utility.check_timers(s[0])  # Checks if any timers need execution
                utility.chatEnQ()  # If there is any message in the queue is dequeued it and sends it.
                if time.time() - point_timer >= config.TIMERFORPOINTS:  # Start a thread to get requests
                    t1 = threading.Thread(target=utility.try_giving_points)
                    t1.start()
                    point_timer = time.time()
                if giveaway.giveawayRunning:
                    giveaway.run_timer(s[0])
                if guess.guessRunning:
                    guess.timer(s[0])
                if guess.isDrawn:
                    guess.claimTimer(s[0])
            except Exception as exc:
                print("An Error appeared in main.bot_loop.Exception timer,chatEnQ,threading,giveaway.run_timer didn't "
                      "work correctly\n")
                print(exc)
            except KeyboardInterrupt:
                # Make this a function to get called, so it can be called from the website as well (or restart or smth)
                print("^C was pressed. Do some cleanup code in here!")
                utility.chat(s[0], "I am now leaving the chat o7, till next time.")
                utility.chatEnQ()
                sys.exit()
        except KeyboardInterrupt:
            # Make this a function to get called, so it can be called from the website as well (or restart or smth)
            print("^C was pressed. Do some cleanup code in here!")
            utility.chat(s[0], "I am now leaving the chat o7, till next time.")
            utility.chatEnQ()
            sys.exit()



if __name__ == "__main__":
    utility.createDBs()
    utility.get_access_token()
    bot_loop()
