import unittest
from os import path
import json
import inspect

import bsed.definitions as definitions
from bsed import interpreter

append_tests = path.join(definitions.TESTS_DIR, 'test_on_lines_containing.json')


class TestOnLinesContaining(unittest.TestCase):

    def setUp(self):
        self.interpreter = interpreter.default_interpreter()
        with open(append_tests, 'r') as fin:
            self.tests = json.load(fin)

    def perform_test(self, command: [str], input_file: str, expected_result_file: str):
        with open(expected_result_file, 'r') as fin:
            expected = fin.read()
        res = self.interpreter.build_command_and_execute([input_file] + command, return_output=True)
        self.assertEqual(expected, res)

    def perform_test_from_key(self, key: str):
        tests = self.tests[key]
        for t in tests:
            self.perform_test(t["command"], path.join(definitions.TEST_FILES_DIR, t["input"]), path.join(definitions.TEST_FILES_DIR, t["expected"]))

    def test_on_lines_delete(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_on_lines_replace(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_on_lines_prepend(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_on_lines_append(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)

    def test_on_lines_wrap(self):
        func_name = inspect.stack()[0].function
        self.perform_test_from_key(func_name)
