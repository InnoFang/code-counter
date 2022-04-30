#!/usr/bin/env python3
# -*- coding: utf-8  -*-

import os
import asyncio
from collections import defaultdict
from code_counter.conf.config import Config
from code_counter.core.visualization import GraphVisualization
from code_counter.core.countable.iterator import CountableIterator, RemoteCountableIterator
from code_counter.tools.progress import SearchingProgressBar


class CodeCounter:
    def __init__(self):
        self.config = Config()

        self.total_file_lines = 0
        self.total_code_lines = 0
        self.total_blank_lines = 0
        self.total_comment_lines = 0
        self.files_of_language = defaultdict(int)
        self.lines_of_language = defaultdict(int)

        self.args = None

    def setArgs(self, args):
        self.args = args
        if args.suffix:
            self.config.suffix = set(args.suffix)
        if args.comment:
            self.config.comment = set(args.comment)
        if args.ignore:
            self.config.ignore = set(args.ignore)

    def search(self):
        if self.args is None:
            raise Exception('search_args is None, please invoke the `setArgs` function first.')

        input_path = self.args.input_path
        if not input_path:
            print('{} is not a validate path.'.format(input_path))
            return

        output_path = self.args.output_path
        output_file = open(output_path, 'w') if output_path else None

        if self.args.verbose:
            self.__print_searching_verbose_title(output_file)

        progress_bar = SearchingProgressBar()
        progress_bar.start()
        asyncio.run(self.__search(input_path, output_file))
        progress_bar.stop()
        progress_bar.join()

        self.__print_result_info(output_file)

        if output_file:
            output_file.close()

    async def __search(self, input_path, output_file):
        tasks = []
        if isinstance(input_path, list):
            for path in input_path:
                if os.path.exists(path):
                    for cf in CountableIterator().iter(path):
                        tasks.append(asyncio.create_task(self.__resolve_counting_file(cf, output_file)))
        else:
            for cf in RemoteCountableIterator().iter(input_path):
                tasks.append(asyncio.create_task(self.__resolve_counting_file(cf, output_file)))
        await asyncio.gather(*tasks)

    async def __resolve_counting_file(self, cf, output_file=None):
        await cf.count()
        if self.args.verbose:
            print(cf, file=output_file)
        self.files_of_language[cf.file_type] += 1
        self.total_file_lines += cf.file_lines
        self.total_code_lines += cf.code_lines
        self.total_blank_lines += cf.blank_lines
        self.total_comment_lines += cf.comment_lines
        self.lines_of_language[cf.file_type] += cf.code_lines

    def __print_searching_verbose_title(self, output_file=None):
        print('\n\t{}'.format("SEARCHING"), file=output_file)
        print("\t{}".format('=' * 20), file=output_file)
        print('\t{:>10}  |{:>10}  |{:>10}  |{:>10}  |{:>10}  |  {}'
              .format("File Type", "Lines", "Code", "Blank", "Comment", "File Path"), file=output_file)
        print("\t{}".format('-' * 90), file=output_file)

    def __print_result_info(self, output_file=None):
        print('\n\t{}'.format("RESULT"), file=output_file)
        print("\t{}".format('=' * 20), file=output_file)
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

        for tp, file_count in self.files_of_language.items():
            count_count = self.lines_of_language[tp]
            print("\t{:>10}  |{:>10}  |{:>10}  |{:>10}  |{:>10}".format(
                tp, file_count, '%.2f%%' % (file_count / total_files * 100),
                count_count, '%.2f%%' % (count_count / self.total_code_lines * 100)), file=output_file)

    def visualize(self):
        gv = GraphVisualization(
            total_code_lines=self.total_code_lines,
            total_blank_lines=self.total_blank_lines,
            total_comment_lines=self.total_comment_lines,
            files_of_language=self.files_of_language,
            lines_of_language=self.lines_of_language)
        gv.visualize()
