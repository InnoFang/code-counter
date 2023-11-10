#!/usr/bin/env python3
# -*- coding: utf-8  -*-

import os
from typing import Optional, List
from code_counter.tools import request
from code_counter.conf.config import Config


class CountableFile:
    """
    Class for counting lines in a file.

    Parameters
    ----------
    file_path: str
        The file path to count.

    display_path: str, optional
        The display path (default is the same as file_path).

    Attributes
    ----------
    file_type: str
        The file suffix used for counting.

    file_lines: int
        The total number of lines in the file.

    code_lines: int
        The number of lines containing code in the file.

    blank_lines: int
        The number of blank lines in the file.

    comment_lines: int
        The number of lines containing comments in the file.
    """

    def __init__(self, file_path: str, display_path: Optional[str] = ''):
        self._file_path = file_path
        self._display_path = display_path or file_path
        self._format_output: List[str] = []
        self._comment_symbol = tuple(Config().comment)
        self._content: List[str] = []

        self.file_type: str = os.path.splitext(file_path)[1][1:]
        self.file_lines: int = 0
        self.code_lines: int = 0
        self.blank_lines: int = 0
        self.comment_lines: int = 0

    def file_content(self) -> List[str]:
        """
        Return the content of the file.

        If the content has not been read yet, it reads the content from the file identified by the self._file_path.

        Returns:
            List[str]: List of lines in the file.
        """
        if not self._content:
            self._read_file()
        return self._content

    def _read_file(self) -> None:
        try:
            with open(self._file_path, encoding="utf-8") as content:
                self._content = content.readlines()
        except UnicodeDecodeError:
            # If the code line contain Chinese string, decode it as gbk
            try:
                with open(self._file_path, encoding="gbk") as content:
                    self._content = content.readlines()
            except UnicodeDecodeError:
                self._handle_decode_error('', -1)

    async def count(self) -> None:
        """
        Count lines in the file and update the attributes.
        """
        result = self._count_lines()
        self.file_lines, self.code_lines, self.blank_lines, self.comment_lines = result

    def _count_lines(self) -> List[int]:
        single = [0, 0, 0, 0]  # [file_lines, code_lines, blank_lines, comment_lines]

        for line_number, raw_line in enumerate(self.file_content()):
            try:
                line = raw_line.strip()
            except UnicodeDecodeError:
                self._handle_decode_error(raw_line, line_number)
                continue

            single[0] += 1
            if not line:
                single[2] += 1
            elif line.startswith(tuple(self._comment_symbol)):
                single[3] += 1
            else:
                single[1] += 1

        return single

    def _handle_decode_error(self, raw_line: str, line_number: int) -> None:
        self._format_output.append(
            f'\n\t{"WARN":>10}  |  decode line occurs a problem, non-count it, at File "{self._display_path}", line {line_number}:')
        self._format_output.append(f'\t{" ":>10}  |  \t{raw_line}\n')

    def __str__(self) -> str:
        self._format_output.append(
            f'\t{self.file_type:>10}  |{self.file_lines:>10}  |{self.code_lines:>10}  |'
            f'{self.blank_lines:>10}  |{self.comment_lines:>10}  |  {self._display_path}')
        return '\n'.join(self._format_output)


class RemoteCountableFile(CountableFile):
    def __init__(self, file_path: str, display_path: Optional[str] = ''):
        super().__init__(file_path, display_path)

    def file_content(self) -> List[str]:
        """
        Fetch and return the content of the remote file.

        If the content has not been read yet, it fetches and read the content from the file identified by the URL path.

        Returns:
            List[str]: List of lines in the remote file.
        """
        if not self._content:
            self._content = self._fetch_file()
        return self._content

    def _fetch_file(self) -> List[str]:
        try:
            return request.fetch(self._file_path).split('\n')
        except Exception as e:
            self._handle_fetch_error(e)

    def _handle_fetch_error(self, exception: Exception) -> None:
        self._format_output.append(
            f'\n\t{"ERROR":>10}  |  error occurred while fetching remote file "{self._display_path}": {str(exception)}\n')
