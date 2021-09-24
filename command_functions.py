# -*- coding: utf-8 -*-
import time

from command_headers import *

import importlib


def is_valid_command(parameterCommand):  # Checks if command is in commands
    if parameterCommand.lower() in commands:
        return True


def update_last_used(parameterCommand):  # Update the last time used -> Affects only commands with cd
    commands[parameterCommand.lower()]['last_used'] = time.time()


def get_command_limit(parameterCommand):  # Get command cooldown
    return commands[parameterCommand.lower()]['limit']


def is_on_cooldown(parameterCommand):  # Checks if the command is on cooldown
    if time.time() - commands[parameterCommand.lower()]['last_used'] < commands[parameterCommand.lower()]['limit']:
        return True


def get_cooldown_remaining(parameterCommand):  # Gets the remaining seconds till the command can be used again
    return round(commands[parameterCommand.lower()]['limit'] - (time.time() - commands[parameterCommand.lower()]['last_used']))


def get_last_used(parameterCommand):
    return round(time.time() - commands[parameterCommand.lower()]['last_used'])


def get_timer_repeat(parameterCommand):
    return commands[parameterCommand.lower()]['timer_repeat']


def check_has_return(parameterCommand):  # If the command has a return, and doesn't execute a seperate code, return true
    if commands[parameterCommand.lower()]['return'] and commands[parameterCommand.lower()]['return'] != 'command':
        return True


def get_return(parameterCommand):  # Gets return
    return commands[parameterCommand.lower()]['return']


def check_has_args(parameterCommand):  # Checks if the command has argumets
    if 'argc' in commands[parameterCommand.lower()]:
        return True


def check_has_correct_args(message, parameterCommand):
    message = message.split(' ')
    if len(message) - 1 >= commands[parameterCommand.lower()][
        'argc']:  # IF it has same or more args it's true (TAKES Querry into account)
        return True


def check_is_timed(parameterCommand):
    if 'is_timed' in commands[parameterCommand.lower()]:
        if commands[parameterCommand.lower()]['is_timed'] == 1:
            return True


def check_returns_function(parameterCommand):  # Check if the command return as fucntion
    if commands[parameterCommand.lower()]['return'] == 'command':
        return True


def check_returns_giveaway(parameterCommand):
    if commands[parameterCommand.lower()]['return'] == 'giveaway':
        return True


def check_returns_enter(parameterCommand):
    if commands[parameterCommand.lower()]['return'] == 'enter':
        return True


def check_returns_guessing(parameterCommand):
    if commands[parameterCommand.lower()]['return'] == 'guessing':
        return True


def check_returns_guess(parameterCommand):
    if commands[parameterCommand.lower()]['return'] == 'guess':
        return True


def check_access_level(level, parameterCommand):
    if level >= commands[parameterCommand.lower()]['access']:
        return True


def pass_to_function(parameterCommand, args):
    # Passes the arguments to a separate function
    com = parameterCommand.lower().replace('!', '')

    module = importlib.import_module('commands.%s' % com.lower())
    function = getattr(module, com.lower())

    if args:
        # need to reference to commands.<command
        return function(args)
    else:
        # need to reference to commands.<command
        return function()


def return_commands():
    return commands
