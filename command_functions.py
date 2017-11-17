import time

from command_headers import *

import importlib


def is_valid_command(command): #Checks if command is in commands
	if command in commands:
		return True

def update_last_used(command): #Update the last time used -> Affects only commands with cd
	commands[command]['last_used'] = time.time()

def get_command_limit(command): #Get command cooldown
	return commands[command]['limit']

def is_on_cooldown(command): #Checks if the command is on cooldown
	if time.time() - commands[command]['last_used'] < commands[command]['limit']:
		return True

def get_cooldown_remaining(command): #Gets the remaining seconds till the command can be used again
	return round(commands[command]['limit'] - (time.time() - commands[command]['last_used']))

def check_has_return(command): #If the command has a return, and doesn't execute a seperate code, return true
	if commands[command]['return'] and commands[command]['return'] != 'command':
		return True

def get_return(command): #Gets return
	return commands[command]['return']


def check_has_args(command): #Checks if the command has argumets
	if 'argc' in commands[command]:
		return True

def check_has_correct_args(message, command):
	message = message.split(' ')
	if len(message) - 1 >= commands[command]['argc']: # IF it has same or more args it's true (TAKES Querry into account)
		return True

def check_returns_function(command): #Check if the command return as fucntion
	if commands[command]['return'] == 'command':
		return True
def get_user_level(username):
	return 4
def check_access_level(username,command):
	if(commands[command]['access'] >= get_user_level(username)):
		return True

def pass_to_function(command, args): #Passes the arguments to a seperate function
	command = command.replace('!', '')

	module = importlib.import_module('commands.%s' % command)
	function = getattr(module, command)

	if args:
		# need to reference to commands.<command
		return function(args)
	else:
		# need to reference to commands.<command
		return function()
