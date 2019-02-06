from os import system


def enable_autocomplete():
    command = 'eval "$(register-python-argcomplete bsed)"'
    system(command)
