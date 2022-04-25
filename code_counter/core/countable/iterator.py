from collections.abc import Iterator
import os
# !/usr/bin/env python3
# -*- coding: utf-8  -*-

from code_counter.core.countable.file import CountableFile
from code_counter.conf.config import Config
from collections import deque


class CountableFileIterator(Iterator):
    def __init__(self, path):
        self._ignore = Config().ignore
        self._suffix = Config().suffix
        self._file_queue = deque()
        self.__search(path)

    def __search(self, input_path):
        if os.path.isdir(input_path):
            files = os.listdir(input_path)
            for file in files:
                file_path = os.path.join(input_path, file)
                if os.path.isdir(file_path):
                    if file_path in self._ignore:
                        continue
                    self.__search(file_path)
                else:
                    suffix = os.path.splitext(file)[1]
                    if len(suffix) == 0 or suffix[1:] not in self._suffix:
                        continue
                    file_path = os.path.join(input_path, file)
                    self._file_queue.append(CountableFile(file_path))
        elif os.path.isfile(input_path):
            suffix = os.path.splitext(input_path)[1]
            if len(suffix) > 0 and suffix[1:] in self._suffix:
                self._file_queue.append(CountableFile(input_path))

    def __iter__(self):
        return self

    def __next__(self) -> CountableFile:
        if self._file_queue:
            fc = self._file_queue.popleft()
            return fc
        else:
            raise StopIteration
