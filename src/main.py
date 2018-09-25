import sys
from os import system, path
from src import token_tree
from src import definitions

command_tree_fp = definitions.COMMAND_TOKEN_TREE

if len(sys.argv) < 2:
    print('Insufficient arguments. Usage: \'simplesed $input-file <commands>\'')
    exit(1)

file_arg = sys.argv[1]
if not path.exists(file_arg):
    print('Invalid file.')
    exit(2)

command_args = sys.argv[2:]


def merge_quoted_phrases(cmd_args):
    """ Merge literal (quote-wrapped) inputs """
    start = -1
    for i in range(len(cmd_args)):
        arg = cmd_args[i]
        if start >= 0:
            if arg[-1] == '\"':
                new_arg = ' '.join(cmd_args[start:i+1])
                cmd_args = cmd_args[:start] + [new_arg] + cmd_args[i+1:]
                start = -1
                continue
        else:
            if arg[0] == '\"':
                start = i
    return cmd_args


cmd_statement = merge_quoted_phrases(command_args)
tree = token_tree.TokenTree.from_json(command_tree_fp)
cmd, user_text_inputs = tree.validate_command(cmd_statement)
if cmd is not None:
    args = [file_arg] + user_text_inputs
    cmd = cmd.format(*args)
    print(cmd)
    system(cmd)
# tree.print_command_tree()


