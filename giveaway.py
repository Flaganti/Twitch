# -*- coding: utf-8 -*-
import utility
import random
import time

giveawayRunning = False
isDrawn = False
hasClaimed = False

pointCost = 0
maxEntries = 1 # 0 is unlimited

message = "/me There is a current giveaway running for: "
winner = ""

giveawayQueue = []
giveEntries = {}
enteredQueue = []
duration = -1 #How long the giveaway will last | 0 is until winner is drawn
last_sent_timer = 0 # when to send another message to chat. Giveaway item, time left, chance of winning (number of entries)
claimTimer = 60
giveawayStarted = 0
was_drawn = 0
access_level = 1
timeLeft = -1

usage = "/me {user} -> !giveaway [start|stop|usage|draw] [Whats being give away]|[Duration is minutes]|[Access Level]|[Max Entries]|[Point Cost]"

def run_timer(socket):
    global last_sent_timer,winner,isDrawn,hasClaimed,was_drawn,giveawayRunning,timeLeft,stopTimer
    if(time.time() - last_sent_timer >= 60):
        last_sent_timer=time.time()
        if(timeLeft == -1):
            utility.chat(socket,message)
        elif(timeLeft != 0):
            utility.chat(socket,message+". Type !enter to join. Giveaway ends in %s minutes. Current entries %s." % (timeLeft,len(giveawayQueue)))
            timeLeft-=1
    if(isDrawn==False and (time.time() - giveawayStarted >= duration)):
        if(len(giveawayQueue) >0):
            winner = random.choice(giveawayQueue)
            was_drawn=time.time()
            isDrawn = True

            utility.chat(socket,utility.command_formatter_message_without_points("/me @{user} you have won. Speak up in the next 60 seconds or be rerolled",winner))
        else:
            utility.chat(socket,"/me No one entered the giveaway.")
            giveawayRunning=False

    if(hasClaimed==False and time.time()-was_drawn >= claimTimer and was_drawn != 0):
        utility.chat(socket,"/me Rerolling")
        isDrawn=False
    if(hasClaimed):
        winChance = (giveEntries[winner]*1.0 / len(giveawayQueue)*1.0)*100.0
        utility.chat(socket,utility.command_formatter_message_without_points("/me {user} has successfully claimed the prize. Win chance was %.2f%%." % (winChance) ,winner))
        giveawayRunning = False
        isDrawn = False
        hasClaimed = False


def giveaway(sock,args,user):
    global giveawayRunning,winner, isDrawn,hasClaimed,pointCost,maxEntries,message,duration,giveawayStarted,access_level,timeLeft
    del args[0]
    whatdo = args[0]
    if (whatdo == "start"): #Start Giveaway
        del args[0]
        str = " ".join(args)
        arg = str.split("|")

        giveawayRunning = True
        giveawayStarted = time.time()

        message+= arg[0]
        duration = 0
        access_level = 0
        maxEntries = 1
        pointCost = 0
        timeLeft = -1
        if(len(arg) > 0):
            try:
                duration = int(arg[1])*60
                access_level = arg[2]
                maxEntries = arg[3]
                pointCost = arg[4]
                timeLeft = duration/60
            except:
                utility.chat(sock,utility.command_formatter_message_without_points(usage,user))


    elif (whatdo == "stop"): #Ends giveaway or without claiming
        if(giveawayRunning):
            utility.chat(sock,"/me Giveaway has ended. No winners choosen.")
        giveawayRunning = False
        isDrawn=False
        hasClaimed=False

    elif (whatdo == "usage"): #Sends command usage
        utility.chat(sock,utility.command_formatter_message_without_points(usage,user))

    elif (whatdo == "draw"): #TODO: update this :)
        if(giveawayRunning):
            winner = random.choice(giveawayQueue)
            isDrawn = True
        else:
            utility.chat(sock,"/me Cannot draw giveaway winner if giveaway isn't running.")

#TODO: Add POINTS INTO THE MIX
#TODO: If points are 0, don't check for them!
def enter(sock,user,level,args):
    del args[0]
    points = utility.get_user_points(user)
    if(level < access_level):
        #utility.chat(sock,utility.command_formatter_message_without_points("Sorry {user} your rank is too low to enter the giveaway.",user))
        return
    if((user in giveEntries.keys()) == False):
        if(len(args) == 0):
            giveEntries[user] = 1
            giveawayQueue.append(user)
            enteredQueue.append(user)
        elif(len(args) > 0):
            try:
                num = int(args[0])
            except:
                num = 1
            if(num > maxEntries):
                num=maxEntries
            giveEntries[user] = num
            enteredQueue.append(user)
            for x in range (0, num):
                giveawayQueue.append(user)

def look_for_name(username):
    global hasClaimed
    if winner == username:
        hasClaimed=True