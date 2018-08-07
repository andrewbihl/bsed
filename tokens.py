from enum import IntEnum


class Token(IntEnum):
    After = 0
    Append = 1
    Before = 2
    Clear = 3
    Containing = 4
    Delete = 5
    Ending = 6
    Insert = 7
    Lines = 8
    Prepend = 9
    Replace = 10
    Starting = 11
    With = 12
    Wrap = 13


token_list = [
    'after',
    'append',
    'before',
    'clear',
    'containing',
    'delete',
    'ending',
    'insert',
    'lines',
    'prepend',
    'replace',
    'starting',
    'with',
    'wrap'
]
