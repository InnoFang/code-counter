#!/usr/bin/env python3
# coding:utf8

import sys
import os
import unittest
from code_counter.__main__ import main

test_path = os.path.abspath('.')
bin_path = os.path.dirname(os.path.join(os.pardir, '..'))
lib_path = os.path.abspath(os.path.join(bin_path, 'code_counter'))
app_path = os.path.join(lib_path, '__main__.py')


class CodeCounterSearchTest(unittest.TestCase):
    def test_search_case1(self):
        options = ['python', app_path,
                   'search',
                   '..',
                   '-v',
                   '-o=output.txt']
        sys.argv[1:] = options[2:]
        main()

        output_path = os.path.join(test_path, 'output.txt')
        self.assertTrue(os.path.exists(output_path))
        os.remove(output_path)
