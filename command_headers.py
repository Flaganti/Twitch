
#commands = {
#    '!test':{                          ->   command name
#        'limit': 0,                    ->   time limit in seconds
#        'argc': 0,                     ->   number of arguments needed -> only used for commands with return value of 'command'
#        'return': 'This is a test'     ->   return value, if 'command' -> execute command in commands
#    }

commands = {
    '!test':{
        'limit': 0,
        'return': 'This is a test'
    },
    '!limit':{
        'limit': 30,
        'argc': 2,
        'return': 'command'
    }
}

for command in commands:
    commands[command]['last_used'] = 0