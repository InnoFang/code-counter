# !/usr/bin/env python3
# -*- coding: utf-8  -*-

import os
from code_counter.tools import request
from code_counter.core.countable.file import CountableFile, RemoteCountableFile
from code_counter.conf.config import Config
from abc import abstractmethod


class Iterator:
    def __init__(self):
        self._ignore = Config().ignore
        self._suffix = Config().suffix

    @abstractmethod
    def iter(self, url_path):
        pass


class CountableIterator(Iterator):
    def iter(self, input_path):
        if os.path.isdir(input_path):
            files = os.listdir(input_path)
            for file in files:
                file_path = os.path.join(input_path, file)
                if os.path.isdir(file_path):
                    if file in self._ignore:
                        continue
                    yield from self.iter(file_path)
                else:
                    suffix = os.path.splitext(file)[1]
                    if len(suffix) == 0 or suffix[1:] not in self._suffix:
                        continue
                    yield CountableFile(file_path)
        elif os.path.isfile(input_path):
            suffix = os.path.splitext(input_path)[1]
            if len(suffix) > 0 and suffix[1:] in self._suffix:
                yield CountableFile(input_path)


class RemoteCountableIterator(Iterator):
    def iter(self, url):
        content = request.fetch(url, to_json=True)

        for file_json in content:
            file_name = file_json['name']
            if file_json['type'] == 'dir':
                if file_name in self._ignore:
                    continue
                yield from self.iter(file_json['url'])
            else:
                suffix = os.path.splitext(file_name)[1]
                if len(suffix) == 0 or suffix[1:] not in self._suffix:
                    continue
                yield RemoteCountableFile(file_json['download_url'], file_json['path'])
