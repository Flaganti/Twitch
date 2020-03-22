HOST = "irc.twitch.tv"              # This is Twitchs IRC server
PORT = 6667                         # Twitchs IRC server listens on port 6667
NICK = ""            # Twitch username your using for your bot
PASS = "" # your Twitch OAuth token
CHAN = "#"                   # the channel you want the bot to join.
RATE = (20.0/30.0) # 20 messages in 30 seconds
MODRATE = (100.0/30.0) # 100 messages in 30 seconds
POINTAMOUNT = 1 #How many points you get
TIMERFORPOINTS = 20*60 #How often you get the points in seconds
VIEWERAPI = "https://tmi.twitch.tv/group/user/{}/chatters".format(CHAN[1:])
FOLLOW_REQ = False
BAN_PAT=[]
