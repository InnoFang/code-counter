#!/usr/bin/env python3
# coding:utf8

import os
import re
import time
import argparse
from collections import defaultdict
from config import config

total_file_lines = 0
total_code_lines = 0
total_blank_lines = 0
total_comment_lines = 0
files_of_language = defaultdict(int)
lines_of_language = {suffix: 0 for suffix in config['suffix']}

ignore = config['ignore']
comment_symbol = config['comment']
regex = '.*\.({})$'.format('|'.join(config['suffix']))
pattern = re.compile(regex)
result = {'total': {
    'code': '',
    'comment': '',
    'blank': '',
}, 'code': {}, 'file': {}}


def count(filename):
    """
    :param filename: the file you want to count
    :return: file line, code line, blank line, comment line
    """
    file_line = 0
    code_line = 0
    blank_line = 0
    comment_line = 0
    with open(filename, 'rb') as handle:
        for l in handle:
            try:
                line = l.strip().decode('utf8')
            except UnicodeDecodeError:
                # If the code line contain Chinese string, decode it as gbk
                line = l.strip().decode('gbk')

            file_line += 1
            if not line:
                blank_line += 1
            elif line.startswith(comment_symbol):
                comment_line += 1
            else:
                code_line += 1
    return file_line, code_line, blank_line, comment_line


def format_output(file_path, f):
    """
    :param file_path: file path
    :param f:  file
    :return:
    """
    global total_file_lines, total_code_lines, total_blank_lines, total_comment_lines
    try:
        res = re.match(pattern, file_path)
        if res:
            file_lines, code_lines, blank_lines, comment_lines = count(file_path)
            file_type = os.path.splitext(file_path)[1][1:]
            files_of_language[file_type] += 1
            print('\t{:>10}  |{:>10}  |{:>10}  |{:>10}  |{:>10}  |  {}'
                  .format(file_type, file_lines, code_lines, blank_lines, comment_lines, file_path), file=f)
            total_file_lines += file_lines
            total_code_lines += code_lines
            total_blank_lines += blank_lines
            total_comment_lines += comment_lines
            lines_of_language[file_type] += code_lines
    except AttributeError as e:
        print(e)


def search(p, f):
    """
    :param p: path
    :param f: file
    :return:
    """
    if os.path.isdir(p):
        files = os.listdir(p)
        for file in files:
            file_path = os.path.join(p, file)
            if os.path.isdir(file_path):
                if os.path.split(file_path)[-1] in ignore:
                    continue
                search(file_path, f)
            elif os.path:
                file_path = os.path.join(p, file)
                format_output(file_path, f)
    elif os.path.isfile(p):
        format_output(p, f)


def main(p, i, o=None):
    """
    :param p: path
    :param i: input file path
    :param o: output file path
    :return:
    """
    global total_file_lines, total_code_lines, total_blank_lines, total_comment_lines

    f = open(o, 'w') if o else None

    print('\n\t{}'.format("SEARCHING"), file=f)
    print("\t{}".format('=' * 20), file=f)
    print('\t{:>10}  |{:>10}  |{:>10}  |{:>10}  |{:>10}  |  {}'
          .format("File Type", "Lines", "Code", "Blank", "Comment", "File Path"), file=f)
    print("\t{}".format('-' * 90), file=f)

    if not p:
        with open(i) as file:
            for l in file.readlines():
                l_strip = l.strip()
                if os.path.exists(l_strip):
                    search(l_strip, f)
                else:
                    print('{} is not a validate path.'.format(l))
    elif os.path.isdir(p):
        search(p, f)
    elif os.path.isfile(p):
        if os.path.exists(p):
            search(p, f)
        else:
            print('{} is not a validate path.'.format(p))
            exit(0)
    else:
        print('{} is not a validate path.'.format(p))
        exit(0)

    print('\n\t{}'.format("RESULT"), file=f)
    print("\t{}".format('=' * 20), file=f)
    print("\t{:<20}:{:>8} ({:>7})"
          .format("Total file lines", total_file_lines, '100.00%'), file=f)
    print("\t{:<20}:{:>8} ({:>7})"
          .format("Total code lines",
                  total_code_lines, "%.2f%%" % (total_code_lines / total_file_lines * 100)), file=f)
    print("\t{:<20}:{:>8} ({:>7})"
          .format("Total blank lines",
                  total_blank_lines, "%.2f%%" % (total_blank_lines / total_file_lines * 100)), file=f)
    print("\t{:<20}:{:>8} ({:>7})"
          .format("Total comment lines",
                  total_comment_lines, "%.2f%%" % (total_comment_lines / total_file_lines * 100)), file=f)
    print(file=f)

    result['total']['code'] = total_code_lines
    result['total']['blank'] = total_blank_lines
    result['total']['comment'] = total_comment_lines

    total_files = 0

    for _, cnt in files_of_language.items():
        total_files += cnt

    print("\t{:>10}  |{:>10}  |{:>10}  |{:>10}  |{:>10}"
          .format("Type", "Files", 'Ratio', 'Codes', 'Ratio'), file=f)
    print("\t{}".format('-' * 65), file=f)

    for tp, cnt in files_of_language.items():
        code_line = lines_of_language[tp]
        print("\t{:>10}  |{:>10}  |{:>10}  |{:>10}  |{:>10}".format(
            tp, cnt, '%.2f%%' % (cnt / total_files * 100),
            code_line, '%.2f%%' % (code_line / total_code_lines * 100)), file=f)
        result['code'][tp] = code_line
        result['file'][tp] = cnt

    if f:
        f.close()


def visualize():
    from matplotlib import pyplot as plt
    from matplotlib import font_manager as fm
    from matplotlib import cm
    import numpy as np

    global result
    plt.figure('Visualization of Statistical Results', figsize=(15, 6))

    size = 0.3
    wedgeprops = dict(width=0.3, edgecolor='w')
    proptease = fm.FontProperties()

    plt.subplot(121)
    total_values = list(result['total'].values())
    total_keys = list(result['total'].keys())
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
    length = len(result['code'].values())
    colors = cm.rainbow(np.arange(length) / length)
    patches1, l_text1, p_text1 = plt.pie(list(result['code'].values()), labels=list(result['code'].keys()), autopct='%2.1f%%', radius=1,
            wedgeprops=wedgeprops, colors=colors, pctdistance=0.85, labeldistance=1.1)
    patches2, l_text2, p_text2 = plt.pie(list(result['file'].values()), labels=list(result['file'].keys()), autopct='%2.1f%%', radius=1-size,
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
    plt.legend(list(result['code'].keys()), title="Abbreviation", loc='best', bbox_to_anchor=(1.05, 1))
    plt.show()


def args_parser():
    parser = argparse.ArgumentParser(prog="code-counter", description="Let's get count your code")
    parser.add_argument('-i', '--input', dest='input',
                        help="the file contains a list of file path, "
                             "which can make you search more than one file or directory")
    parser.add_argument('-p', '--path', dest='path',
                        help="specify a file or directory path you want to search")
    parser.add_argument('-o', '--output', dest='output',
                        help="specify a output path if you want to store the result")
    parser.add_argument('-v', '--visual', dest='visual', action='store_true',
                        help="choose to whether to visualize the result")

    args = parser.parse_args()

    if not args.path and not args.input:
        print('\033[0;31;0m[ERROR] Please specify a input: specify [-p PATH] or [-i INPUT]\033[0m')
        print(parser.print_help())
        exit(0)

    if args.path and args.input:
        print('\033[0;33;0m[WARN] Specify one input is enough,'
              ' the option `[-p PATH]` will be cover the option `[-i INPUT]`\033[0m')

    return args.path, args.input, args.output, args.visual


if __name__ == '__main__':
    path, input_path, output_path, visual = args_parser()

    time_start = time.time()
    main(path, input_path, output_path)
    time_end = time.time()

    print('\n\tTotally cost {}s.'.format(time_end - time_start))

    if visual:
        visualize()
