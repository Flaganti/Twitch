# -*- coding: utf-8 -*-
import grequests
import json
import datetime
import config
class UserClass:
    def __init__(self,tags,username):
        self.userName = username
        self.badges,self.color,self.dName,self.emotes,self.id,self.mod,self.roomId,self.sub,self.timestamp,self.turbo,self.userId,self.userType = tags[1:].split(";")
    def is_follower(self):
        try:
            user_id=self.userId.split('=')[1]
            channel_id=self.roomId.split('=')[1]
            req = grequests.get("https://api.twitch.tv/kraken/users/%s/follows/channels/%s"%(user_id,channel_id),headers = {'Client-ID':'jktjplv8zqdnj0xbn3i8gag8y7tzg3','Accept':'application/vnd.twitchtv.v5+json'})
            res = grequests.map([req])
            viewersDict = json.loads(res[0].content)
            return viewersDict["created_at"]
        except Exception as e:
            return False
    def get_user_level(self): #Get user level from tags -> Some tags are irrelevant
        userLevel = 0
        mod=self.mod.split("=")[1]
        sub=self.sub.split("=")[1]

        if(sub=="1"):
            userLevel=1
        if(mod=="1"):
            userLevel=2
        if("broadcaster" in self.badges):
            userLevel=3
        #print("UserLevel: {}".format(userLevel))
        return userLevel
    def get_followage(self):
        follow=self.is_follower()
        if(follow!=False):
            utc_dt = datetime.datetime.strptime(follow, '%Y-%m-%dT%H:%M:%SZ')
            diff = relativedelta(datetime.datetime.utcnow(),utc_dt)
            return "/me @%s has been following %s for %d Years %d Months %d Days %d Hours %d Minutes %d Seconds" % (self.userName,config.CHAN[1:],diff.years, diff.months, diff.days, diff.hours, diff.minutes,diff.seconds)
        else:
            return "/me @%s is not following the channel." % (self.userName)


