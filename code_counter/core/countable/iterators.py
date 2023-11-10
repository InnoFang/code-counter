# !/usr/bin/env python3
# -*- coding: utf-8  -*-

import os
from abc import ABC, abstractmethod
from typing import Iterable, Iterator

from code_counter.tools import request
from code_counter.conf.config import Config
from code_counter.core.countable.file import CountableFile, RemoteCountableFile


class BaseCountableIterator(ABC):
    """Base iterator class for counting files.

    This class provides a common interface and functionality for iterating and counting files.
    Subclasses should implement the _generate_files method for specific file sources.

    Parameters
    ----------
    path: str
        The path or URL to the source of files

    """

    def __init__(self, path: str):
        self._ignore = Config().ignore
        self._suffix = Config().suffix
        self._path = path
        self._files: Iterator[CountableFile] = self._generate_files()

    # @abstractmethod
    # def iter(self, url_path):
    #     pass

    @abstractmethod
    def _generate_files(self) -> Iterator[CountableFile]:
        """
        Generate files to be iterated over. Subclasses should implement this method.

        Yields:
            Iterator[CountableFile]: An iterator of CountableFile objects.
        """
        pass

    def __iter__(self) -> Iterable[CountableFile]:
        return self

    def __next__(self) -> CountableFile:
        try:
            return next(self._files)
        except StopIteration:
            raise StopIteration


class LocalFileIterator(BaseCountableIterator):
    """
    Iterator for counting local files.

    This iterator is used to count local files and supports recursive directory traversal.

    Parameters
    ----------
    path :str
        The local directory path to start the iteration.
    """

    def __init__(self, path: str):
        super().__init__(path)

    def _generate_files(self) -> Iterator[CountableFile]:
        for root, dirs, files in os.walk(self._path):
            dirs[:] = [d for d in dirs if d not in self._ignore]
            for file in files:
                file_path = os.path.join(root, file)
                suffix = os.path.splitext(file)[1]
                if suffix and suffix[1:] in self._suffix:
                    yield CountableFile(file_path)

    @PendingDeprecationWarning
    def iter(self, path):
        if os.path.isdir(path):
            files = os.listdir(path)
            for file in files:
                file_path = os.path.join(path, file)
                if os.path.isdir(file_path):
                    if file in self._ignore:
                        continue
                    yield from self.iter(file_path)
                else:
                    suffix = os.path.splitext(file)[1]
                    if len(suffix) == 0 or suffix[1:] not in self._suffix:
                        continue
                    yield CountableFile(file_path)
        elif os.path.isfile(path):
            suffix = os.path.splitext(path)[1]
            if len(suffix) > 0 and suffix[1:] in self._suffix:
                yield CountableFile(path)


class RemoteFileIterator(BaseCountableIterator):
    """
    Iterator for counting remote files.

    This iterator is used to count files from a remote source, such as a GitHub or Gitee repository.
    It supports remote file retrieval from a project hosted on these platforms.

    Parameters
    ----------
    path : str
        The URL of the remote source (GitHub or Gitee repository) to start the iteration.
    """

    def __init__(self, path: str):
        super().__init__(path)

    def _generate_files(self) -> Iterator[CountableFile]:
        content = request.fetch(self._path, to_json=True)
        yield from self._generate_files_recursive(content)

    def _generate_files_recursive(self, content) -> Iterator[CountableFile]:
        for file_json in content:
            file_name = file_json.get('name')
            file_type = file_json.get('type')
            file_url = file_json.get('url')
            file_path = file_json.get('path')
            file_download_url = file_json.get('download_url')

            if file_name and file_type:
                if file_type == 'dir':
                    if file_name not in self._ignore:
                        yield from self._generate_files_recursive(request.fetch(file_url, to_json=True))
                else:
                    suffix = os.path.splitext(file_name)[1]
                    if len(suffix) == 0 or suffix[1:] not in self._suffix:
                        continue
                    yield RemoteCountableFile(file_download_url, file_path)

    @PendingDeprecationWarning
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
