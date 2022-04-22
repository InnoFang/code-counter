#!/usr/bin/env python3
# coding:utf8

import os
import sys
import unittest
from unittest.mock import patch

from code_counter.conf.config import Config
from code_counter.core.args import CodeCounterArgs

test_path = os.path.abspath('.')
bin_path = os.path.dirname(os.path.join(os.pardir, '..'))
lib_path = os.path.abspath(os.path.join(bin_path, 'code_counter'))
app_path = os.path.join(lib_path, '__main__.py')


class CodeCounterConfigTest(unittest.TestCase):
    def setUp(self):
        self.default_suffix = {"c", "cc", "clj", "cpp", "cs", "cu", "cuh", "dart", "go", "h",
                               "hpp", "java", "jl", "js", "kt", "lisp", "lua", "pde", "m", "php",
                               "py", "R", "rb", "rs", "rust", "sh", "scala", "swift", "ts", "vb"}
        self.default_comment = {"#", "//", "/*", "*", "*/", ":", ";", '""""'}
        self.default_ignore = {"out", "venv", ".git", ".idea", "build", "target", "node_modules", ".vscode", "dist"}

    @patch('builtins.input')
    def test_Config_restore(self, mock_input):
        mock_input.side_effect = ['y']

        options = ['python', app_path,
                   'config',
                   '--restore']
        sys.argv[1:] = options[2:]

        args = CodeCounterArgs()
        self.assertTrue(args.has_config_args())

        config = Config()
        config.invoke(args.config())

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

        args = CodeCounterArgs()
        self.assertTrue(args.has_config_args())
        config.invoke(args.config())

        suffix = {'java', 'cpp', 'go', 'js', 'py'}
        comment = {'//', '#', '/**'}
        ignore = {'target', 'build', 'node_modules', '__pycache__'}

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

        args = CodeCounterArgs()
        self.assertTrue(args.has_config_args())
        config.invoke(args.config())

        suffix = {'java', 'cpp', 'go', 'js', 'py'}
        comment = {'//', '#', '/**'}
        ignore = {'target', 'build', 'node_modules', '__pycache__'}

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

        args = CodeCounterArgs()
        self.assertTrue(args.has_config_args())
        config.invoke(args.config())

        suffix = {'java', 'cpp', 'go', 'js', 'py'}
        comment = {'//', '#', '/**'}
        ignore = {'target', 'build', 'node_modules', '__pycache__'}

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

        args = CodeCounterArgs()
        self.assertTrue(args.has_config_args())
        config.invoke(args.config())

        suffix = {'java', 'cpp', 'go', 'js', 'py'}
        comment = {'//', '#', '/**'}
        ignore = {'target', 'build', 'node_modules', '__pycache__'}

        self.assertEqual(config.suffix, suffix)
        self.assertEqual(config.comment, comment)
        self.assertEqual(config.ignore, self.default_ignore)

        config.restore()

    @patch('builtins.input')
    def test_Config_reset_duplicate(self, mock_input):
        mock_input.side_effect = ['y', 'y', 'y', 'y', 'y']

        config = Config()
        config.restore()

        options = ['python', app_path,
                   'config',
                   '--suffix-reset=py,py,py,py',
                   '--comment-reset=#,#,#',
                   '--ignore-reset=__pycache__,__pycache__']
        sys.argv[1:] = options[2:]

        args = CodeCounterArgs()
        self.assertTrue(args.has_config_args())
        config.invoke(args.config())

        suffix = {'py'}
        comment = {'#'}
        ignore = {'__pycache__'}

        self.assertEqual(len(config.suffix), 1)
        self.assertEqual(len(config.comment), 1)
        self.assertEqual(len(config.ignore), 1)

        self.assertEqual(config.suffix, suffix)
        self.assertEqual(config.comment, comment)
        self.assertEqual(config.ignore, ignore)

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

        args = CodeCounterArgs()
        self.assertTrue(args.has_config_args())
        config.invoke(args.config())

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

        args = CodeCounterArgs()
        self.assertTrue(args.has_config_args())
        config.invoke(args.config())

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

        args = CodeCounterArgs()
        self.assertTrue(args.has_config_args())
        config.invoke(args.config())

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

        args = CodeCounterArgs()
        self.assertTrue(args.has_config_args())
        config.invoke(args.config())

        suffix = 'TEST_SUFFIX'
        comment = 'TEST_COMMENT'
        ignore = 'TEST_IGNORE'

        self.assertTrue(suffix in config.suffix)
        self.assertTrue(comment in config.comment)
        self.assertTrue(ignore not in config.ignore)

        config.restore()
