#!/usr/bin/env python3
# coding:utf8

import time
from code_counter.core.codecounter import CodeCounter
from code_counter.core.argspaser import CodeCounterArgsParser
from code_counter.conf.config import Config


def main():
    parser = CodeCounterArgsParser()
    args = parser.args

    config = Config()
    if 'config' in parser.args:
        config.invoke(args['config'])
        return

    if 'search' not in parser.args:
        raise Exception('wrong subcommand, only `config` and `search` are supported!')

    code_counter = CodeCounter(config)

    search_args = args['search']
    code_counter.setSearchArgs(search_args)

    time_start = time.time()
    code_counter.search()
    time_end = time.time()

    print('\n\tTotally cost {} s.'.format(time_end - time_start))

    if search_args.graph:
        code_counter.visualize()


if __name__ == '__main__':
    main()
