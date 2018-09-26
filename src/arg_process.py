
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


def process_args(args: [str]) -> [str]:
    return merge_quoted_phrases(args)