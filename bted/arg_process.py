#
# def merge_quoted_phrases(cmd_args):
#     """ Merge literal (quote-wrapped) inputs """
#     res = []
#     start = -1
#     for i in range(len(cmd_args)):
#         arg = cmd_args[i]
#         if start >= 0:
#             if arg[-1] == '\"':
#                 new_arg = ' '.join(cmd_args[start:i+1])
#                 res.append(new_arg)
#                 # cmd_args = cmd_args[:start] + [new_arg] + cmd_args[i+1:]
#                 start = -1
#                 continue
#         elif arg[0] == '\"':
#                 start = i
#         else:
#             res.append(arg)
#     return cmd_args


def extract_flags(cmd_args):
    flags = []
    res = []
    for i in range(len(cmd_args)):
        arg = cmd_args[i]
        if arg == ['--']:
            if i + 1 < len(cmd_args):
                res += cmd_args[i+1]
            break
        if arg[0] == '-':
            flags.append(arg)
        else:
            res.append(arg)
    return res, flags


def process_args(args: [str]) -> ([str], [str]):
    return extract_flags(args)
