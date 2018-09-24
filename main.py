#!/usr/bin/python

import sys
from os import path
from tokens import Token, token_list

basic_command_words = ['delete', 'replace', 'append', 'prepend', 'wrap']
basic_commands = {basic_command_words[0]: 's/%s//g',
                  basic_command_words[1]: 's/%s/%s/',
                  basic_command_words[2]: 's/%s/%s%s/',
                  basic_command_words[3]: 's/%s/%s%s/',
                  basic_command_words[4]: 's/%s/%s%s%s/'}


def num_args_for_command(command_word):
    if command_word not in basic_commands.keys():
        return -1
    if command_word.lower() == 'delete':
        return 1
    return 3


def print_generic_error_and_exit():
    print('Invalid input.')
    exit(3)


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


def consume_user_string(args) -> (str, list):
    if len(args) == 0:
        return None
    if not args[0].startswith('\"') or args[0].startswith('\''):
        res = args.pop(0)
        return res, args
    res = ''
    i = 0
    while i < len(args):
        s = args.pop(0)
        last = s.endswith('\'') or s.endswith('\"')
        res += s.strip('\"\'')
        if last:
            return res, args
    print('Please terminate string.')
    exit(4)

if len(sys.argv) < 2:
    print('Insufficient arguments. Usage: \'simplesed $input-file <commands>\'')
    exit(1)

fin = sys.argv[1]
if not path.exists(fin):
    print('Invalid file.')
    exit(2)

cmd_args = sys.argv[2:]

# i = 0
# curr = cmd_args[i]
# if curr.lower() in basic_commands.keys():
#     cmd_str = interpret_basic_command(fin, cmd_args[i:])


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
