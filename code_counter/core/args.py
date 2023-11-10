#!/usr/bin/env python3
# -*- coding: utf-8  -*-
"""
Command-line interface (CLI) utility for counting code lines and displaying detailed results.
"""

import re
import sys
import argparse
from typing import List, Optional
from code_counter import __version__


def split_args(args: str) -> List[str]:
    """
    Split input arguments separated by commas.

    Parameters
    ----------
    args: str
        Input arguments as a comma-separated string.

    Returns
    -------
    List[str]
        List of split arguments.
    """
    return list(args.split(','))


def parse_remote_repo(repo: str) -> str:
    """
    Parse the input repository link to extract information and construct API URL.

    Parameters
    ----------
    repo: str
        Input repository link.

    Returns
    -------
    str
        Constructed API URL for the repository.
    """
    # Check both HTTPS and SSH links for GitHub or Gitee repositories
    res = re.search(r"^(https|git)@(github|gitee).com:([^/]+)/([^\.]+)\.git$", repo, re.I)
    if not res:
        print('Remote repository link parse error! Please enter a valid HTTPS or SSH link:')
        print('\tcocnt remote', repo)
        exit(1)

    # Construct API URL based on the matched repository
    api_url = f'https://{res.group(2)}.com/api/v5/repos/{res.group(3)}/{res.group(4)}/contents/'
    return api_url


@PendingDeprecationWarning
def remote_repo_parse(repo: str) -> str:
    """
    Parse the input repository link and return the corresponding API URL.

    This function is deprecated in favor of `parse_remote_repo`.

    Parameters
    ----------
    repo: str
        Input repository link.

    Returns
    -------
    str
        Constructed API URL for the repository.
    """
    # check HTTPS link first
    res = re.search(r"^https://(github|gitee).com/([^/]+)/([^\.]+)\.git$", repo, re.I)
    # if got none, then check SSH link
    if not res:
        res = re.search(r"^git@(github|gitee).com:([^/]+)/([^\.]+)\.git$", repo, re.I)
    if not res:
        print('Remote repository link parse error! please enter a right HTTPS or SSH link:')
        print('\tcocnt remote', repo)
        exit(1)
    if res.group(1).lower() == 'github':
        # Github API
        return 'https://api.github.com/repos/{}/{}/contents/'.format(res.group(2), res.group(3))
    elif res.group(1).lower() == 'gitee':
        # Gitee API
        return 'https://gitee.com/api/v5/repos/{}/{}/contents/'.format(res.group(2), res.group(3))
    else:
        print('Remote repository link parse error! please enter a right HTTPS or SSH link:')
        print('\tcocnt remote', repo)
        exit(1)


class CodeCounterArgs:
    SEARCH = 'search'
    CONFIG = 'config'
    REMOTE = 'remote'

    def __init__(self):
        """
        Initialize CodeCounterArgs instance.
        """
        parser = argparse.ArgumentParser(
            prog="code-counter",
            description="A command-line interface (CLI) utility that counts code lines and displays detailed results.",
            usage="""cocnt <command> [<args>]
These are common Code-Counter commands used in various situations:
    search     Search and count code lines for the given path(s)
    remote     Search and count the remote repository
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

        self.__args = {args.command: argparse.Namespace()}
        getattr(self, args.command)()

    def has_search_args(self) -> bool:
        """
        Check if the instance has search-related arguments.

        Returns
        -------
        bool
            True if search-related arguments are present, False otherwise.
        """
        return self.SEARCH in self.__args

    def has_remote_args(self) -> bool:
        """
        Check if the instance has remote-related arguments.

        Returns
        -------
        bool
            True if remote-related arguments are present, False otherwise.
        """
        return self.REMOTE in self.__args

    def has_config_args(self) -> bool:
        """
        Check if the instance has config-related arguments.

        Returns
        -------
        bool
            True if config-related arguments are present, False otherwise.
        """
        return self.CONFIG in self.__args

    def is_github_repo(self) -> bool:
        """
        Check if the provided input is a GitHub repository.

        Returns
        -------
            bool
            True if the input is a GitHub repository, False otherwise.
        """
        return self.has_remote_args() \
            and self.__args[self.REMOTE].input_path.startswith('https://api.github.com/repos/')

    def is_gitee_repo(self) -> bool:
        """
        Check if the provided input is a Gitee repository.

        Returns
        -------
        bool
            True if the input is a Gitee repository, False otherwise.
        """
        return self.has_remote_args() \
            and self.__args[self.REMOTE].input_path.startswith('https://gitee.com/api/v5/repos/')

    def search(self) -> Optional[argparse.Namespace]:
        """
        Get search-related arguments.

        Returns
        -------
        Optional[argparse.Namespace]
            Search-related arguments if present, None otherwise.
        """
        if not self.has_search_args():
            return None
        if self.__args[self.SEARCH] == argparse.Namespace():
            self.__args[self.SEARCH] = self.__search()
        return self.__args[self.SEARCH]

    def remote(self) -> Optional[argparse.Namespace]:
        """
        Get remote-related arguments.

        Returns
        -------
        Optional[argparse.Namespace]
            Remote-related arguments if present, None otherwise.
        """
        if not self.has_remote_args():
            return None
        if self.__args[self.REMOTE] == argparse.Namespace():
            self.__args[self.REMOTE] = self.__remote()
        return self.__args[self.REMOTE]

    def config(self) -> Optional[argparse.Namespace]:
        """
        Get config-related arguments.

        Returns
        -------
        Optional[argparse.Namespace]
            Config-related arguments if present, None otherwise.
        """
        if not self.has_config_args():
            return None
        if self.__args[self.CONFIG] == argparse.Namespace():
            self.__args[self.CONFIG] = self.__config()
        return self.__args[self.CONFIG]

    def __search(self) -> argparse.Namespace:
        """
        Parse search-related arguments.

        Returns
        -------
        argparse.Namespace
            Search-related arguments.
        """
        parser = argparse.ArgumentParser(
            description="Search and count code lines for the given path(s)",
            usage="cocnt search input_path [-h] [-v] [-g] "
                  "[-o OUTPUT_PATH] [--suffix SUFFIX] [--comment COMMENT] [--ignore IGNORE]")
        parser.add_argument('input_path', metavar="paths", type=split_args,
                            help="counting the code lines according to the given path(s)")
        parser.add_argument('-v', '--verbose', dest="verbose", action='store_true',
                            help="show verbose information")
        parser.add_argument('-g', '--graph', dest='graph', action='store_true',
                            help="choose whether to visualize the result")
        parser.add_argument('-o', '--output', dest='output_path',
                            help="specify an output path if you want to store the result")
        parser.add_argument('--suffix', dest='suffix', type=split_args,
                            help="what code files do you want to count")
        parser.add_argument('--comment', dest='comment', type=split_args,
                            help="the comment symbol, which can be judged whether the current line is a comment")
        parser.add_argument('--ignore', dest='ignore', type=split_args,
                            help="ignore some directories or files that you don't want to count")
        return parser.parse_args(sys.argv[2:])

    def __remote(self) -> argparse.Namespace:
        """
        Parse remote-related arguments.

        Returns
        -------
        argparse.Namespace
            Remote-related arguments.
        """
        parser = argparse.ArgumentParser(
            description="Search and count the remote repository with a given GitHub or Gitee HTTP link",
            usage="cocnt remote <repository> [-h] [-v] [-g] "
                  "[-o OUTPUT_PATH] [--suffix SUFFIX] [--comment COMMENT] [--ignore IGNORE]")
        parser.add_argument('input_path', metavar="repository", type=parse_remote_repo,
                            help="search and count a remote repository")
        parser.add_argument('-v', '--verbose', dest="verbose", action='store_true',
                            help="show verbose information")
        parser.add_argument('-g', '--graph', dest='graph', action='store_true',
                            help="choose whether to visualize the result")
        parser.add_argument('-o', '--output', dest='output_path',
                            help="specify an output path if you want to store the result")
        parser.add_argument('--suffix', dest='suffix', type=split_args,
                            help="what code files do you want to count")
        parser.add_argument('--comment', dest='comment', type=split_args,
                            help="the comment symbol, which can be judged whether the current line is a comment")
        parser.add_argument('--ignore', dest='ignore', type=split_args,
                            help="ignore some directories or files that you don't want to count")
        return parser.parse_args(sys.argv[2:])

    def __config(self) -> argparse.Namespace:
        """
        Parse config-related arguments.

        Returns
        -------
        argparse.Namespace
            Config-related arguments.
        """
        parser = argparse.ArgumentParser(
            prog="code-counter",
            description="configure code-counter",
            usage="cocnt config [-h] [--list] [--suffix-reset SUFFIX_RESET] "
                  "[--suffix-add SUFFIX_ADD] [--comment-reset COMMENT_RESET] "
                  "[--comment-add COMMENT_ADD] [--ignore-reset IGNORE_RESET] "
                  "[--ignore-add IGNORE_ADD] [--restore] ")
        parser.add_argument('--list', dest='show_list', action='store_true',
                            help="list all variables set in the config file, along with their values")
        parser.add_argument('--suffix-reset', dest='suffix_reset', type=split_args,
                            help="reset the 'suffix' in the config and count code lines according to this value")
        parser.add_argument('--suffix-add', dest='suffix_add', type=split_args,
                            help="append new value for the 'suffix' in the config "
                                 "and count code lines according to this value")
        parser.add_argument('--suffix-del', dest='suffix_del', type=split_args,
                            help="delete some values of the 'suffix' in the config")

        parser.add_argument('--comment-reset', dest='comment_reset', type=split_args,
                            help="reset the 'comment' in the config and count comment lines according to this value")
        parser.add_argument('--comment-add', dest='comment_add', type=split_args,
                            help="append new value for the 'comment' in the config "
                                 "and count comment lines according to this value")
        parser.add_argument('--comment-del', dest='comment_del', type=split_args,
                            help="delete some values of the 'comment' in the config")

        parser.add_argument('--ignore-reset', dest='ignore_reset', type=split_args,
                            help="reset the 'ignore' in the config "
                                 "and ignore some files or directories according to this value")
        parser.add_argument('--ignore-add', dest='ignore_add', type=split_args,
                            help="append new value for the 'ignore' in the config "
                                 "and ignore some files or directories according to this value")
        parser.add_argument('--ignore-del', dest='ignore_del', type=split_args,
                            help="delete some values of the 'ignore' in the config")

        parser.add_argument('--github-token', dest='github_token',
                            help="update the GitHub access token")
        parser.add_argument('--gitee-token', dest='gitee_token',
                            help="update the Gitee access token")

        parser.add_argument('--restore', dest='restore', action='store_true',
                            help="restore default config")

        return parser.parse_args(sys.argv[2:])
