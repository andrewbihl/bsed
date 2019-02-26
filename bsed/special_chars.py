
special_chars = {
    "\\$": '''\\044''',
    "\\\\": '''\\134'''
}


def parse_special_chars(args: [str]) -> [str]:
    for i in range(len(args)):
        arg = args[i]
        for j in range(len(arg)-1):
            if arg[j] != '\\':
                continue
            c = arg[j:j+2]
            if c in special_chars:
                args[i] = arg[:j] + special_chars[c] + arg[j+2:]
    return args
