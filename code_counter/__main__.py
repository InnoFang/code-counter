#!/usr/bin/env python3
# -*- coding: utf-8  -*-

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
        if cocnt_args.is_gitee_repo() and not config.access_tokens.gitee:
            config.request_gitee_access_token()
        elif cocnt_args.is_github_repo() and not config.access_tokens.github:
            config.request_github_access_token()
    else:
        raise Exception('wrong command')

    code_counter.set_args(args)

    time_start = time.time()
    code_counter.search()
    time_end = time.time()

    print('\n\tTotally cost {} s.'.format(time_end - time_start))

    if args.graph:
        code_counter.visualize()


if __name__ == '__main__':
    main()
