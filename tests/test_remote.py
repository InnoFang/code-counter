#!/usr/bin/env python3
# coding:utf8

import sys
import os
import unittest
from unittest.mock import patch
from code_counter.__main__ import main

test_path = os.path.abspath('.')
bin_path = os.path.dirname(os.path.join(os.pardir, '..'))
lib_path = os.path.abspath(os.path.join(bin_path, 'code_counter'))
app_path = os.path.join(lib_path, '__main__.py')


class CodeCounterRemoteTest(unittest.TestCase):
    @patch('builtins.input')
    def test_remote_case1(self, mock_input):
        mock_input.side_effect = ['']
        options = ['python', app_path,
                   'remote',
                   'https://github.com/innofang/code-counter.git',
                   '-v',
                   '-o=output.txt']
        sys.argv[1:] = options[2:]
        try:
            main()
        except:
            print('Occur Error!')

        output_path = os.path.join(test_path, 'output.txt')
        self.assertTrue(os.path.exists(output_path))
        os.remove(output_path)
