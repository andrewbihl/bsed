from os import path

SOURCE_ROOT = path.dirname(path.abspath(__file__))
PROJECT_ROOT = path.dirname(SOURCE_ROOT)
TESTS_DIR = path.join(PROJECT_ROOT, 'tests')
TEST_FILES_DIR = path.join(TESTS_DIR, 'test_files')
CONFIG_DIR = path.join(SOURCE_ROOT, 'config')
COMMAND_TOKEN_TREE = path.join(CONFIG_DIR, 'token_tree.json')
