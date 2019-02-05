import sys
from os import path
import subprocess
import argparse
import argcomplete

from .token_tree import TokenTree, token_trees
from .parser import Parser
import bsed.definitions as definitions
from .arg_process import process_args
from .translator import Translator


class Interpreter:
    accepted_flags = {'-i', '-t'}

    def __init__(self, command_tree_file, translations_dir):
        self.tree = TokenTree.from_json(command_tree_file)
        self.translator = Translator(definitions.CONFIG_DIR)
        self.parser = Parser(self.translator, token_trees)

    def print_commands(self):
        print("Supported commands:", file=sys.stderr)
        for k in self.tree.command_translations:
            print(' >', k, file=sys.stderr)

    def build_command(self, command_args, file_arg) -> (str, [str]):
        if file_arg is None:
            print('File argument not found.:', file=sys.stderr)
            return None, None
        cmd_statement, flags = process_args(command_args)
        unsupported_flags = [f for f in flags if f not in Interpreter.accepted_flags]
        if len(unsupported_flags) > 0:
            print('Invalid flags:', unsupported_flags, file=sys.stderr)
            return None, None

        # tree.print_command_tree()
        # cmd, user_text_inputs = self.tree.validate_command(cmd_statement)
        
        cmd, words_parsed = self.parser.translate_expression(cmd_statement, extra_args={'file': file_arg})
        if cmd is None:
            return None, None
        # if words_parsed < len(cmd_statement):
        #     return None, None

        # args = [file_arg] + user_text_inputs
        # inputs.update({'file': file_arg})
        # cmd_str = ' '.join(cmd)
        # cmd_str = cmd_str.format(**inputs)
        return cmd, flags

    @classmethod
    def execute_command(cls, cmd, flags, return_output=False, stdin=sys.stdin):
        if cmd is None:
            return None
        res = None
        translation_only = '-t' in flags
        in_place = '-i' in flags
        if in_place:
            parts = cmd.split()
            cmd = ' '.join(parts[:-1] + ['-i'] + [parts[-1]])
        if translation_only:
            print('Translation:\n >', cmd)
        else:
            # if return_output:
            #     with popen(cmd) as fout:
            #         return fout.read()
            stdout = subprocess.PIPE if return_output else None
            with subprocess.Popen(cmd, shell=True, stdout=stdout, stdin=stdin) as p:
                try:
                    # exit_code = subprocess.call(cmd, shell=True, stdout=stdout)
                    exit_code = p.wait()
                    if exit_code < 0:
                        print("Child was terminated by signal", -exit_code, file=sys.stderr)
                except OSError as e:
                    print("Execution failed:", e, file=sys.stderr)
                if return_output:
                    res = bytes.decode(p.stdout.read())
        return res


def default_interpreter():
    command_tree_fp = definitions.COMMAND_TOKEN_TREE
    translations_dir = definitions.CONFIG_DIR
    return Interpreter(command_tree_fp, translations_dir)


def print_commands():
    default_interpreter().print_commands()


def main():
    interpreter = default_interpreter()

    def autocomplete(parsed_args, prefix, **kwargs):
        # return kwargs['parsed_args'].get('command_tokens', ['HEllo', 'World'])
        # print('>>>>>>>>kwargs: ', kwargs)
        # if prefix.startswith('s'):
        #     return ['select']
        # return ['Hello', 'World']
        return interpreter.parser.possible_next_vals(parsed_args.command_tokens, prefix)


    parser = argparse.ArgumentParser(prog='bsed')
    parser.add_argument('-t', '--translate', action='store_true')
    parser.add_argument('-i', '--in-place', action='store_true')
    parser.add_argument('--', dest='ignore_remaining_args')
    parser.add_argument('input_file')
    parser.add_argument('command_tokens', nargs='*').completer = autocomplete

    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    cmd, flags = interpreter.build_command(args.command_tokens, args.input_file)
    if cmd is not None:
        interpreter.execute_command(cmd, flags)
    else:
        print('Invalid command.', file=sys.stderr)
