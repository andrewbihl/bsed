import os
import sys
import json
import subprocess
import argparse
import argcomplete

from .token_tree import TokenTree, token_trees, Keyword
from .parser import Parser
import bsed.definitions as definitions
from .translator import Translator
from .special_chars import parse_special_chars


class Interpreter:
    accepted_flags = {'-i', '-t'}

    def __init__(self, command_tree_file):
        self.tree = TokenTree.from_json(command_tree_file)
        self.translator = Translator(definitions.CONFIG_DIR)
        self.parser = Parser(self.translator, token_trees)

    def print_commands(self):
        with open(definitions.COMMAND_TOKEN_TREE, 'r') as fin:
            tree_dict = json.load(fin)
        print("Supported commands:", file=sys.stderr)
        translation_file = tree_dict[Keyword.ROOT_TREE.value][Keyword.TRANSLATIONS_FILE.value]
        self.translator.load_translations(translation_file)
        for k in self.translator.translations[translation_file]:
            print(' >', k, file=sys.stderr)
        print("\nLine filters:", file=sys.stderr)
        translation_file = tree_dict['line-filters'][Keyword.TRANSLATIONS_FILE.value]
        self.translator.load_translations(translation_file)
        for k in self.translator.translations[translation_file]:
            print(' >', k, file=sys.stderr)

    def build_command_and_execute(self, inputs: [str],  return_output=False, stdin=sys.stdin):
        cmd, args = self._build_command(inputs)
        if cmd is None:
            print('Invalid command.', file=sys.stderr)
            return None
        return Interpreter.execute_command(cmd, translation_only=args.translate, in_place=args.in_place,
                                           return_output=return_output, stdin=sys.stdin)

    def _build_command(self, inputs: [str]) -> (str, [str]):

        def autocomplete(parsed_args, prefix, **kwargs):
            command_tokens = parsed_args.command_tokens
            if len(command_tokens) > 0:
                cmd_start = 0
                if os.path.exists(command_tokens[0]):
                    cmd_start = 1
                return self.parser.possible_next_vals(command_tokens[cmd_start:])
            return self.parser.possible_next_vals(command_tokens) + custom_root_commands()

        def custom_root_commands(**kwargs):
            return ['help', 'commands']

        def custom_validator(completion, prefix):
            if not completion.startswith(prefix):
                return False
            if completion.startswith('$USER'):
                return False
            return True

        parser = argparse.ArgumentParser(prog='bsed')
        parser.add_argument('-t', '--translate', action='store_true', help='Print the translated comamnd without executing.')
        parser.add_argument('-i', '--in-place', action='store_true', help='Save the output to the input file. Not recommended.')
        parser.add_argument('--', dest='ignore_remaining_args')
        parser.add_argument('command_tokens', nargs='*').completer = autocomplete

        argcomplete.autocomplete(parser, validator=custom_validator, always_complete_options=False)

        input_file = ''
        args = parser.parse_args(inputs)
        tokens = args.command_tokens
        if len(tokens) < 2:
            return None, None
        if os.path.exists(tokens[0]):
            input_file = args.command_tokens.pop(0)
        elif os.path.exists(tokens[-1]):
            input_file = args.command_tokens.pop(-1)
        elif sys.stdin.isatty():
            print('File argument not found.', file=sys.stderr)
            return None, None

        args.command_tokens = parse_special_chars(args.command_tokens)
        cmd, words_parsed = self.parser.translate_expression(args.command_tokens, extra_args={'file': input_file})
        if cmd is None:
            return None, None
        return cmd, args

    @classmethod
    def execute_command(cls, cmd, translation_only=False, in_place=False, return_output=False, stdin=sys.stdin):
        if cmd is None:
            return None
        res = None
        if in_place:
            parts = cmd.split()
            cmd = ' '.join(parts[:-1] + ['-i'] + [parts[-1]])
        if translation_only:
            print('Translation:\n >', cmd)
        else:
            stdout = subprocess.PIPE if return_output else None
            with subprocess.Popen(cmd, shell=True, stdout=stdout, stdin=stdin) as p:
                try:
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
    return Interpreter(command_tree_fp)


def print_commands():
    default_interpreter().print_commands()


def print_help():
    default_interpreter().build_command_and_execute(['-h'])


def main():

    if len(sys.argv[1:]) == 1:
        if sys.argv[1] == 'help':
            print_help()
            return
        if sys.argv[1] == 'commands':
            print_commands()
            return
    # args = parse_special_chars(sys.argv[1:])
    interpreter = default_interpreter()
    interpreter.build_command_and_execute(sys.argv[1:])
