#!/usr/bin/env python3
# coding:utf8

import time
import argparse
import json
from code_counter import CodeCounter

def args_parser():
    parser = argparse.ArgumentParser(prog="code-counter", description="Let's get count your code")
    
    parser.add_argument('path', help="specify a file or directory path you want to search")
    parser.add_argument('-l', '--list', dest='use_list', action='store_true',
                        help="the file contains a list of file path, "
                             "which can make you search more than one file or directory")
    parser.add_argument('-v', '--visual', dest='visual', action='store_true',
                        help="choose to whether to visualize the result")
    parser.add_argument('-o', '--output', dest='output_path',
                        help="specify a output path if you want to store the result")

    return parser.parse_args()


if __name__ == '__main__':

    args = args_parser()

    with open('./config.json', 'r') as config:
        config = json.load(config)

    code_counter = CodeCounter(config)

    time_start = time.time()
    code_counter.count(args.path, args.use_list, args.output_path)
    time_end = time.time()

    print('\n\tTotally cost {}s.'.format(time_end - time_start))

    if args.visual:
        code_counter.visualize()

