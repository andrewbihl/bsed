#!/usr/bin/python

import sys
import os
import argparse
from os import path
import subprocess

basic_command_words = ['delete', 'replace', 'append', 'prepend', 'wrap']
basic_commands = {basic_command_words[0]: 's/%s//g',
                  basic_command_words[1]: 's/%s/%s/',
                  basic_command_words[2]:'s/%s/%s%s/',
                  basic_command_words[3]: 's/%s/%s%s/',
                  basic_command_words[4]: 's/%s/%s%s%s/'}


def print_generic_error_and_exit():
    print('Invalid input.')
    exit(2)


def interpret_delete(args) -> str:
    command_word = basic_command_words[0]
    assert args[0].lower() == command_word and len(args) == 2
    keyword = args[1]
    return basic_commands[command_word] % keyword


def interpret_replace(args) -> str:
    command_word = basic_command_words[1]
    assert args[0].lower() == command_word and len(args) == 4
    keyword = args[1]
    with_word = args[2]
    assert with_word.lower() == 'with'
    insert = args[3]
    return basic_commands[command_word] % (keyword, insert)


def interpret_append(args) -> str:
    command_word = basic_command_words[2]
    assert args[0].lower() == command_word and len(args) == 4
    keyword = args[1]
    with_word = args[2]
    assert with_word.lower() == 'with'
    insert = args[3]
    return basic_commands[command_word] % (keyword, keyword, insert)


def interpret_prepend(args) -> str:
    command_word = basic_command_words[3]
    assert args[0].lower() == command_word and len(args) == 4
    keyword = args[1]
    with_word = args[2]
    assert with_word.lower() == 'with'
    insert = args[3]
    return basic_commands[command_word] % (keyword, insert, keyword)


def interpret_wrap(args) -> str:
    command_word = basic_command_words[4]
    assert args[0].lower() == command_word and len(args) == 4
    keyword = args[1]
    with_word = args[2]
    assert with_word.lower() == 'with'
    insert = args[3]
    return basic_commands[command_word] % (keyword, insert, keyword, insert)


def interpret_basic_command(fin, basic_command_args):
    cmd = basic_command_args[0].lower()
    interpret_functions = [interpret_delete, interpret_replace, interpret_append, interpret_prepend, interpret_wrap]
    for i in range(len(basic_command_words)):
        cmd_key = basic_command_words[i]
        if cmd == cmd_key:
            cmd_str = interpret_functions[i](basic_command_args)
            return 'sed \'%s\' %s' % (cmd_str, fin)


if len(sys.argv) < 2:
    print('Insufficient arguments. Usage: \'simplesed $input-file <commands>\'')
    exit(1)

fin = sys.argv[1]

args = sys.argv[2:]

i = 0
curr = args[i]
if curr.lower() in basic_commands.keys():
    cmd_str = interpret_basic_command(fin, args[i:])
    os.system(cmd_str)


# import argparse
#
# parser = argparse.ArgumentParser(description='Process some text.')
# subcommands = parser.add_subparsers()
#
# subcommands.add_parser('find')
#
# args = parser.parse_args()
# print(parser)
#
#
