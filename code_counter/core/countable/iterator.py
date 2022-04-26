# !/usr/bin/env python3
# -*- coding: utf-8  -*-

import os
from code_counter.core.countable.file import CountableFile
from code_counter.conf.config import Config


class CountableFileIterator:
    def __init__(self):
        self._ignore = Config().ignore
        self._suffix = Config().suffix

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
