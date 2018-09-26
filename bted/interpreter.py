import sys
from os import system, path
import json

from .token_tree import TokenTree
import bted.definitions as definitions
from .arg_process import process_args


command_tree_fp = definitions.COMMAND_TOKEN_TREE

translations_fp = definitions.COMMAND_TRANSLATIONS_FILE

accepted_flags = {'-t'}


def print_commands():
    with open(translations_fp, 'r') as fin:
        command_translations = json.load(fin)
    print("Supported commands:")
    for k in command_translations:
        print(' >', k)


def main():

    if len(sys.argv) < 2:
        print('Insufficient arguments. Usage: \'bted $input-file <commands>\'')
        exit(1)

    file_arg = sys.argv[1]
    if not path.exists(file_arg):
        print('Invalid file.')
        exit(2)

    command_args = sys.argv[2:]

    cmd_statement, flags = process_args(command_args)
    unsupported_flags = [f for f in flags if f not in accepted_flags]
    if len(unsupported_flags) > 0:
        print('Invalid flags:', unsupported_flags)
        return
    translation_only = '-t' in flags

    if translation_only:
        print('Command statement:\n >', cmd_statement)
        print('Flags:\n >', flags)

    tree = TokenTree.from_json(command_tree_fp, translations_fp)
    # tree.print_command_tree()
    cmd, user_text_inputs = tree.validate_command(cmd_statement)
    if cmd is not None:
        args = [file_arg] + user_text_inputs
        cmd = cmd.format(*args)
        if translation_only:
            print('Translation:\n >', cmd)
        else:
            system(cmd)
    else:
        print('Invalid command.')
