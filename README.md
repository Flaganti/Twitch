# FlagBot
## What is this bot?
FlagBot is a python Twich bot used for Twitch chat moderation
FlagBot is constantly being updated with new features
## How to install?
Just download/copy/clone the project and start the main.py.

### [Can I add my own commands to the bot?](https://github.com/Flaganti/Twitch/blob/master/command_headers.py)

Yes. Use the !command
Or if you know some python you can add commands in the command_headers.py

    commands = {
        '!test':{                          ->   command name
            'limit': 0,                    ->   time limit in seconds
            'argc': 0,                     ->   number of arguments needed -> only used for commands with return value of 'command'
            'return': 'This is a test'     ->   return value, if 'command' -> execute command in commands
            'access': [0,1,2,3,4]
        }
    }
    Access Levels:
    0 -> Everyone
    1 -> Regular
    2 -> Subscriber
    3 -> Moderator
    4 -> Owner
    
if you used 'command' as the return value
create your own python file and put it into the commands [folder](https://github.com/Flaganti/Twitch/blob/master/commands/)

    def limit(args):
        usage = "Usage: !limit <number1> <number2>"
        data =''
    
    try:
        n1,n2 = (int(args[0]),int(args[1]))
        for x in range(n1,n2+1):
            if x == n2:
                data+='%s' % x
            else:
                data+='%s, ' % x

    except:
        return usage
    return data

## Features
### Working Features
* Read chat
* Reply to commands
* Add custom commands
* Access levels for commands

### To be implamented
* Timers
* Moderation support
* Point system
* Webserver for Point store

