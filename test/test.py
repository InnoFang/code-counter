#!/usr/bin/env python3
# coding:utf8

import sys
import os
import unittest
from code_counter.core.argspaser import CodeCounterArgsParser
from code_counter.conf.config import Config
from code_counter.__main__ import main

bin_path = os.path.dirname(os.path.join(os.pardir, '..'))
lib_path = os.path.abspath(os.path.join(bin_path, 'code_counter'))
app_path = os.path.join(lib_path, '__main__.py')


class CodeCounterTest(unittest.TestCase):
    def test_print_help(self):
        options = ('python', app_path, '--help')
        sys.argv[1:] = options[2:]
        try:
            CodeCounterArgsParser()
        except SystemExit:
            pass

    def test_print_search_help(self):
        options = ('python', app_path, 'search', '--help')
        sys.argv[1:] = options[2:]
        try:
            CodeCounterArgsParser()
        except SystemExit:
            pass

    def test_print_config_help(self):
        options = ('python', app_path, 'config', '--help')
        sys.argv[1:] = options[2:]
        try:
            CodeCounterArgsParser()
        except SystemExit:
            pass

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
        parser = CodeCounterArgsParser()
        self.assertTrue('config' not in parser.args, '"config" is in the "args"')
        self.assertTrue('search' in parser.args, '"search" is not in the "args"')
        search_args = parser.args['search']
        self.assertEqual(search_args.path, '../code_counter/', "search path parsed error.")
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
        parser = CodeCounterArgsParser()
        self.assertTrue('config' in parser.args, '"config" is not in the "args"')
        self.assertTrue('search' not in parser.args, '"search" is in the "args"')
        config_args = parser.args['config']
        self.assertTrue(config_args.show_list, '--list flag parsed error.')
        self.assertEqual(config_args.suffix_add, ['lisp'], "suffix_add flag and values parsed error.")
        self.assertEqual(config_args.suffix_reset, ['clj'], "suffix_reset flag and values parsed error.")
        self.assertEqual(config_args.comment_add, ['//'], "comment_add flag and values parsed error.")
        self.assertEqual(config_args.comment_reset, [';'], "comment_reset flag and values parsed error.")
        self.assertEqual(config_args.ignore_add, ['.idea'], "ignore_add flag and values parsed error.")
        self.assertEqual(config_args.ignore_reset, ['target'], "ignore_reset flag and values parsed error.")
        self.assertTrue(config_args.restore, '--restore flag parsed error.')

    def test_search_case1(self):
        options = ['python', app_path,
                   'search',
                   '..',
                   '-v']
        sys.argv[1:] = options[2:]
        main()
