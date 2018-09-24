import sys
from os import path, system
import token_tree


json_fp = path.join('config', 'command_token_tree.json')

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


cmd_args = merge_quoted_phrases(command_args)
tree = token_tree.TokenTree.from_json(json_fp)
cmd, user_text_inputs = tree.validate_command(cmd_args)
if cmd is not None:
    cmd = cmd % tuple(user_text_inputs + [file_arg])
    print(cmd)
    system(cmd)
# tree.print_command_tree()


