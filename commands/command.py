from command_headers import *
#TODO: Save changes to file
def command(args):
    usage = "/me {user} -> !command [add|edit|del] [command_name] [cooldown] [access] [command string]"
    print("Gets till here")
    try:
        command_header = args[0]
        command_name=args[1]
        if(command_header=="del"):
            del commands[command_header]
            return "/me {user} command was successfully deleted."
        cooldown = int(args[2])
        access = int(args[3])
        del args[0]
        del args[0]
        del args[0]
        del args[0]
        command_string = " ".join(args)
        if(command_header=="add"):
            commands.update({command_name:{
                'limit':cooldown,
                'argc':0,
                'return':command_string,
                'access':access,
                'last_used':0
            }})
            print("Add done")
            return "/me {user} command was successfully created."
        elif(command_header=="edit"):
            commands[command_name]['limit']=cooldown
            commands[command_name]['return']=command_string
            commands[command_name]['access']=access
            commands[command_name]['last_used']=0
            return "/me {user} command was successfully edited."
        else:
            return usage
    except:
        return usage
