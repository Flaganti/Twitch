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
#   1 -> Regular
#   2 -> Subscriber
#   3 -> Moderator
#   4 -> Owner
#

#TODO: Commands can be added while the program is running. New file is saved seperatly -> When updating file is coppied into the new version. (or make a database of commands)
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
    '!command':{
        'limit':30,
        'argc':2,
        'return':"command",
        'access': 3
    },
    '!tt':{
        'limit':0,
        'return':'/me This is a timer test',
        'access': 3,
        'is_timed': 1,
        'argc':0,
        'timer_repeat': 300
    }

}

for command in commands:
    commands[command]['last_used'] = 0