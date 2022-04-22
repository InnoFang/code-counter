#!/usr/bin/env python3
# coding:utf8

import sys
import os
import unittest
from code_counter.core.args import CodeCounterArgs

test_path = os.path.abspath('.')
bin_path = os.path.dirname(os.path.join(os.pardir, '..'))
lib_path = os.path.abspath(os.path.join(bin_path, 'code_counter'))
app_path = os.path.join(lib_path, '__main__.py')


class CodeCounterArgsTest(unittest.TestCase):
    def test_search_args(self):
        options = ['python', app_path,
                   'search',
                   '../code_counter/',
                   '-v',
                   '-g',
                   '-o=output.txt',
                   '--suffix=py,java,cpp',
                   '--comment=//,#,/*',
                   '--ignore=.vscode,.idea']
        sys.argv[1:] = options[2:]
        args = CodeCounterArgs()
        self.assertFalse(args.has_config_args(), '"config" is in the "args"')
        self.assertTrue(args.has_search_args(), '"search" is not in the "args"')
        search_args = args.search()
        self.assertEqual(search_args.input_path, ['../code_counter/'], "search path parsed error.")
        self.assertTrue(search_args.verbose, '-v,--verbose flag parsed error.')
        self.assertTrue(search_args.graph, '-g,--graph flag parsed error.')
        self.assertEqual(search_args.output_path, 'output.txt', "output path parsed error.")
        self.assertEqual(search_args.suffix, ['py', 'java', 'cpp'], "suffix flag and values parsed error.")
        self.assertEqual(search_args.comment, ['//', '#', '/*'], "comment flag and values parsed error.")
        self.assertEqual(search_args.ignore, ['.vscode', '.idea'], "ignore flag and values parsed error.")

    def test_config_args(self):
        options = ['python', app_path,
                   'config',
                   '--list',
                   '--suffix-add=lisp',
                   '--suffix-reset=clj',
                   '--comment-add=//',
                   '--comment-reset=;',
                   '--ignore-add=.idea',
                   '--ignore-reset=target',
                   '--restore']
        sys.argv[1:] = options[2:]
        args = CodeCounterArgs()
        self.assertTrue(args.has_config_args(), '"config" is not in the "args"')
        self.assertFalse(args.has_search_args(), '"search" is in the "args"')
        config_args = args.config()
        self.assertTrue(config_args.show_list, '--list flag parsed error.')
        self.assertEqual(config_args.suffix_add, ['lisp'], "suffix_add flag and values parsed error.")
        self.assertEqual(config_args.suffix_reset, ['clj'], "suffix_reset flag and values parsed error.")
        self.assertEqual(config_args.comment_add, ['//'], "comment_add flag and values parsed error.")
        self.assertEqual(config_args.comment_reset, [';'], "comment_reset flag and values parsed error.")
        self.assertEqual(config_args.ignore_add, ['.idea'], "ignore_add flag and values parsed error.")
        self.assertEqual(config_args.ignore_reset, ['target'], "ignore_reset flag and values parsed error.")
        self.assertTrue(config_args.restore, '--restore flag parsed error.')
