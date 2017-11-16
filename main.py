#!/usr/bin/env python
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

    s[0].send("JOIN {}\r\n".format(config.CHAN).encode("utf-8"))
    connected = True #Socket succefully connected
except Exception as e:
    print(str(e))
    connected = False #Socket failed to connect

def bot_loop():
    while connected:
        response = s[0].recv(1024).rstrip()
        if response == "PING :tmi.twitch.tv":
            print(response+"\r\n")
            s[0].send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            print("Pong")
        else:
            print(response+"\r\n")
            username = re.search(r"\w+", response).group(0)
            message = CHAT_MSG.sub("", response)
            print(username + ": " + message+"\r\n")
            if message.startswith("!",0,1):
                utility.func_command(s[0],username,message)
            #for pattern in config.BAN_PAT:
            #    if re.match(pattern, message):
            #        utility.ban(s[0], username)
            #        break
        time.sleep(1 / config.MODRATE)

if __name__ == "__main__":
    bot_loop()