# -*- coding: utf-8 -*-
import time

from command_headers import *

import importlib


def is_valid_command(command): #Checks if command is in commands
	if command.lower() in commands:
		return True

def update_last_used(command): #Update the last time used -> Affects only commands with cd
	commands[command.lower()]['last_used'] = time.time()

def get_command_limit(command): #Get command cooldown
	return commands[command.lower()]['limit']

def is_on_cooldown(command): #Checks if the command is on cooldown
	if time.time() - commands[command.lower()]['last_used'] < commands[command.lower()]['limit']:
		return True

def get_cooldown_remaining(command): #Gets the remaining seconds till the command can be used again
	return round(commands[command.lower()]['limit'] - (time.time() - commands[command.lower()]['last_used']))

def get_last_used(command):
	return round(time.time() - commands[command.lower()]['last_used'])

def get_timer_repeat(command):
	return commands[command.lower()]['timer_repeat']

def check_has_return(command): #If the command has a return, and doesn't execute a seperate code, return true
	if commands[command.lower()]['return'] and commands[command.lower()]['return'] != 'command':
		return True

def get_return(command): #Gets return
	return commands[command.lower()]['return']


def check_has_args(command): #Checks if the command has argumets
	if 'argc' in commands[command.lower()]:
		return True

def check_has_correct_args(message, command):
	message = message.split(' ')
	if len(message) - 1 >= commands[command.lower()]['argc']: # IF it has same or more args it's true (TAKES Querry into account)
		return True

def check_is_timed(command):
	if 'is_timed' in commands[command.lower()]:
		if commands[command.lower()]['is_timed'] == 1:
			return True

def check_returns_function(command): #Check if the command return as fucntion
	if commands[command.lower()]['return'] == 'command':
		return True

def check_returns_giveaway(command):
	if commands[command.lower()]['return'] == 'giveaway':
		return True

def check_returns_enter(command):
	if commands[command.lower()]['return']  == 'enter':
		return True

def get_user_level(tags): #Get user level from tags -> Some tags are irrelevant
	userLevel = 0
	badges,color,dName,emotes,id,mod,roomId,sub,timestamp,turbo,userId,userType = tags[1:].split(";")

	mod=mod.split("=")[1]
	sub=sub.split("=")[1]

	if(sub=="1"):
		userLevel=1
	if(mod=="1"):
		userLevel=2
	if("broadcaster" in badges):
		userLevel=3
	print("UserLevel: {}".format(userLevel))
	return userLevel

def check_access_level(tags,command):
	if(get_user_level(tags) >= commands[command.lower()]['access'] ):
		return True

def pass_to_function(command, args): #Passes the arguments to a seperate function
	command = command.lower().replace('!', '')

	module = importlib.import_module('commands.%s' % command.lower())
	function = getattr(module, command.lower())

	if args:
		# need to reference to commands.<command
		return function(args)
	else:
		# need to reference to commands.<command
		return function()

def return_commands():
	return  commands