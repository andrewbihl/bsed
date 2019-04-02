import unittest
from os import path
import json
import inspect

import bsed.definitions as definitions
from bsed import interpreter

special_chars_tests = path.join(definitions.TESTS_DIR, 'test_nonescaped_symbols.json')


def get_test_files_dir(test_dict: dict):
    if 'config' in test_dict and 'test_files_subdir' in test_dict['config']:
        test_files_dir = path.join(definitions.TEST_FILES_DIR, test_dict['config']['test_files_subdir'])
    else:
        test_files_dir = definitions.TEST_FILES_DIR
    return test_files_dir


class TestNonEscapedSymbols(unittest.TestCase):

    def setUp(self):
        self.interpreter = interpreter.default_interpreter()
        with open(special_chars_tests, 'r') as fin:
            self.tests = json.load(fin)
        self.test_files_dir = get_test_files_dir(self.tests)

    def perform_test(self, command: [str], input_file: str, expected_result_file: str):
        with open(expected_result_file, 'r') as fin:
            expected = fin.read()
        res = self.interpreter.build_command_and_execute([input_file] + command, return_output=True)
        self.assertEqual(expected, res)

    def perform_test_from_key(self, key: str):
        tests = self.tests[key]
        for t in tests:
            self.perform_test(t["command"], path.join(self.test_files_dir, t["input"]), path.join(self.test_files_dir, t["expected"]))

    def test_forward_slash(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_exclamation(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_at_sign(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_pound(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_percent(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_ampersand(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_underscore(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_semicolon(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_equals(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_tick(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_tilde(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_less_than(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_greater_than(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_single_quote(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_double_quote(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)
