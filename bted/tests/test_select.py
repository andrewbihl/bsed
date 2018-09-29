import unittest
from os import path
import json
import inspect

import bted.definitions as definitions
from bted import interpreter

test_files_dir = 'test_files'
select_tests = 'test_select.json'


class TestSelect(unittest.TestCase):

    def setUp(self):
        command_tree_fp = definitions.COMMAND_TOKEN_TREE
        translations_fp = definitions.COMMAND_TRANSLATIONS_FILE
        self.interpreter = interpreter.Interpreter(command_tree_fp, translations_fp)
        with open(select_tests, 'r') as fin:
            self.tests = json.load(fin)

    def perform_test(self, command: [str], input_file: str, expected_result_file: str):
        with open(expected_result_file, 'r') as fin:
            expected = fin.read()
        cmd, flags = self.interpreter.build_command(command, input_file)
        res = self.interpreter.execute_command(cmd, flags, return_output=True)
        self.assertEqual(res, expected)

    def test_select_lines_containing_word(self):
        func_name = inspect.stack()[0].function
        tests = self.tests[func_name]
        for t in tests:
            self.perform_test(t["command"], path.join(test_files_dir, t["input"]), path.join(test_files_dir, t["expected"]))

    def test_select_lines_starting_with_word(self):
        func_name = inspect.stack()[0].function
        tests = self.tests[func_name]
        for t in tests:
            self.perform_test(t["command"], path.join(test_files_dir, t["input"]), path.join(test_files_dir, t["expected"]))

    def test_select_lines_ending_with_word(self):
        func_name = inspect.stack()[0].function
        tests = self.tests[func_name]
        for t in tests:
            self.perform_test(t["command"], path.join(test_files_dir, t["input"]), path.join(test_files_dir, t["expected"]))