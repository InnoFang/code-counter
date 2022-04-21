#!/usr/bin/env python3
# coding:utf8

import sys
import os
import unittest
from unittest.mock import patch
from code_counter.core.argspaser import CodeCounterArgsParser
from code_counter.conf.config import Config
from code_counter.__main__ import main

test_path = os.path.abspath('.')
bin_path = os.path.dirname(os.path.join(os.pardir, '..'))
lib_path = os.path.abspath(os.path.join(bin_path, 'code_counter'))
app_path = os.path.join(lib_path, '__main__.py')


class CodeCounterTest(unittest.TestCase):
    def setUp(self):
        self.default_suffix = ["c", "cc", "clj", "cpp", "cs", "cu", "cuh", "dart", "go", "h",
                               "hpp", "java", "jl", "js", "kt", "lisp", "lua", "pde", "m", "php",
                               "py", "R", "rb", "rs", "rust", "sh", "scala", "swift", "ts", "vb"]
        self.default_comment = ["#", "//", "/*", "*", "*/", ":", ";", '""""']
        self.default_ignore = ["out", "venv", ".git", ".idea", "build", "target", "node_modules", ".vscode", "dist"]

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
        self.assertFalse(parser.has_config_args(), '"config" is in the "args"')
        self.assertTrue(parser.has_search_args(), '"search" is not in the "args"')
        search_args = parser.search()
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
        parser = CodeCounterArgsParser()
        self.assertTrue(parser.has_config_args(), '"config" is not in the "args"')
        self.assertFalse(parser.has_search_args(), '"search" is in the "args"')
        config_args = parser.config()
        self.assertTrue(config_args.show_list, '--list flag parsed error.')
        self.assertEqual(config_args.suffix_add, ['lisp'], "suffix_add flag and values parsed error.")
        self.assertEqual(config_args.suffix_reset, ['clj'], "suffix_reset flag and values parsed error.")
        self.assertEqual(config_args.comment_add, ['//'], "comment_add flag and values parsed error.")
        self.assertEqual(config_args.comment_reset, [';'], "comment_reset flag and values parsed error.")
        self.assertEqual(config_args.ignore_add, ['.idea'], "ignore_add flag and values parsed error.")
        self.assertEqual(config_args.ignore_reset, ['target'], "ignore_reset flag and values parsed error.")
        self.assertTrue(config_args.restore, '--restore flag parsed error.')

    @patch('builtins.input')
    def test_Config_restore(self, mock_input):
        mock_input.side_effect = ['y']

        options = ['python', app_path,
                   'config',
                   '--restore']
        sys.argv[1:] = options[2:]

        parser = CodeCounterArgsParser()
        self.assertTrue(parser.has_config_args())

        config = Config()
        config.invoke(parser.config())

        self.assertEqual(config.suffix, self.default_suffix, "the suffix doesn't equal")
        self.assertEqual(config.comment, self.default_comment, "the comment doesn't equal")
        self.assertEqual(config.ignore, self.default_ignore, "the ignore doesn't equal")

    @patch('builtins.input')
    def test_Config_reset1(self, mock_input):
        mock_input.side_effect = ['y', 'y', 'y', 'y', 'y']

        config = Config()
        config.restore()

        options = ['python', app_path,
                   'config',
                   '--suffix-reset=java,cpp,go,js,py',
                   '--comment-reset=//,#,/**',
                   '--ignore-reset=target,build,node_modules,__pycache__']
        sys.argv[1:] = options[2:]

        parser = CodeCounterArgsParser()
        self.assertTrue(parser.has_config_args())
        config.invoke(parser.config())

        suffix = ['java', 'cpp', 'go', 'js', 'py']
        comment = ['//', '#', '/**']
        ignore = ['target', 'build', 'node_modules', '__pycache__']

        self.assertEqual(config.suffix, suffix)
        self.assertEqual(config.comment, comment)
        self.assertEqual(config.ignore, ignore)

        config.restore()

    @patch('builtins.input')
    def test_Config_reset2(self, mock_input):
        mock_input.side_effect = ['y', 'n', 'y', 'y', 'y']

        config = Config()
        config.restore()

        options = ['python', app_path,
                   'config',
                   '--suffix-reset=java,cpp,go,js,py',
                   '--comment-reset=//,#,/**',
                   '--ignore-reset=target,build,node_modules,__pycache__']
        sys.argv[1:] = options[2:]

        parser = CodeCounterArgsParser()
        self.assertTrue(parser.has_config_args())
        config.invoke(parser.config())

        suffix = ['java', 'cpp', 'go', 'js', 'py']
        comment = ['//', '#', '/**']
        ignore = ['target', 'build', 'node_modules', '__pycache__']

        self.assertEqual(config.suffix, self.default_suffix)
        self.assertEqual(config.comment, comment)
        self.assertEqual(config.ignore, ignore)

        config.restore()

    @patch('builtins.input')
    def test_Config_reset3(self, mock_input):
        mock_input.side_effect = ['y', 'y', 'n', 'y', 'y']

        config = Config()
        config.restore()

        options = ['python', app_path,
                   'config',
                   '--suffix-reset=java,cpp,go,js,py',
                   '--comment-reset=//,#,/**',
                   '--ignore-reset=target,build,node_modules,__pycache__']
        sys.argv[1:] = options[2:]

        parser = CodeCounterArgsParser()
        self.assertTrue(parser.has_config_args())
        config.invoke(parser.config())

        suffix = ['java', 'cpp', 'go', 'js', 'py']
        comment = ['//', '#', '/**']
        ignore = ['target', 'build', 'node_modules', '__pycache__']

        self.assertEqual(config.suffix, suffix)
        self.assertEqual(config.comment, self.default_comment)
        self.assertEqual(config.ignore, ignore)

        config.restore()

    @patch('builtins.input')
    def test_Config_reset4(self, mock_input):
        mock_input.side_effect = ['y', 'y', 'y', 'n', 'y']

        config = Config()
        config.restore()

        options = ['python', app_path,
                   'config',
                   '--suffix-reset=java,cpp,go,js,py',
                   '--comment-reset=//,#,/**',
                   '--ignore-reset=target,build,node_modules,__pycache__']
        sys.argv[1:] = options[2:]

        parser = CodeCounterArgsParser()
        self.assertTrue(parser.has_config_args())
        config.invoke(parser.config())

        suffix = ['java', 'cpp', 'go', 'js', 'py']
        comment = ['//', '#', '/**']
        ignore = ['target', 'build', 'node_modules', '__pycache__']

        self.assertEqual(config.suffix, suffix)
        self.assertEqual(config.comment, comment)
        self.assertEqual(config.ignore, self.default_ignore)

        config.restore()

    @patch('builtins.input')
    def test_Config_add1(self, mock_input):
        mock_input.side_effect = ['y', 'y', 'y', 'y', 'y']

        config = Config()
        config.restore()

        options = ['python', app_path,
                   'config',
                   '--suffix-add=TEST_SUFFIX',
                   '--comment-add=TEST_COMMENT',
                   '--ignore-add=TEST_IGNORE']
        sys.argv[1:] = options[2:]

        parser = CodeCounterArgsParser()
        self.assertTrue(parser.has_config_args())
        config.invoke(parser.config())

        suffix = 'TEST_SUFFIX'
        comment = 'TEST_COMMENT'
        ignore = 'TEST_IGNORE'

        self.assertTrue(suffix in config.suffix)
        self.assertTrue(comment in config.comment)
        self.assertTrue(ignore in config.ignore)

        config.restore()

    @patch('builtins.input')
    def test_Config_add2(self, mock_input):
        mock_input.side_effect = ['y', 'n', 'y', 'y', 'y']

        config = Config()
        config.restore()

        options = ['python', app_path,
                   'config',
                   '--suffix-add=TEST_SUFFIX',
                   '--comment-add=TEST_COMMENT',
                   '--ignore-add=TEST_IGNORE']
        sys.argv[1:] = options[2:]

        parser = CodeCounterArgsParser()
        self.assertTrue(parser.has_config_args())
        config.invoke(parser.config())

        suffix = 'TEST_SUFFIX'
        comment = 'TEST_COMMENT'
        ignore = 'TEST_IGNORE'

        self.assertTrue(suffix not in config.suffix)
        self.assertTrue(comment in config.comment)
        self.assertTrue(ignore in config.ignore)

        config.restore()

    @patch('builtins.input')
    def test_Config_add3(self, mock_input):
        mock_input.side_effect = ['y', 'y', 'n', 'y', 'y']

        config = Config()
        config.restore()

        options = ['python', app_path,
                   'config',
                   '--suffix-add=TEST_SUFFIX',
                   '--comment-add=TEST_COMMENT',
                   '--ignore-add=TEST_IGNORE']
        sys.argv[1:] = options[2:]
        parser = CodeCounterArgsParser()
        args = parser.args
        self.assertTrue('config' in args)
        config.invoke(args['config'])

        suffix = 'TEST_SUFFIX'
        comment = 'not TEST_COMMENT'
        ignore = 'TEST_IGNORE'

        self.assertTrue(suffix in config.suffix)
        self.assertTrue(comment not in config.comment)
        self.assertTrue(ignore in config.ignore)

        config.restore()

    @patch('builtins.input')
    def test_Config_add4(self, mock_input):
        mock_input.side_effect = ['y', 'y', 'y', 'n', 'y']

        config = Config()
        config.restore()

        options = ['python', app_path,
                   'config',
                   '--suffix-add=TEST_SUFFIX',
                   '--comment-add=TEST_COMMENT',
                   '--ignore-add=TEST_IGNORE']
        sys.argv[1:] = options[2:]

        parser = CodeCounterArgsParser()
        self.assertTrue(parser.has_config_args())
        config.invoke(parser.config())

        suffix = 'TEST_SUFFIX'
        comment = 'TEST_COMMENT'
        ignore = 'TEST_IGNORE'

        self.assertTrue(suffix in config.suffix)
        self.assertTrue(comment in config.comment)
        self.assertTrue(ignore not in config.ignore)

        config.restore()

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
