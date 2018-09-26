#!/usr/bin/env python3

import sys
from os import system, path
import token_tree
import definitions
import arg_process

command_tree_fp = definitions.COMMAND_TOKEN_TREE

if len(sys.argv) < 2:
    print('Insufficient arguments. Usage: \'simplesed $input-file <commands>\'')
    exit(1)

file_arg = sys.argv[1]
if not path.exists(file_arg):
    print('Invalid file.')
    exit(2)

command_args = sys.argv[2:]

cmd_statement = arg_process.process_args(command_args)
tree = token_tree.TokenTree.from_json(command_tree_fp)
# tree.print_command_tree()
cmd, user_text_inputs = tree.validate_command(cmd_statement)
if cmd is not None:
    args = [file_arg] + user_text_inputs
    cmd = cmd.format(*args)
    print(cmd)
    system(cmd)
else:
    print('Invalid command.')


