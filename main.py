#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config
import utility
import socket
import time
import re

CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

try:
    s = [socket.socket(),socket.socket()]
    s[0].connect((config.HOST, config.PORT))
    s[0].send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
    s[0].send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
    s[0].send("USER {} 8 * :{}\r\n".format(config.NICK,config.NICK).encode("utf-8"))

    s[0].send("CAP REQ :twitch.tv/membership\r\n".encode("utf-8"))
    s[0].send("CAP REQ :twitch.tv/commands\r\n".encode("utf-8"))
    #s[0].send("CAP REQ :twitch.tv/tags\r\n".encode("utf-8")) #Needs re changing! so it can read tags
    s[0].send("JOIN {}\r\n".format(config.CHAN).encode("utf-8"))
    s[0].settimeout(0) #Set timeout for socket
    connected = True #Socket successfully connected
except Exception as e:
    print(str(e))
    connected = False #Socket failed to connect


def bot_loop(): #TODO: Change to a queueing system so spamm gets proccessed more quickly -> Sending will be restricted to MODRATE or RATE
    while connected:
        try:
            #TODO: Add timer commands (messages that get executed on a set interval)
            #TODO: Giveaway system
            response = s[0].recv(1024).rstrip()
            if response == "PING :tmi.twitch.tv":
                print(response+"\r\n")
                s[0].send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
                print("Pong")
            else:
                try:
                    #print(response+"\r\n")
                    username = re.search(r"\w+", response).group(0)
                    message = CHAT_MSG.sub("", response)
                    print(username + ": " + message+"\r\n")
                    if message.startswith("!",0,1):
                        utility.func_command(s[0],username,message)
                except Exception as e:
                    print(e)
        except Exception as e:
            utility.check_timers(s[0]) # Checks if any timers need execution
            utility.chatEnQ()
            utility.try_giving_points()
            #print(e)
        #time.sleep(1 / config.MODRATE)# Not needed anymore as chatEnQ takes care of it

if __name__ == "__main__":
    utility.createDBs()
    bot_loop()