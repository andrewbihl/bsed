import unittest
import os
from os import path
import json
from shutil import copy

import bsed.definitions as definitions
from bsed import interpreter


def get_test_files_dir(test_dict: dict):
    if 'config' in test_dict and 'test_files_subdir' in test_dict['config']:
        test_files_dir = path.join(definitions.TEST_FILES_DIR, test_dict['config']['test_files_subdir'])
    else:
        test_files_dir = definitions.TEST_FILES_DIR
    return test_files_dir


class TestInPlaceFlag(unittest.TestCase):

    @staticmethod
    def __f_to_str(file_path):
        with open(file_path, 'r') as fin:
            content = fin.read()
        return content

    def setUp(self):
        self.test_files = [path.join(definitions.TESTS_DIR, f)
                           for f in os.listdir(definitions.TESTS_DIR)
                           if f.startswith('test_') and f.endswith('.json')]
        self.interpreter = interpreter.default_interpreter()

    def perform_test(self, command: [str], input_file: str, expected_result_file: str):
        expected = TestInPlaceFlag.__f_to_str(expected_result_file)
        tmp_file = 'tmp.txt'
        copy(input_file, 'tmp.txt')
        self.interpreter.build_command_and_execute([tmp_file] + command, return_output=True)
        res = TestInPlaceFlag.__f_to_str(tmp_file)
        os.remove(tmp_file)
        self.assertEqual(expected, res)

    def test_all(self):
        print()
        for test_file in self.test_files:
            print(path.split(test_file)[-1])
            with open(test_file, 'r') as fin:
                test_dict = json.load(fin)

            test_files_dir = get_test_files_dir(test_dict)

            for command, tests in test_dict.items():
                if not command.startswith('test_'):
                    continue
                print('\t%s' % command)
                for test in tests:
                    input_file = path.join(test_files_dir, test['input'])
                    expected_file = path.join(test_files_dir, test['expected'])
                    command = test['command'] + ['-i']
                    self.perform_test(command, input_file, expected_file)
