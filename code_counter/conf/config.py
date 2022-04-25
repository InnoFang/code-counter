#!/usr/bin/env python3
# coding:utf8

import json
import pkg_resources


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


class SingletonMeta(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instance[cls]


class Config(metaclass=SingletonMeta):
    def __init__(self):
        conf = self.__load()

        self.suffix: set = set(conf['suffix'])
        self.comment: set = set(conf['comment'])
        self.ignore: set = set(conf['ignore'])

    def invoke(self, args):
        if args.restore:
            self.restore()
        else:
            if any([args.suffix_reset, args.comment_reset, args.ignore_reset]):
                self.__reset_config(args.suffix_reset, args.comment_reset, args.ignore_reset)
            if any([args.suffix_add, args.comment_add, args.ignore_add]):
                self.__append_config(args.suffix_add, args.comment_add, args.ignore_add)
            if any([args.suffix_del, args.comment_del, args.ignore_del]):
                self.__remove_config(args.suffix_del, args.comment_del, args.ignore_del)
        if args.show_list:
            self.show()

    def show(self):
        print(json.dumps(self.__dict__, indent=4, cls=SetEncoder))

    def __confirm(self, tips):
        check = input(tips)
        return check.strip().lower() == 'y'

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
            json.dump(self.__dict__, config, indent=4, cls=SetEncoder)

    def restore(self):
        self.suffix = {"c", "cc", "clj", "cpp", "cs", "cu", "cuh", "dart", "go", "h", "hpp", "java", "jl", "js", "kt",
                       "lisp", "lua", "pde", "m", "php", "py", "R", "rb", "rs", "rust", "sh", "scala", "swift", "ts",
                       "vb"}
        self.comment = {"#", "//", "/*", "*", "*/", ":", ";", '""""'}
        self.ignore = {"out", "venv", ".git", ".idea", "build", "target", "node_modules", ".vscode", "dist"}

        if self.__confirm('The default configuration will be restored. (y/n) '):
            self.__update()
