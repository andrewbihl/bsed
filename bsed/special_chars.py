
special_chars = {
    "\\$": '''\\044''',
    "\\": '''\\134''',
    "@": '''\\100''',
    "/": '''\\057''',
    "'": '''\\047''',
    "\"": '''\\042''',
    "`": '''\\140'''
}


def parse_special_chars(args: [str]) -> [str]:
    for i in range(len(args)):
        arg = args[i]
        for start in range(len(arg)):
            end = start + 1
            if arg[start] == '\\' and start < len(arg):
                end += 1
            c = arg[start:end]
            if c in special_chars:
                args[i] = arg[:start] + special_chars[c] + arg[end:]
    return args
