#!/usr/bin/env python3
# -*- coding: utf-8  -*-

import os
from code_counter.tools import request
from code_counter.conf.config import Config


class CountableFile:
    def __init__(self, url_path, path=''):
        """
        :param url_path: use to search
        :param path: default value is equal to url_path, use to display
        """
        self._url_path = url_path
        self._path = path if path else url_path
        self._format_output = []
        self._comment_symbol = tuple(Config().comment)

        self.file_type = os.path.splitext(url_path)[1][1:]
        self.file_lines = 0
        self.code_lines = 0
        self.blank_lines = 0
        self.comment_lines = 0

    def file_content(self):
        try:
            with open(self._url_path, encoding="utf-8") as content:
                return content.readlines()
        except UnicodeDecodeError:
            # If the code line contain Chinese string, decode it as gbk
            try:
                with open(self._url_path, encoding="gbk") as content:
                    return content.readlines()
            except UnicodeDecodeError:
                self._format_output.append(
                    '\n\t{:>10}  |  decode file occurs a problem, non-count it, at File "{}"\n'.format(
                        'WARN', self._path))
                return ''

    async def count(self):
        single = {
            'file_lines': 0,
            'code_lines': 0,
            'blank_lines': 0,
            'comment_lines': 0,
        }

        for line_number, raw_line in enumerate(self.file_content()):
            try:
                line = raw_line.strip()
            except UnicodeDecodeError:
                self._format_output.append(
                    '\n\t{:>10}  |  decode line occurs a problem, non-count it, at File "{}", line {}:'.format(
                        'WARN', self._path, line_number))
                self._format_output.append('\t{:>10}  |      {}\n'.format(' ', raw_line))
                continue

            single['file_lines'] += 1
            if not line:
                single['blank_lines'] += 1
            elif line.startswith(tuple(self._comment_symbol)):
                single['comment_lines'] += 1
            else:
                single['code_lines'] += 1

        self.file_lines = single['file_lines']
        self.code_lines = single['code_lines']
        self.blank_lines = single['blank_lines']
        self.comment_lines = single['comment_lines']

    def __str__(self):
        self._format_output.append(
            '\t{:>10}  |{:>10}  |{:>10}  |{:>10}  |{:>10}  |  {}'.format(self.file_type, self.file_lines,
                                                                         self.code_lines, self.blank_lines,
                                                                         self.comment_lines,
                                                                         self._path))
        return '\n'.join(self._format_output)


class RemoteCountableFile(CountableFile):
    def __init__(self, url_path, path=''):
        super().__init__(url_path, path)

    def file_content(self):
        return request.fetch(self._url_path).split('\n')
