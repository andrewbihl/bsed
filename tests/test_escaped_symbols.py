import unittest
from os import path
import json
import inspect

import bsed.definitions as definitions
from bsed import interpreter

special_chars_tests = path.join(definitions.TESTS_DIR, 'test_escaped_symbols.json')


def get_test_files_dir(test_dict: dict):
    if 'config' in test_dict and 'test_files_subdir' in test_dict['config']:
        test_files_dir = path.join(definitions.TEST_FILES_DIR, test_dict['config']['test_files_subdir'])
    else:
        test_files_dir = definitions.TEST_FILES_DIR
    return test_files_dir


class TestEscapedSymbols(unittest.TestCase):

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

    def test_backslash(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_star(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_dot(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_question_mark(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_plus(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_pipe(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_dollar(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_caret(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_brackets(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_braces(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_parentheses(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)
