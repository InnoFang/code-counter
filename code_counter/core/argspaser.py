#!/usr/bin/env python3
# coding:utf8

import sys
import argparse
from code_counter import __version__


def split_args(args):
    return list(args.split(','))


class CodeCounterArgsParser:
    def __init__(self):
        parser = argparse.ArgumentParser(
            prog="code-counter",
            description="A command-line interface (CLI) utility "
                        "that can help you easily count code and display detailed results.",
            usage="""cocnt <command> [<args>]
These are common Code-Counter commands used in various situations:
    search     Search code in the given path(s)
    config     Configure Code-Counter
""")
        parser.add_argument('--version', action='version',
                            version='%(prog)s {}'.format(__version__))
        parser.add_argument("command", help="Subcommand to run, `search` or `config`")
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print("Unrecognized command")
            parser.print_help()
            exit(1)
        self.args = {args.command: getattr(self, args.command)()}

    def search(self):
        parser = argparse.ArgumentParser(
            description="Search code in the given path(s)",
            usage="cocnt search input_path [-h] [-v] [-g] "
                  "[-o OUTPUT_PATH] [--suffix SUFFIX] [--comment COMMENT] [--ignore IGNORE]")
        parser.add_argument('input_path', type=split_args,
                            help="counting the code lines according the given path(s)")
        parser.add_argument('-v', '--verbose', dest="verbose", action='store_true',
                            help="show verbose infomation")
        parser.add_argument('-g', '--graph', dest='graph', action='store_true',
                            help="choose to whether to visualize the result")
        parser.add_argument('-o', '--output', dest='output_path',
                            help="specify a output path if you want to store the result")
        parser.add_argument('--suffix', dest='suffix', type=split_args,
                            help="what code files do you want to count, this parameter is disposable")
        parser.add_argument('--comment', dest='comment', type=split_args,
                            help="the comment symbol, which can be judged whether the current line is a comment, "
                                 "this parameter is disposable")
        parser.add_argument('--ignore', dest='ignore', type=split_args,
                            help="ignore some directories or files that you don't want to count, "
                                 "this parameter is disposable")
        return parser.parse_args(sys.argv[2:])

    def config(self):
        parser = argparse.ArgumentParser(
            prog="code-counter",
            description="configure code-counter",
            usage="cocnt config [-h] [--list] [--suffix-reset SUFFIX_RESET] "
                  "[--suffix-add SUFFIX_ADD] [--comment-reset COMMENT_RESET] "
                  "[--comment-add COMMENT_ADD] [--ignore-reset IGNORE_RESET] "
                  "[--ignore-add IGNORE_ADD] [--restore] ")
        parser.add_argument('--list', dest='show_list', action='store_true',
                            help="list all variables set in config file, along with their values")
        parser.add_argument('--suffix-reset', dest='suffix_reset', type=split_args,
                            help="override 'suffix' in config and count codes according to this value")
        parser.add_argument('--suffix-add', dest='suffix_add', type=split_args,
                            help="append new value for 'suffix' in config and count codes according to this value")

        parser.add_argument('--comment-reset', dest='comment_reset', type=split_args,
                            help="override 'comment' in config and count comment lines according to this value")
        parser.add_argument('--comment-add', dest='comment_add', type=split_args,
                            help="append new value for 'comment' in config "
                                 "and count comment lines according to this value")

        parser.add_argument('--ignore-reset', dest='ignore_reset', type=split_args,
                            help="override 'ignore' in config "
                                 "and ignore some files or directory according to this value")
        parser.add_argument('--ignore-add', dest='ignore_add', type=split_args,
                            help="append new value for 'ignore' in config "
                                 "and ignore some files or directory according to this value")

        parser.add_argument('--restore', dest='restore', action='store_true',
                            help="restore default config")

        return parser.parse_args(sys.argv[2:])
