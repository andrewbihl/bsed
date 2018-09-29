import sys
from os import system, path
import json

from .token_tree import TokenTree
import bted.definitions as definitions
from .arg_process import process_args

command_tree_fp = definitions.COMMAND_TOKEN_TREE
translations_fp = definitions.COMMAND_TRANSLATIONS_FILE
accepted_flags = {'-t'}


class Interpreter:
    def __init__(self, command_tree_file, translations_file):
        self.tree = TokenTree.from_json(command_tree_file, translations_file)

    def print_commands(self):
        print("Supported commands:")
        for k in self.tree.command_translations:
            print(' >', k)

    def build_command(self, command_args, file_arg):
        cmd_statement, flags = process_args(command_args)
        unsupported_flags = [f for f in flags if f not in accepted_flags]
        if len(unsupported_flags) > 0:
            print('Invalid flags:', unsupported_flags)
            return None, None

        # tree.print_command_tree()
        cmd, user_text_inputs = self.tree.validate_command(cmd_statement)
        if cmd is None:
            return None, None
        args = [file_arg] + user_text_inputs
        cmd = cmd.format(*args)
        return cmd, flags

    @classmethod
    def execute_command(cls, cmd, flags):
        translation_only = '-t' in flags
        if translation_only:
            print('Translation:\n >', cmd)
        else:
            system(cmd)


def main():
    if len(sys.argv) < 2:
        print('Insufficient arguments. Format: \'bted <input-file> <command statement>\'\n'
              'For example: \n'
              '> bted example.txt delete lines starting with "example Phrase"\n'
              '> bted example.txt select lines containing "Andrew"\n'
              '> bted example.txt prepend beat with "Don\'t stop the "')
        exit(1)

    file_arg = sys.argv[1]
    if not path.exists(file_arg):
        print('File not found.')
        exit(2)

    interpreter = Interpreter(command_tree_fp, translations_fp)
    cmd, flags = interpreter.build_command(sys.argv[2:], file_arg)
    if cmd is not None:
        interpreter.execute_command(cmd, flags)
    else:
        print('Invalid command.')
