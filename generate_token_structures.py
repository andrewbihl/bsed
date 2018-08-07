token_str = ''

with open('tokens.txt', 'r') as fin:
    tokens = [line.strip().lower() for line in fin.readlines()]
    token_str += 'from enum import IntEnum\n'
    token_str += '\n\n'
    token_str += 'class Token(IntEnum):\n'
    for i, token_lower in enumerate(tokens):
        enum_line = '    %s = %d\n' % (token_lower.capitalize(), i)
        token_str += enum_line
    token_str += '\n\n'
    token_str += 'token_list = [\n'
    for token_lower in tokens:
        token_str += '    \'%s\',\n' % token_lower
    token_str = token_str[:-2] + '\n]\n'

with open('tokens.py', 'w') as fout:
    fout.write(token_str)