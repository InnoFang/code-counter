#!/usr/bin/env python3
# -*- coding: utf-8  -*-

import os
import argparse
import asyncio
from collections import defaultdict
from typing import List, Optional, DefaultDict

from code_counter.conf.config import Config
from code_counter.core.vis import GraphVisualization
from code_counter.core.countable.file import CountableFile
from code_counter.core.countable.iterators import LocalFileIterator, RemoteFileIterator
from code_counter.tools.progress import SearchingProgressBar
from code_counter.tools.timing import timing_decorator


class CodeCounter:
    """
   Class for counting lines in code files.

   Parameters
   ----------
   args: argparse.Namespace
        A namespace containing command-line arguments for performing search operation.

   Attributes
   ----------
   total_file_lines: int
       The total number of lines in all processed files.

   total_code_lines: int
       The total number of lines containing code in all processed files.

   total_blank_lines: int
       The total number of blank lines in all processed files.

   total_comment_lines: int
       The total number of lines containing comments in all processed files.

   files_of_language: DefaultDict[str, int]
       A dictionary storing the count of files for each code language.

   lines_of_language: DefaultDict[str, int]
       A dictionary storing the count of lines for each code language.
   """

    def __init__(self, args: argparse.Namespace):
        self._args: argparse.Namespace = args
        self._config: Config = Config()

        self.total_file_lines: int = 0
        self.total_code_lines: int = 0
        self.total_blank_lines: int = 0
        self.total_comment_lines: int = 0
        self.files_of_language: DefaultDict[str, int] = defaultdict(int)
        self.lines_of_language: DefaultDict[str, int] = defaultdict(int)

        self.__update_configuration()

    @timing_decorator
    def search(self) -> None:
        """
        Search for code files in the specified input path and perform code counting.
        """
        if self._args is None:
            raise Exception('search_args is None, please invoke the `setArgs` function first.')

        input_path: str = self._args.input_path
        if not input_path:
            print(f'{input_path} is not a validate path.')
            return

        output_path: str = self._args.output_path
        output_file = open(output_path, 'w') if output_path else None

        if self._args.verbose:
            self.__print_searching_verbose_title(output_file)

        SearchingProgressBar().start()
        asyncio.run(self.__search(input_path, output_file))
        SearchingProgressBar().stop()

        self.__print_result_info(output_file)

        if output_file:
            output_file.close()

    def __update_configuration(self) -> None:
        """
        Update configuration for code counter according to the self._args.
        """
        args = self._args
        if args.suffix:
            self._config.suffix = set(args.suffix)
        if args.comment:
            self._config.comment = set(args.comment)
        if args.ignore:
            self._config.ignore = set(args.ignore)

    async def __search(self, input_path: str, output_file: Optional[str] = None) -> None:
        """
        Asynchronously search for code files in the specified input path and perform code counting.

        Parameters
        ----------
        input_path: str
            Input path where code files are searched.

        output_file: str
            Optional output file to write verbose results.
        """
        tasks: List[asyncio.Task] = []
        if isinstance(input_path, list):
            for path in input_path:
                if os.path.exists(path):
                    for cf in LocalFileIterator(path):
                        tasks.append(asyncio.create_task(self.__resolve_counting_file(cf, output_file)))
        else:
            for cf in RemoteFileIterator(input_path):
                tasks.append(asyncio.create_task(self.__resolve_counting_file(cf, output_file)))
        await asyncio.gather(*tasks)

    async def __resolve_counting_file(self, cf: CountableFile, output_file: Optional[str] = None) -> None:
        """
        Asynchronously resolve and count a code file.

        Parameters
        ----------
        cf: CountableFile.
            CountableFile instance.

        output_file: Optional[str]
            Optional output file to write verbose results.
        """
        await cf.count()
        if self._args.verbose:
            print(cf, file=output_file)
        self.files_of_language[cf.file_type] += 1
        self.total_file_lines += cf.file_lines
        self.total_code_lines += cf.code_lines
        self.total_blank_lines += cf.blank_lines
        self.total_comment_lines += cf.comment_lines
        self.lines_of_language[cf.file_type] += cf.code_lines

    def __print_searching_verbose_title(self, output_file: Optional[str] = None):
        print('\n\tSEARCHING', file=output_file)
        print("\t" + ("=" * 20), file=output_file)
        print('\t{:>10}  |{:>10}  |{:>10}  |{:>10}  |{:>10}  |  {}'
              .format("File Type", "Lines", "Code", "Blank", "Comment", "File Path"), file=output_file)
        print("\t" + ("-" * 90), file=output_file)

    def __print_result_info(self, output_file: Optional[str] = None):
        print('\n\tRESULT', file=output_file)
        print("\t" + ("=" * 20), file=output_file)
        print("\t{:<20}:{:>8} ({:>7})"
              .format("Total file lines", self.total_file_lines, '100.00%'), file=output_file)

        if self.total_file_lines == 0:
            return

        print("\t{:<20}:{:>8} ({:>7})"
              .format("Total code lines",
                      self.total_code_lines, "%.2f%%" % (self.total_code_lines / self.total_file_lines * 100)),
              file=output_file)
        print("\t{:<20}:{:>8} ({:>7})"
              .format("Total blank lines",
                      self.total_blank_lines, "%.2f%%" % (self.total_blank_lines / self.total_file_lines * 100)),
              file=output_file)
        print("\t{:<20}:{:>8} ({:>7})"
              .format("Total comment lines",
                      self.total_comment_lines, "%.2f%%" % (self.total_comment_lines / self.total_file_lines * 100)),
              file=output_file)
        print(file=output_file)

        total_files = sum(self.files_of_language.values())

        print("\t{:>10}  |{:>10}  |{:>10}  |{:>10}  |{:>10}"
              .format("Type", "Files", 'Ratio', 'Lines', 'Ratio'), file=output_file)
        print("\t{}".format('-' * 65), file=output_file)

        result_list = [(tp, file_count, self.lines_of_language[tp])
                       for tp, file_count in self.files_of_language.items()]

        result_list.sort(key=lambda x: (-x[2], -x[1]))  # priority: code_cont > file_count, descend

        for tp, file_count, code_count in result_list:
            print("\t{:>10}  |{:>10}  |{:>10}  |{:>10}  |{:>10}".format(
                tp, file_count, '%.2f%%' % (file_count / total_files * 100),
                code_count, '%.2f%%' % (code_count / self.total_code_lines * 100)), file=output_file)


    def visualize(self) -> None:
        """
        Visualize the code counting results and display graphical information.
        """
        gv = GraphVisualization(
            total_code_lines=self.total_code_lines,
            total_blank_lines=self.total_blank_lines,
            total_comment_lines=self.total_comment_lines,
            files_of_language=self.files_of_language,
            lines_of_language=self.lines_of_language)
        gv.visualize()
