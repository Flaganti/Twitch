# FlagBot
## What is this bot?
FlagBot is a python Twitch bot used for Twitch chat moderation

FlagBot is constantly being updated with new features
## How to install?
* Download and install python 3.9
* Copy/clone/download the project
* Run pip install -r .\requirements.txt
* Run the code with py main.py

### [Can I add my own commands to the bot?](https://github.com/Flaganti/Twitch/blob/master/command_headers.py)

Yes. Use the !command, command.

Or if you know some python you can add commands in the command_headers.py

    commands = {
        '!test':{                          ->   command name
            'limit': 0,                    ->   time limit in seconds
            'argc': 0,                     ->   number of arguments needed -> only used for commands with return value of 'command'
            'return': 'This is a test'     ->   return value, if 'command' -> execute command in commands
            'access': [0,1,2,3]
            'is_timed': 0,1                ->   0 no, 1 yes
            'timer_repeat': 300            ->   time in seconds
        }
    }
    Access Levels:
    0 -> Everyone
    1 -> Subscriber
    2 -> Moderator
    3 -> Owner
    
if you used 'command' as the return value, create your own python file and put it into the commands [folder](https://github.com/Flaganti/Twitch/blob/master/commands/)

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
* Timers
* Point system (partially)
### To be implemented
* Moderation support 
* Point system (partially)
* Webserver for Point store
