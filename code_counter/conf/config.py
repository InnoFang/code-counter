#!/usr/bin/env python3
# -*- coding: utf-8  -*-

import json
import pkg_resources
from code_counter.tools import singleton


class ConfigEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, Config.AccessTokens):
            return obj.__dict__
        return json.JSONEncoder.default(self, obj)


class Config(metaclass=singleton.SingletonMeta):
    class AccessTokens:
        def __init__(self, github='', gitee=''):
            self.github = github
            self.gitee = gitee

    def __init__(self):
        conf = self.__load()

        self.suffix = set(conf['suffix'])
        self.comment = set(conf['comment'])
        self.ignore = set(conf['ignore'])

        self.access_tokens = self.AccessTokens(github=conf['access_tokens']['github'],
                                               gitee=conf['access_tokens']['gitee'])

    def invoke(self, args):
        if args.restore:
            self.restore()
        else:
            if any([args.github_token, args.gitee_token]):
                self.__update_access_token(args.github_token, args.gitee_token)
            if any([args.suffix_reset, args.comment_reset, args.ignore_reset]):
                self.__reset_config(args.suffix_reset, args.comment_reset, args.ignore_reset)
            if any([args.suffix_add, args.comment_add, args.ignore_add]):
                self.__append_config(args.suffix_add, args.comment_add, args.ignore_add)
            if any([args.suffix_del, args.comment_del, args.ignore_del]):
                self.__remove_config(args.suffix_del, args.comment_del, args.ignore_del)
        if args.show_list:
            self.show()

    def show(self):
        print(json.dumps(self.__dict__, indent=4, cls=ConfigEncoder))

    def __confirm(self, tips):
        check = input(tips)
        return check.strip().lower() == 'y'

    def __update_access_token(self, github_access_token, gitee_access_token):
        if github_access_token:
            if self.__confirm(
                    "the old Github access token will be updated to `{}` . (y/n) ".format(github_access_token)):
                self.access_tokens.github = github_access_token
        if gitee_access_token:
            if self.__confirm("the old Gitee access token will be updated to `{}` . (y/n) ".format(gitee_access_token)):
                self.access_tokens.gitee = gitee_access_token

        self.__update()

    def __reset_config(self, suffix_reset, comment_reset, ignore_reset):
        if suffix_reset:
            if self.__confirm("'suffix' will be replaced with {} . (y/n) ".format(suffix_reset)):
                self.suffix = set(suffix_reset)
        if comment_reset:
            if self.__confirm("'comment' will be replaced with {} . (y/n) ".format(comment_reset)):
                self.comment = set(comment_reset)
        if ignore_reset:
            if self.__confirm("'ignore' will be replaced with {} . (y/n) ".format(ignore_reset)):
                self.ignore = set(ignore_reset)

        self.__update()

    def __append_config(self, suffix_add, comment_add, ignore_add):
        if suffix_add:
            if self.__confirm("'suffix' will be appended with {} . (y/n) ".format(suffix_add)):
                self.suffix.update(suffix_add)
        if comment_add:
            if self.__confirm("'comment' will be appended with {} . (y/n) ".format(comment_add)):
                self.comment.update(comment_add)
        if ignore_add:
            if self.__confirm("'ignore' will be appended with {} . (y/n) ".format(ignore_add)):
                self.ignore.update(ignore_add)

        self.__update()

    def __remove_config(self, suffix_del, comment_del, ignore_del):
        if suffix_del:
            if self.__confirm("'suffix' will remove {} . (y/n) ".format(suffix_del)):
                self.suffix.difference_update(suffix_del)
        if comment_del:
            if self.__confirm("'comment' will remove {} . (y/n) ".format(comment_del)):
                self.comment.difference_update(comment_del)
        if ignore_del:
            if self.__confirm("'ignore' will remove {} . (y/n) ".format(ignore_del)):
                self.ignore.difference_update(ignore_del)

        self.__update()

    def __load(self):
        filename = pkg_resources.resource_filename(__name__, 'config.json')
        with open(filename, 'r') as config:
            conf = json.load(config)
        return conf

    def __update(self):
        filename = pkg_resources.resource_filename(__name__, 'config.json')
        with open(filename, 'w') as config:
            json.dump(self.__dict__, config, indent=4, cls=ConfigEncoder)

    def request_github_access_token(self):
        if not self.access_tokens.github:
            print("\nThe Github access token is empty. In this case, your usage times will be limited by Github. "
                  "You can change this situation by setting access token. ")
        print("\nRequest a Github access token from https://github.com/settings/tokens/new .")
        print("`code-counter` require access to the public repositories .")
        print("Choose the `public_repo` in `Select scopes`, and click the `Generate token` to generate a token, "
              "then copy the access token and paste it here.")

        access_token = input('\nthe Github access token: \n')
        access_token = access_token.strip()
        if access_token:
            self.access_tokens.github = access_token
            self.__update()
            print('======================\n')
            return True
        print('\nNo access token obtained!')
        print('======================\n')
        return False

    def request_gitee_access_token(self):
        if not self.access_tokens.gitee:
            print("\nThe Gitee access token is empty. In this case, your usage times will be limited by Gitee. "
                  "You can change this situation by setting access token. ")
        print("\nRequest a Gitee access token from https://gitee.com/profile/personal_access_tokens/new .")
        print("`code-counter` require access to the public repositories.")
        print("Only need to choose the `projects`, and click the `submit` to generate a token, "
              "then copy the access token and paste it here.")

        access_token = input('\nthe Gitee access token: \n')
        access_token = access_token.strip()
        if access_token:
            self.access_tokens.gitee = access_token
            self.__update()
            print('======================\n')
            return True
        print('\nNo access token obtained!')
        print('======================\n')
        return False

    def restore(self):
        self.suffix = {"asm", "c", "cc", "clj", "cpp", "cs", "cu", "cuh", "dart", "go", "h", "hpp", "java", "jl", "js",
                       "kt", "lisp", "lua", "pde", "m", "php", "py", "r", "rb", "rs", "sh", "scala", "swift", "ts",
                       "vb"}
        self.comment = {"#", "//", "/*", "*", ":", ";", '--', ';', '%', "'"}
        self.ignore = {"venv", ".git", ".idea", "build", "target", "node_modules", ".vscode", "dist"}

        if self.__confirm('The default configuration will be restored. (y/n) '):
            self.__update()
