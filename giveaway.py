# -*- coding: utf-8 -*-
import utility
import random
import time
import config
from user_functions import *


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
    global last_sent_timer,winner,isDrawn,hasClaimed,was_drawn,giveawayRunning,timeLeft,stopTimer,giveawayQueue,enteredQueue,giveEntries
    if(time.time() - last_sent_timer >= 60):
        last_sent_timer=time.time()
        if(timeLeft == -1):
            utility.chat(socket,message)
        elif(timeLeft != 0):
            utility.chat(socket,message+". Type !enter to join. Giveaway ends in %s minutes. Current entries %s." % (timeLeft,len(giveawayQueue)))
            timeLeft-=1

    if(hasClaimed==False and time.time()-was_drawn >= claimTimer and was_drawn != 0):
        utility.chat(socket,"/me Re-rolling")
        isDrawn=False

    if(isDrawn==False and (time.time() - giveawayStarted >= duration)):
        print("(%s - %s >= %s)" % (time.time(),giveawayStarted,duration))
        if(len(giveawayQueue) >0):
            winner = random.choice(giveawayQueue)
            #if(remove winner from queue = true)
            giveawayQueue = remove_values_from_list(giveawayQueue,winner)
            was_drawn=time.time()
            isDrawn = True

            utility.chat(socket,utility.command_formatter_message_without_points("/me @{user} you have won. Speak up in the next 60 seconds or be rerolled",winner))
        else:
            utility.chat(socket, "/me No one entered the giveaway.")
            giveawayRunning=False

    if(hasClaimed):
        winChance = 0
        if(len(giveawayQueue)<1):
            winChance = (giveEntries[winner]*1.0 / (len(giveawayQueue)+1)*1.0)*100.0
        else:
            winChance = (giveEntries[winner]*1.0 / (len(giveawayQueue))*1.0)*100.0
        utility.chat(socket,utility.command_formatter_message_without_points("/me {user} has successfully claimed the prize. Win chance was %.2f%%." % (winChance),winner))
        utility.take_points(winner,giveEntries[winner]*pointCost)
        giveawayRunning = False
        isDrawn = False
        hasClaimed = False
        was_drawn=0
        giveawayQueue = []
        giveEntries = {}
        enteredQueue = []


def giveaway(sock,args,user):
    global giveawayRunning,winner, isDrawn,hasClaimed,pointCost,maxEntries,message,duration,giveawayStarted,access_level,timeLeft,was_drawn,giveawayQueue,giveEntries,enteredQueue
    del args[0]
    doWhat = args[0]
    if (doWhat == "start"): #Start Giveaway
        del args[0]
        str = " ".join(args)
        arg = str.split("|")

        giveawayRunning = True
        giveawayStarted = time.time()

        was_drawn = 0
        enteredQueue = []
        giveEntries = {}
        giveawayQueue = []

        was_drawn=0
        message+= arg[0]
        duration = 0
        access_level = 0
        maxEntries = 1
        pointCost = 0
        timeLeft = -1
        if(len(arg) > 0):
            try:
                duration = int(arg[1])*60
                access_level = int(arg[2])
                maxEntries = int(arg[3])
                pointCost = int(arg[4])
                timeLeft = duration/60
            except:
                utility.chat(sock,utility.command_formatter_message_without_points(usage,user))


    elif (doWhat == "stop"): #Ends giveaway or without claiming
        if(giveawayRunning):
            utility.chat(sock,"/me Giveaway has ended. No winners choosen.")
        giveawayRunning = False
        isDrawn=False
        hasClaimed=False


    elif (doWhat == "usage"): #Sends command usage
        utility.chat(sock,utility.command_formatter_message_without_points(usage,user))

    elif (doWhat == "draw"): #TODO: update this :)
        if(giveawayRunning):
            winner = random.choice(giveawayQueue)
            isDrawn = True
        else:
            utility.chat(sock,"/me Cannot draw giveaway winner if giveaway isn't running.")

#TODO: Add POINTS INTO THE MIX
#TODO: If points are 0, don't check for them!
def enter(sock,user,args):
    del args[0]
    follow = user.is_follower()
    level = 0
    if(access_level == 0):
        level = user.get_user_level()
    user = user.userName
    numOfEntries = 1
    try:
        if(len(args) > 0):
            numOfEntries = int(args[0])
    except:
        numOfEntries = 1

    try:
        points = utility.get_user_points(user)
    except:
        points = 0

    if(config.FOLLOW_REQ == True):
        print("stopped here")
        if((follow==False or (time.time()-utility.convert_enddate_to_seconds(follow))<600)):
            return
    if(level < access_level): #this fucks up 0 < 0 == true ... what?
        print("access level %s %s" % (access_level,level))
        #utility.chat(sock,utility.command_formatter_message_without_points("Sorry {user} your rank is too low to enter the giveaway.",user))
        return
    if(numOfEntries > maxEntries):
        print("numentries")
        numOfEntries = maxEntries
    if((points < pointCost * numOfEntries) and pointCost != 0): #this fucks up
        print("points fcked up")
        #utility.chat(sock,utility.command_formatter_message_without_points("Sorry {user}, you don't have enough points to enter the giveaway.",user))
        return
    if((user in giveEntries.keys()) == False):
        print("user was entered to the giveaway.")
        if(len(args) == 0):
            giveEntries[user] = 1
            giveawayQueue.append(user)
            enteredQueue.append(user)
        elif(len(args) > 0):
            giveEntries[user] = numOfEntries
            enteredQueue.append(user)
            for x in range (0, numOfEntries):
                giveawayQueue.append(user)

def look_for_name(username):
    global hasClaimed
    if winner == username:
        hasClaimed=True

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]
