# -*- coding: utf-8 -*-
#commands = {
#    '!test':{                          ->   command name
#        'limit': 0,                    ->   time limit in seconds
#        'argc': 0,                     ->   number of arguments needed -> only used for commands with return value of 'command'
#        'return': 'This is a test'     ->   return value, if 'command' -> execute command in commands
#        'access': [0,1,2,3,4]
#        'is_timed': 0,1                ->   0 no, 1 yes
#        'timer_repeat': 300            ->   time in seconds
#    }
# Access Levels:
#   0 -> Everyone
#   1 -> Subscriber
#   2 -> Moderator
#   3 -> Owner
#

#TODO: Make this a SQL database
#TODO: function reads from database of commands
#TODO: Makes it a dict, when new command is added run the command again
commands = {
    '!test':{
        'limit': 0,
        'return': '/me This is a test',
        'access': 0
    },
    '!limit':{
        'limit': 30,
        'argc': 2,
        'return': 'command',
        'access': 1
    },
    '!hug':{
        'limit':0,
        'argc':0,
        'return':"/me hugs {target} (> ˙^˙ <)",
        'access': 0
    },
    '!followage':{
        'limit':5,
        'argc':0,
        'return':'{follow}',
        'access':0
    },
    '!command':{
        'limit':30,
        'argc':2,
        'return':"command",
        'access': 2
    },
    '!tt':{
        'limit':0,
        'return':'/me This is a timer test',
        'access': 3,
        'is_timed': 0,
        'argc':0,
        'timer_repeat': 300
    },
    '!giveaway':{
        'limit':30,
        'return':'giveaway',
        'access': 0,
        'argc':0
    },
    '!enter':{
        'limit':0,
        'return':'enter',
        'access':0,
        'argc':0
    },
    '!guessing':{
        'limit':30,
        'return':'guessing',
        'access':0,
        'argc':1
    },
    "!guess":{
        'limit':0,
        'return':'guess',
        'access':0,
        'argc':2
    },
    '!points':{
        'limit':10,
        'return': '/me {user} has {points} Flags',
        'access': 0,
    }


}

for command in commands:
    commands[command]['last_used'] = 0