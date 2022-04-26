#!/usr/bin/env python3
# coding:utf8

import time
from code_counter.core.counter import CodeCounter
from code_counter.core.args import CodeCounterArgs
from code_counter.conf.config import Config


def main():
    cocnt_args = CodeCounterArgs()

    config = Config()
    if cocnt_args.has_config_args():
        config.invoke(cocnt_args.config())
        return

    code_counter = CodeCounter()

    if cocnt_args.has_search_args():
        args = cocnt_args.search()
    elif cocnt_args.has_remote_args():
        args = cocnt_args.remote()
    else:
        raise Exception('wrong command')

    code_counter.setArgs(args)

    time_start = time.time()
    code_counter.search()
    time_end = time.time()

    print('\n\tTotally cost {} s.'.format(time_end - time_start))

    if args.graph:
        code_counter.visualize()


if __name__ == '__main__':
    main()
