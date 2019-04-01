# Instructions

1. Install bsed
    - `pip3 install --upgrade bsed`
2. Install argcomplete
    - `pip3 install argcomplete`
3. Register bsed for autocompletion
    - `echo eval "$(register-python-argcomplete bsed)" >> ~/.bash_profile`


# Common issues

1. Missing Python3 or Perl. Windows doesn't come with these by default.
2. argcomplete for python2 instead of python3
3. Activating a conda environment without running `eval "$(register-python-argcomplete bsed)"` afterward
