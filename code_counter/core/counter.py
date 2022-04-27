#!/usr/bin/env python3
# -*- coding: utf-8  -*-

import os
import asyncio
from collections import deque
from collections import defaultdict
from code_counter.conf.config import Config
from code_counter.core.countable.iterator import CountableIterator, RemoteCountableIterator


class CodeCounter:

    def __init__(self):
        self.config = Config()

        self.total_file_lines = 0
        self.total_code_lines = 0
        self.total_blank_lines = 0
        self.total_comment_lines = 0
        self.files_of_language = defaultdict(int)

        self.args = None
        self.lines_of_language = {}

        self.result = {
            'total': {
                'code': 0,
                'comment': 0,
                'blank': 0,
            },
            'code': {},
            'file': {}
        }

    def setArgs(self, args):
        self.args = args
        if args.suffix:
            self.config.suffix = set(args.suffix)
        if args.comment:
            self.config.comment = set(args.comment)
        if args.ignore:
            self.config.ignore = set(args.ignore)

        self.lines_of_language = {suffix: 0 for suffix in self.config.suffix}

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

        asyncio.run(self.__search(input_path, output_file))

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

        self.result['total']['code'] = self.total_code_lines
        self.result['total']['blank'] = self.total_blank_lines
        self.result['total']['comment'] = self.total_comment_lines

        total_files = 0

        for _, cnt in self.files_of_language.items():
            total_files += cnt

        print("\t{:>10}  |{:>10}  |{:>10}  |{:>10}  |{:>10}"
              .format("Type", "Files", 'Ratio', 'Lines', 'Ratio'), file=output_file)
        print("\t{}".format('-' * 65), file=output_file)

        for tp, cnt in self.files_of_language.items():
            code_line = self.lines_of_language[tp]
            self.result['code'][tp] = code_line
            self.result['file'][tp] = cnt
            print("\t{:>10}  |{:>10}  |{:>10}  |{:>10}  |{:>10}".format(
                tp, cnt, '%.2f%%' % (cnt / total_files * 100),
                code_line, '%.2f%%' % (code_line / self.total_code_lines * 100)), file=output_file)

    def visualize(self):
        from matplotlib import pyplot as plt
        from matplotlib import font_manager as fm
        from matplotlib import cm
        import numpy as np

        plt.figure('Visualization of Statistical Results', figsize=(15, 6))

        size = 0.3
        wedgeprops = dict(width=0.3, edgecolor='w')
        proptease = fm.FontProperties()

        plt.subplot(121)
        total_values = list(self.result['total'].values())
        total_keys = list(self.result['total'].keys())
        explode = np.array([0., 0., 0.])
        explode[total_keys.index('code')] = 0.05
        patches, l_text, p_text = plt.pie(total_values, labels=total_keys, autopct='%2.1f%%',
                                          explode=explode, startangle=90)
        proptease.set_size('x-large')
        plt.setp(l_text, fontproperties=proptease)
        plt.setp(p_text, fontproperties=proptease)
        plt.axis('equal')
        plt.title("Total Statistics")
        plt.legend(title="Index", loc='best', bbox_to_anchor=(0, 1))

        plt.subplot(122)
        length = len(self.result['code'].values())
        colors = cm.rainbow(np.arange(length) / length)
        patches1, l_text1, p_text1 = plt.pie(list(self.result['code'].values()),
                                             labels=list(self.result['code'].keys()), autopct='%2.1f%%', radius=1,
                                             wedgeprops=wedgeprops, colors=colors, pctdistance=0.85, labeldistance=1.1)
        patches2, l_text2, p_text2 = plt.pie(list(self.result['file'].values()),
                                             labels=list(self.result['file'].keys()), autopct='%2.1f%%',
                                             radius=1 - size,
                                             wedgeprops=wedgeprops, colors=colors, pctdistance=0.8, labeldistance=0.4)
        # font size include: ‘xx-small’,x-small’,'small’,'medium’,‘large’,‘x-large’,‘xx-large’ or number, e.g. '12'
        proptease.set_size('x-large')
        plt.setp(l_text1, fontproperties=proptease)
        proptease.set_size('large')
        plt.setp(p_text1, fontproperties=proptease)
        proptease.set_size('medium')
        plt.setp(p_text2, fontproperties=proptease)
        proptease.set_size('small')
        plt.setp(l_text2, fontproperties=proptease)
        plt.axis('equal')
        plt.title("Inner Pie: Code Files, Outer Pie: Code Lines")
        plt.legend(list(self.result['code'].keys()), title="Abbreviation", loc='best', bbox_to_anchor=(1.05, 1))
        plt.show()
