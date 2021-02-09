#!/usr/bin/env python3
# coding:utf8
import os
import re
from collections import defaultdict

class CodeCounter:

    def __init__(self, config):
        self.total_file_lines = 0
        self.total_code_lines = 0
        self.total_blank_lines = 0
        self.total_comment_lines = 0
        self.files_of_language = defaultdict(int)
        self.lines_of_language = {suffix: 0 for suffix in config['suffix']}

        self.ignore = tuple(config['ignore'])
        self.comment_symbol = tuple(config['comment'])
        
        regex = '.*\.({})$'.format('|'.join(config['suffix']))
        self.pattern = re.compile(regex)
        self.result = {
            'total': {
                'code': 0,
                'comment': 0,
                'blank': 0,
            }, 
            'code': {}, 
            'file': {}
        }

        self.verbose = False


    def count(self, input_path, verbose=False, use_list=False, output_path=None):
        """
        :param input_path: path
        :param use_list: whether the path is the file that contains a list of file
        :param output_path: output file path
        :return:
        """
        self.verbose = verbose

        output_file = open(output_path, 'w') if output_path else None

        if self.verbose:
            print('\n\t{}'.format("SEARCHING"), file=output_file)
            print("\t{}".format('=' * 20), file=output_file)
            print('\t{:>10}  |{:>10}  |{:>10}  |{:>10}  |{:>10}  |  {}'
                .format("File Type", "Lines", "Code", "Blank", "Comment", "File Path"), file=output_file)
            print("\t{}".format('-' * 90), file=output_file)

        if use_list:
            with open(input_path) as file:
                for l in file.readlines():
                    l_strip = l.strip()
                    if os.path.exists(l_strip):
                        self.__search(l_strip, output_file)
                    else:
                        print('{} is not a validate path.'.format(l))
        elif os.path.isdir(input_path) or os.path.isfile(input_path) :
            self.__search(input_path, output_file)
        else:
            print('{} is not a validate path.'.format(input_path))
            return

        print('\n\t{}'.format("RESULT"), file=output_file)
        print("\t{}".format('=' * 20), file=output_file)
        print("\t{:<20}:{:>8} ({:>7})"
            .format("Total file lines", self.total_file_lines, '100.00%'), file=output_file)

        if self.total_file_lines == 0:
            return

        print("\t{:<20}:{:>8} ({:>7})"
            .format("Total code lines",
                    self.total_code_lines, "%.2f%%" % (self.total_code_lines / self.total_file_lines * 100)), file=output_file)
        print("\t{:<20}:{:>8} ({:>7})"
            .format("Total blank lines",
                    self.total_blank_lines, "%.2f%%" % (self.total_blank_lines / self.total_file_lines * 100)), file=output_file)
        print("\t{:<20}:{:>8} ({:>7})"
            .format("Total comment lines",
                    self.total_comment_lines, "%.2f%%" % (self.total_comment_lines / self.total_file_lines * 100)), file=output_file)
        print(file=output_file)

        self.result['total']['code'] = self.total_code_lines
        self.result['total']['blank'] = self.total_blank_lines
        self.result['total']['comment'] = self.total_comment_lines

        total_files = 0

        for _, cnt in self.files_of_language.items():
            total_files += cnt

        print("\t{:>10}  |{:>10}  |{:>10}  |{:>10}  |{:>10}"
            .format("Type", "Files", 'Ratio', 'Codes', 'Ratio'), file=output_file)
        print("\t{}".format('-' * 65), file=output_file)

        for tp, cnt in self.files_of_language.items():
            code_line = self.lines_of_language[tp]
            print("\t{:>10}  |{:>10}  |{:>10}  |{:>10}  |{:>10}".format(
                tp, cnt, '%.2f%%' % (cnt / total_files * 100),
                code_line, '%.2f%%' % (code_line / self.total_code_lines * 100)), file=output_file)
            self.result['code'][tp] = code_line
            self.result['file'][tp] = cnt

        if output_file:
            output_file.close()


    def __search(self, input_path, output_file=None):
        """
        :param input_path: path
        :param output_file: file
        :return:
        """
        if os.path.isdir(input_path):
            files = os.listdir(input_path)
            for file in files:
                file_path = os.path.join(input_path, file)
                if os.path.isdir(file_path):
                    if os.path.split(file_path)[-1] in self.ignore:
                        continue
                    self.__search(file_path, output_file)
                elif os.path:
                    file_path = os.path.join(input_path, file)
                    self.__format_output(file_path, output_file)
        elif os.path.isfile(input_path):
            self.__format_output(input_path, output_file)


    def __format_output(self, file_path, output_file):
        """
        :param file_path: file path
        :param output_file: file
        :return:
        """
        try:
            res = re.match(self.pattern, file_path)
            if res:
                single = self.count_single(file_path)
                file_lines = single['file_lines']
                code_lines = single['code_lines']
                blank_lines = single['blank_lines']
                comment_lines = single['comment_lines']

                file_type = os.path.splitext(file_path)[1][1:]
                self.files_of_language[file_type] += 1

                if self.verbose:
                    print('\t{:>10}  |{:>10}  |{:>10}  |{:>10}  |{:>10}  |  {}'
                        .format(file_type, file_lines, code_lines, blank_lines, comment_lines, file_path), file=output_file)

                self.total_file_lines += file_lines
                self.total_code_lines += code_lines
                self.total_blank_lines += blank_lines
                self.total_comment_lines += comment_lines
                self.lines_of_language[file_type] += code_lines
        except AttributeError as e:
            print(e)
    

    def count_single(self, file_path):
        """
        :param file_path: the file you want to count
        :return: single { file_lines, code_lines, blank_lines, comment_lines }
        """
        assert os.path.isfile(file_path), "Function: 'code_counter' need a file path, but {} is not.".format(file_path)

        single = {
            'file_lines' : 0,
            'code_lines' : 0,
            'blank_lines' : 0,
            'comment_lines' : 0,
        }
        with open(file_path, 'rb') as handle:
            for l in handle:
                try:
                    line = l.strip().decode('utf8')
                except UnicodeDecodeError:
                    # If the code line contain Chinese string, decode it as gbk
                    line = l.strip().decode('gbk')

                single['file_lines'] += 1
                if not line:
                    single['blank_lines'] += 1
                elif line.startswith(self.comment_symbol):
                    single['comment_lines'] += 1
                else:
                    single['code_lines'] += 1
        return single


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
        patches1, l_text1, p_text1 = plt.pie(list(self.result['code'].values()), labels=list(self.result['code'].keys()), autopct='%2.1f%%', radius=1,
                wedgeprops=wedgeprops, colors=colors, pctdistance=0.85, labeldistance=1.1)
        patches2, l_text2, p_text2 = plt.pie(list(self.result['file'].values()), labels=list(self.result['file'].keys()), autopct='%2.1f%%', radius=1-size,
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
        plt.title("Inner Pie: Code Files, Outer Pie: Code Type")
        plt.legend(list(self.result['code'].keys()), title="Abbreviation", loc='best', bbox_to_anchor=(1.05, 1))
        plt.show()

