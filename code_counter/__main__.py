#!/usr/bin/env python3
# coding:utf8

import time
from code_counter.core.counter import CodeCounter
from code_counter.core.args import CodeCounterArgs
from code_counter.conf.config import Config


def main():
    args = CodeCounterArgs()

    config = Config()
    if args.has_config_args():
        config.invoke(args.config())
        return

    code_counter = CodeCounter()

    search_args = args.search()
    code_counter.setSearchArgs(search_args)

    time_start = time.time()
    code_counter.search()
    time_end = time.time()

    print('\n\tTotally cost {} s.'.format(time_end - time_start))

    if search_args.graph:
        code_counter.visualize()


if __name__ == '__main__':
    main()
