# -*- coding: utf-8 -*-
import config
import command_functions as commands


def chat(sock, msg):
	"""
	Send a chat message to the server.
	Keyword arguments:
	sock -- the socket over which to send the message
	msg  -- the message to be sent
	"""
	sock.send(("PRIVMSG {} :{}\r\n".format(config.CHAN, msg)))

def ban(sock, user):
	"""
	Ban a user from the current channel.
	Keyword arguments:
	sock -- the socket over which to send the ban command
	user -- the user to be banned
	"""
	chat(sock, ".ban {}".format(user))

def timeout(sock, user, secs=600):
	"""
	Time out a user for a set period of time.
	Keyword arguments:
	sock -- the socket over which to send the timeout command
	user -- the user to be timed out
	secs -- the length of the timeout in seconds (default 600)
	"""
	chat(sock, ".timeout {}".format(user, secs))

def func_command(sock, username, message):
	if (commands.is_valid_command(message) or commands.is_valid_command(message.split(' ')[0])) and (commands.check_access_level(username,message.split(' ')[0]) or commands.check_access_level(username,message)):
		command = message
		if commands.check_returns_function(command.split(' ')[0]):
			if commands.check_has_correct_args(command, command.split(' ')[0]): #TODO: CHANGE this or ANND QUERRY FLAG TO FUNCTION
				args = command.split(' ')
				del args[0]
				command = command.split(' ')[0]

				if commands.is_on_cooldown(command):
					print('Command is on cooldown. (%s) (%s) (%ss remaining)' % (command, username, commands.get_cooldown_remaining(command)))

				else:
					print('Command is valid an not on cooldown. (%s) (%s)' % (command, username))
					result = commands.pass_to_function(command, args)
					commands.update_last_used(command)

					if result:
						resp = '@%s > %s' % (username, result)
						print(resp)
						chat(sock, command_formatter_message(result,username))
			else:
				chat(sock, command_formatter_message(commands.pass_to_function(command.split(' ')[0], ('','')),username))#Print out command usage!

		else:
			if commands.is_on_cooldown(command.split(' ')[0]):
				print('Command is on cooldown. (%s) (%s) (%ss remaining)' % (command, username, commands.get_cooldown_remaining(command)))
			elif(commands.check_has_args(command.split(' ')[0])):#TODO: Make this a seperate function
				args = command.split(' ')
				del args[0]
				command = command.split(' ')[0]
				print('empty')
				chat(sock,command_formatter(username,command,args))

			elif commands.check_has_return(command):
				print('Command is valid an not on cooldown. (%s) (%s)' % (command, username))

				resp = '@%s > %s' % (username, commands.get_return(command))
				commands.update_last_used(command)

				print(resp)
				chat(sock,command_formatter(username,command,[]))

def give_points():
	return ''

def command_formatter_message(message,username=''):
	argc={'user':username,'points':0}
	return str(message.format(**argc))

def command_formatter(username,command,args): # formats the string
	argc={}
	if(len(args)<1):
		argc={'user':username,'target':username,'points':0} #creats dict
	else:
		argc={'user':username,'target':args[0],'points':0}

	return str(commands.get_return(command)).format(**argc) #replaces values with dict values


def check_timers(sock): #Checks for timers
	command = commands.return_commands()
	for key in command:
		if(commands.check_is_timed(key)):
			print(commands.get_last_used(key))
			if(commands.get_last_used(key) >= commands.get_timer_repeat(key)):
				if(commands.get_return(key)=='command'): #if the timer is a seperate command -> execute this
					result = commands.pass_to_function(key,[])
					chat(sock, command_formatter_message(result)) #formats result from command
				else:
					result = command_formatter('',key,[]) #formats result from timer
					chat(sock, result)
				commands.update_last_used(key)





