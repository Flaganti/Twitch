import utility
import random
import time
import config
from user_functions import *

guessRunning = False
canEnter = False

guessStarted = 0
guessBlue = {}
guessRed = {}
guessEntries = []

def timer(sock):
    global guessBlue,guessRed,guessEntries,canEnter,guessRunning,guessStarted
    if(time.time() - guessStarted >= 120 and canEnter==True):
        canEnter=False
        utility.chat(sock,"/me Guessing has stopped. You cannot enter anymore.")

def guessStartEnd(sock,args,user):
    global guessBlue,guessRed,guessEntries,canEnter,guessRunning,guessStarted
    del args[0]
    case = args[0]
    if(case == "start"):
        guessRunning = True
        canEnter = True

        guessStarted = time.time()
        guessBlue = {}
        guessRed = {}
        guessEntries = []
        utility.chat(sock,"/me Guessing has started. Type !guess <teamcolor> <numbers of kills> with out the <> to enter.")
    if(case == "end" and guessRunning == True):
        del args[0]
        if(len(args)!=4):
            utility.chat(sock,"/me @"+user.userName+" you didn't end guessing correctly.")
            return
        blue = str(args[0])
        bluenum = int(args[1])
        red =str(args[2])
        rednum = int(args[3])
        tempnum=0
        winners=[]
        if(blue.lower() != "blue"):
            tempnum = bluenum
            bluenum = rednum
            rednum = tempnum

        for winner,number in guessBlue.iteritems():
            print("blue")
            print(winner)
            print(number)
            if(number == bluenum):
                winners.append(winner)
        for winner,number in guessRed.iteritems():
            print("red")
            print(winner)
            print(number)
            if(number == rednum):
                winners.append(winner)

        print "\nPoints are being given:"
        utility.give_points_all_points(winners,20)
        string=""
        for winner in winners:
            string+=winner+","
        utility.chat(sock,"/me Guessed correctly have: "+string[:len(string)-1]+". Congratulations to all.")

        guessRunning = False
        canEnter = False

        guessStarted = 0

        guessBlue = {}
        guessRed = {}
        guessEntries = []
    if(case == "usage"):
        utility.chat(sock,utility.command_formatter_message_without_points("@{user} -> !guessing start or !guessing end blue <number> red <number>",user.userName))


def guess(sock,user,args):
    global guessBlue,guessRed,guessEntries,canEnter,guessRunning,guessStarted
    del args[0]
    user = user.userName
    if(len(args) != 2):
        utility.chat(sock,"Wrongly entered. TEST")
        return
    if(user in guessEntries):
        return
    team=""
    number=0
    try:
        team = str(args[0])
        number = int(args[1])
    except Exception as e:
        print "In Guess: "
        print e
    if(team.lower() == "blue"):
        guessBlue[user]=number
        guessEntries.append(user)
    elif(team.lower()=="red"):
        guessRed[user]=number
        guessEntries.append(user)