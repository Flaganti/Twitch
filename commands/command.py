from command_headers import *


def command(username, args):
    usage = "!command [add|edit|del] [command_name] [cooldown] [command string]"
    try:
        command_header = args[0]
        command_name=args[1]
        if(command_header=="del"):
            del commands[command_header]
            return "{} -> Command was successfully deleted.".format(username)
        cooldown = args [2]
        del args[0]
        del args[0]
        del args[0]
        command_string = str(args)
        if(command_header=="add"):
            commands.update({command_name:{
                'limit':cooldown,
                'argc':0,
                'return':command_string
            }})
            return "{} -> Command was successfully created.".format(username)
        elif(command_header=="edit"):
            commands[command_name]['limit']=cooldown
            commands[command_name]['return']=command_string
            return "{} -> Command was successfully edited.".format(username)
        else:
            return usage
    except:
        return usage
