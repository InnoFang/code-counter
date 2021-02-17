#!/usr/bin/env python3
# coding:utf8

import sys
import time
import argparse
from core.codecounter import CodeCounter
from conf.config import Config
from code_counter import __version__

def args_parser():
    parser = argparse.ArgumentParser(prog="code-counter", 
                        description="A command-line interface (CLI) utility that can help you easily count code and display detailed results.")

    parser.add_argument('-V', '--version', action='version', version='%(prog)s {}'.format(__version__))

    parser.add_argument('path', metavar='[path, CONFIG]',
                        help="specify a file or directory path you want to count or use CONFIG placeholder to configure")
    parser.add_argument('-l', '--list', dest='use_list', action='store_true',
                        help="the file contains a list of file path, which can make you search more than one file or directory")
    parser.add_argument('-v', '--verbose', dest="verbose", action='store_true',
                        help="show verbose infomation")
    parser.add_argument('-g', '--graph', dest='graph', action='store_true',
                        help="choose to whether to visualize the result")
    parser.add_argument('-o', '--output', dest='output_path', metavar='OUTPUT',
                        help="specify a output path if you want to store the result")

    # Configure arguments
    config_args_type = lambda args: list(args.split(','))

    # suffix = parser.add_mutually_exclusive_group()
    parser.add_argument('--suffix', dest='suffix', type=config_args_type,
                        help="")
    parser.add_argument('--suffix-save', dest='suffix_save', type=config_args_type,
                        help="")
    parser.add_argument('--suffix-add', dest='suffix_add', type=config_args_type,
                        help="")

    # comment = parser.add_mutually_exclusive_group()
    parser.add_argument('--comment', dest='comment', type=config_args_type,
                        help="")
    parser.add_argument('--comment-save', dest='comment_save', type=config_args_type,
                        help="")
    parser.add_argument('--comment-add', dest='comment_add', type=config_args_type,
                        help="")

    # ignore = parser.add_mutually_exclusive_group()
    parser.add_argument('--ignore', dest='ignore', type=config_args_type,
                        help="")
    parser.add_argument('--ignore-save', dest='ignore_save', type=config_args_type,
                        help="")
    parser.add_argument('--ignore-add', dest='ignore_add', type=config_args_type,
                        help="")

    parser.add_argument('--restore', dest='restore', action='store_true',
                        help="restore default config")
    
    return parser.parse_args()

def main():
    args = args_parser()
    
    config = Config(args)

    if args.path == 'CONFIG':
        config.show()
        sys.exit(0)
    
    code_counter = CodeCounter(config)

    time_start = time.time()
    code_counter.count(args.path, args.verbose, args.use_list, args.output_path)
    time_end = time.time()

    print('\n\tTotally cost {}s.'.format(time_end - time_start))

    if args.graph:
        code_counter.visualize()

if __name__ == '__main__':
    main()
    

