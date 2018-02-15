#!/usr/bin/env python
# -*- coding: utf-8 -*-
import config
import utility
import socket
import time
import re
import threading
import giveaway
import sys

point_timer = 0#time.time()
CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

try:
    s = [socket.socket(),socket.socket()]
    s[0].connect((config.HOST, config.PORT))
    s[0].send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
    s[0].send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
    s[0].send("USER {} 8 * :{}\r\n".format(config.NICK,config.NICK).encode("utf-8"))

    s[0].send("CAP REQ :twitch.tv/membership\r\n".encode("utf-8"))
    s[0].send("CAP REQ :twitch.tv/commands\r\n".encode("utf-8"))
    s[0].send("CAP REQ :twitch.tv/tags\r\n".encode("utf-8")) #Needs re changing! so it can read tags
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
                    badges, response = response.split(" ",1)
                    #print(response+"\r\n")
                    username = re.search(r"\w+", response).group(0)
                    message = CHAT_MSG.sub("", response)
                    print(username + ": " + message+"\r\n")
                    if message.startswith("!",0,1):
                        utility.func_command(s[0],username,message)
                    if giveaway.giveawayRunning and giveaway.isDrawn:
                        giveaway.look_for_name(username)
                except Exception as e:
                    print(e)
        except Exception as e:
                global point_timer
                try:
                    utility.check_timers(s[0]) # Checks if any timers need execution
                    utility.chatEnQ() #If there is any messsage in the queue is dequeses it and sends it.
                    if(time.time() - point_timer >= config.TIMERFORPOINTS): #Start a thread to get requests
                        t1 = threading.Thread(target=utility.try_giving_points)
                        t1.start()
                        point_timer = time.time()
                    if(giveaway.giveawayRunning):
                        giveaway.run_timer(s[0])
                except Exception as exc:
                    print "An Error appeared in main.bot_loop.Exception timer,chatEnQ,threading,giveaway.run_timer didn't work correctly\n"
                    print exc
                except KeyboardInterrupt:
                    #Make this a function to get called, so it can be called from the website as well (or restart or smth)
                    print("^C was pressed. Do some cleanup code in here!")
                    sys.exit()
        except KeyboardInterrupt:
            #Make this a function to get called, so it can be called from the website as well (or restart or smth)
            print("^C was pressed. Do some cleanup code in here!")
            sys.exit()
        #print(e)
        #time.sleep(1 / config.MODRATE)# Not needed anymore as chatEnQ takes care of it

if __name__ == "__main__":
    utility.createDBs()
    bot_loop()