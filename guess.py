import utility
import random
import time

guessRunning = False
canEnter = False
canCheck = False
isDrawn = False
is_drawn = False
hasClaimed = False

guessingGiveaway = False

guessStarted = 0

guessBlue = {}
guessRed = {}

guessRedG = {}
guessBlueG = {}

guessingEntries = []
winnersG = []

message = ""
timeLeft = -1
last_sent_timer = 0

was_drawn = 0
winnerG = ""

ClaimTimer = 60
guessTime = 120


def timer(sock):
    global guessBlue, guessRed, canEnter, guessRunning, guessStarted, timeLeft, last_sent_timer
    if time.time() - guessStarted >= guessTime and canEnter is True:
        canEnter = False
        utility.chat(sock, "/me Guessing has stopped. You cannot enter anymore.")
    if time.time() - last_sent_timer >= 60 and guessingGiveaway is True and canEnter is True:
        last_sent_timer = time.time()
        if timeLeft == -1:
            utility.chat(sock, message)
        elif timeLeft != 0:
            utility.chat(sock, "/me Type !guess <teamcolor> <win/loose> for a chane to win.")
            timeLeft -= 1


def claimTimer(socket):
    global guessBlue, guessRed, canEnter, guessRunning, guessStarted, guessingGiveaway, message, timeLeft, guessBlueG, \
        guessRedG, winnersG, canCheck, isDrawn, was_drawn, hasClaimed, is_drawn, winnerG
    if hasClaimed is False and time.time() - was_drawn >= ClaimTimer and was_drawn != 0:
        utility.chat(socket, "/me Re-rolling")
        is_drawn = False

    if is_drawn is False:
        # print("(%s - %s >= %s)" % (time.time(),giveawayStarted,duration))
        if len(winnersG) > 0:
            winnerG = random.choice(winnersG)
            # if(remove winner from queue = true)
            winnersG = remove_values_from_list(winnersG, winnerG)
            was_drawn = time.time()
            is_drawn = True

            print("/me @" + winnerG + "you have won. Speak up in the next 60 seconds or be rerolled")
            utility.chat(socket, utility.command_formatter_message_without_points(
                "/me @{user} you have won. Speak up in the next 60 seconds or be rerolled", winnerG))
        else:
            utility.chat(socket, "/me No one entered the giveaway.")
            isDrawn = False
            winnersG = []

    if hasClaimed:
        utility.chat(socket,
                     utility.command_formatter_message_without_points("/me {user} has successfully claimed the prize.",
                                                                      winnerG))
        guessingGiveaway = False
        isDrawn = False
        hasClaimed = False
        canCheck = False
        was_drawn = 0
        winnersG = []


def guessStartEnd(sock, args, user):
    global guessBlue, guessRed, canEnter, guessRunning, guessStarted, guessingGiveaway, message, timeLeft, guessBlueG, \
        guessRedG, winnersG, canCheck, isDrawn, was_drawn, guessingEntries
    del args[0]
    if len(args) < 1:
        utility.chat(sock, utility.command_formatter_message_without_points(
            "@{user} -> !guessing start or !guessing end blue <number> red <number>", user.userName))
    case = args[0]
    if case == "start":
        if len(args) == 1:
            guessRunning = True
            canEnter = True

            guessStarted = time.time()
            guessBlue = {}
            guessRed = {}
            utility.chat(sock,
                         "/me Guessing has started. Type !guess <teamcolor> <# kills> or !guess <teamcolor1> <# "
                         "kills> <teamcolor2> <# kills> without <> to enter.")
        else:
            guessRunning = True
            guessingGiveaway = True
            canEnter = True
            canCheck = True

            guessStarted = time.time()
            guessBlueG = {}
            guessRedG = {}
            guessingEntries = []
            del args[0]

            message = " ".join(args)
            utility.chat(sock, "/me Guessing for: " + message + " has started!")
            utility.chat(sock, "/me Type !guess <teamcolor> <win/loose> for a chance to win.")
            timeLeft = guessTime / 60
    elif case == "end" and guessRunning is True and guessingGiveaway is True:
        del args[0]
        if len(args) != 4:
            utility.chat(sock, "/me @" + user.userName + " you didn't end guessing correctly.")
            return
        utility.chat(sock, "/me Winners have been entered into the raffle for a chance to win the giveaway.")
        blue = str(args[0])
        blueW = str(args[1])
        red = str(args[2])
        redW = str(args[3])

        if blue.lower() != "blue":
            tempW = blueW
            blueW = redW
            redW = tempW

        for winner, number in guessBlueG.items():
            print("blue")
            print(winner)
            print(number)
            if number == blueW:
                winnersG.append(winner)

        for winner, number in guessRedG.items():
            print("red")
            print(winner)
            print(number)
            if number == redW:
                winnersG.append(winner)

        print(winnersG)
        guessRunning = False
        guessingGiveaway = False
        canEnter = False

        guessStarted = 0
        guessingEntries = []
        guessBlue = {}
        guessRed = {}
        guessRedG = {}
        guessBlueG = {}
        timeLeft = -1
    elif case == "end" and guessRunning is True and guessingGiveaway is False:
        del args[0]
        if len(args) != 4:
            utility.chat(sock, "/me @" + user.userName + " you didn't end guessing correctly.")
            return
        try:
            blue = str(args[0])
            blueNum = int(args[1])
            red = str(args[2])
            redNum = int(args[3])
        except ():
            utility.chat(sock, "/me @" + user.userName + " you didn't end guessing correctly.")
            return
        tempNum = 0
        winners = []
        if blue.lower() != "blue":
            tempNum = blueNum
            blueMum = redNum
            redNum = tempNum

        for winner, number in guessBlue.items():
            print("blue")
            print(winner)
            print(number)
            if number == blueNum:
                winners.append(winner)
        for winner, number in guessRed.items():
            print("red")
            print(winner)
            print(number)
            if number == redNum:
                winners.append(winner)

        print("\nPoints are being given:")
        utility.give_points_all_points(winners, 20)
        string = ""
        for winner in winners:
            string += winner + ","
        utility.chat(sock, "/me Guessed correctly have: " + string[:len(string) - 1] + ". Congratulations to all.")

        guessRunning = False
        canEnter = False

        guessStarted = 0

        guessBlue = {}
        guessRed = {}
        guessRedG = {}
        guessBlueG = {}
        message = ""
        timeLeft = -1
    elif case == "draw":
        canCheck = False
        if len(winnersG) > 0:
            isDrawn = True
            was_drawn = time.time()
        else:
            print("Noone is eligable to win")
    elif case == "usage":
        utility.chat(sock, utility.command_formatter_message_without_points(
            "@{user} -> !guessing start or !guessing end blue <number> red <number>", user.userName))
    else:
        utility.chat(sock, utility.command_formatter_message_without_points(
            "@{user} -> !guessing start or !guessing end blue <number> red <number>", user.userName))


def guess(sock, user, args):
    global guessBlue, guessRed, canEnter, guessRunning, guessStarted, guessBlueG, guessRedG, guessingEntries, winnersG
    del args[0]
    print("is inside")
    user = user.userName
    arg = str(args[0])
    if arg.lower().startswith("ent", 0, 3) and (len(winnersG) > 0):
        print("stuff")
        if user in winnersG:
            utility.chat(sock, "/me @" + user + " -> You are eligable to win.")
    if canEnter is False:
        return
    if len(args) != 2 and len(args) != 4:
        # utility.chat(sock,"Wrongly entered. TEST")
        print("User: " + user + " wrongly used the command.")
        return
    team1 = ""
    number1 = 0
    team2 = ""
    number2 = 0
    win_loose = ""
    if len(args) == 4 and guessingGiveaway is False:
        print("has successfully entered normal guessing")
        try:
            team1 = str(args[0])
            number1 = int(args[1])
            team2 = str(args[2])
            number2 = int(args[3])
        except Exception as e:
            print("In Guess: ")
            print(e)
        if team1.lower() == "blue":
            guessBlue[user] = number1
            guessRed[user] = number2
        elif team1.lower() == "red":
            guessBlue[user] = number2
            guessRed[user] = number1

    elif len(args) == 2 and guessingGiveaway is False:
        print("has successfully entered normal guessing")
        try:
            team1 = str(args[0])
            number1 = int(args[1])
        except Exception as e:
            print("In Guess: ")
            print(e)
        if team1.lower() == "blue":
            guessBlue[user] = number1
        elif team1.lower() == "red":
            guessRed[user] = number1
    elif len(args) == 2 and guessingGiveaway is True:
        print("has successfully entered the guessing giveaway")
        try:
            team1 = str(args[0])
            win_loose = str(args[1])
        except Exception as e:
            print("In giveaway guessing")
            print(e)

        if team1.lower() == "blue" and (user in guessingEntries) is False:
            print("entered in blue")
            guessBlueG[user] = win_loose.lower()
            if win_loose.lower() == "win":
                guessRedG[user] = "loose"
            else:
                guessRedG[user] = "win"
            guessingEntries.append(user)
        elif team1.lower() == "red" and (user in guessingEntries) is False:
            print("entered in red")
            guessRedG[user] = win_loose.lower()
            if win_loose.lower() == "win":
                guessBlueG[user] = "loose"
            else:
                guessBlueG[user] = "win"
            guessingEntries.append(user)


def remove_values_from_list(the_list, val):
    return [value for value in the_list if value != val]


def look_for_name(username):
    global hasClaimed
    if winnerG == username:
        hasClaimed = True
