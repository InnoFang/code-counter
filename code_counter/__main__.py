#!/usr/bin/env python3
# -*- coding: utf-8  -*-
import os
from code_counter.conf.config import Config
from code_counter.core.counter import CodeCounter
from code_counter.core.args import CodeCounterArgs


def handle_config_command(config, args):
    # Handle configuration command
    config.invoke(args.config())


def handle_remote_args(config, cocnt_args):
    # Handle remote repository-related arguments
    args = cocnt_args.remote()
    if cocnt_args.is_gitee_repo() and not config.access_tokens.gitee:
        config.request_gitee_access_token()
    elif cocnt_args.is_github_repo() and not config.access_tokens.github:
        config.request_github_access_token()
    return args


def handle_search_args(config, cocnt_args):
    # Handle search-related arguments
    args = cocnt_args.search()
    return args


def main():
    cocnt_args = CodeCounterArgs()
    config = Config()

    # If configuration command is present, invoke and return
    if cocnt_args.has_config_args():
        handle_config_command(config, cocnt_args)
        return

    # If searching or processing a remote repository, check and request access tokens
    if cocnt_args.has_remote_args():
        args = handle_remote_args(config, cocnt_args)
    elif cocnt_args.has_search_args():
        args = handle_search_args(config, cocnt_args)
    else:
        raise Exception('Wrong command')

    code_counter = CodeCounter(args)
    code_counter.search()

    if args.output_path:
        print(f'Output saved to: {os.path.abspath(args.output_path)}')

    if args.graph:
        code_counter.visualize()


if __name__ == '__main__':
    main()
