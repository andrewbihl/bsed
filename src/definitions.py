from os import path

ROOT_DIR = path.dirname(path.dirname(path.abspath(__file__)))
CONFIG_DIR = path.join(ROOT_DIR, 'config')
COMMAND_TRANSLATIONS_FILE = path.join(CONFIG_DIR, 'command_translations.json')
COMMAND_TOKEN_TREE = path.join(CONFIG_DIR, 'command_token_tree.json')
