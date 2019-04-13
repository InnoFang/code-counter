import os
import re
import sys
import time
import argparse
from collections import defaultdict
from config import config

total_file_lines = 0
total_code_lines = 0
total_space_lines = 0
files_of_language = defaultdict(int)
lines_of_language = {suffix: 0 for suffix in config['suffix']}

ignore = config['ignore']
regex = '.*\.({})$'.format('|'.join(config['suffix']))
pattern = re.compile(regex)


def countFileLines(filename):
    line_of_file = 0
    line_of_code = 0
    line_of_space = 0
    with open(filename, 'rb') as handle:
        for line in handle:
            line = line.strip()
            line_of_file += 1
            if not line:
                line_of_space += 1
            else:
                line_of_code += 1
    return line_of_file, line_of_code, line_of_space


def formatOutput(file):
    global total_file_lines, total_code_lines, total_space_lines
    file_path = os.path.join(path, file)
    try:
        res = re.match(pattern, file)
        if res:
            line_of_file, line_of_code, line_of_space = countFileLines(file_path)
            file_type = os.path.splitext(file)[1][1:]
            files_of_language[file_type] += 1
            print('{:>13}  |  {:>13}  |  {:>13}  |  {:>13}  |  {}'.format(file_type, line_of_file, line_of_code,
                                                                          line_of_space, file_path))
            total_file_lines += line_of_file
            total_code_lines += line_of_code
            total_space_lines += line_of_space
            lines_of_language[file_type] += line_of_code
    except AttributeError as e:
        print(e)


def listDir(path):
    if os.path.isdir(path):
        files = os.listdir(path)
        for file in files:
            file_path = os.path.join(path, file)
            if os.path.isdir(file_path):
                if os.path.split(file_path)[-1] in ignore:
                    continue
                listDir(file_path)
            elif os.path:
                formatOutput(file)
    elif os.path.isfile(path):
        formatOutput(path)


def search(path, input_path, output_path=None):
    global total_file_lines, total_code_lines, total_space_lines

    if not os.path.exists(input_path):
        print('{} is not exist, please create it and add some file path you want to count.'.format(input_path))
        exit(0)

    f = open(output_path, 'w')

    print('\n\t{}'.format("SEARCHING"))
    print("\t{}".format('=' * 20))
    print('{:>13}  |  {:>13}  |  {:>13}  |  {:>13}  |  {}'.format("File Type", "Line of File", "Code of File",
                                                                  "Space of File", "File Path"))
    print("\t{}".format('-' * 100))

    if not path:
        with open(input_path) as file:
            for l in file.readlines():
                l_strip = l.strip()
                if os.path.exists(l_strip):
                    listDir(l_strip)
                else:
                    print('{} is not a validate path.'.format(l))
    else:
        if os.path.exists(path):
            listDir(path)
        else:
            print('{} is not a validate path.'.format(path))
            exit(0)

    f.write('\n\t{}\n'.format("RESULT"))
    f.write("\t{}\n".format('=' * 20))
    f.write("\t{:^25}|{:^15}|{:^15}|{:^15}|{:^15}\n"
            .format("Item", "File Count", 'File Ratio', 'Code Count', 'Code Ratio'))
    f.write("\t{}\n".format('-' * 90))
    f.write("\t{:<25}|{:^15}|{:^15}|{:^15}|{:^15}\n"
            .format("Total line of files", '----', '----', total_file_lines, '100.00%'))
    f.write("\t{:<25}|{:^15}|{:^15}|{:^15}|{:^15}\n"
            .format("Total line of codes", '----', '----',
                    total_code_lines, "%.2f%%" % (total_code_lines / total_file_lines * 100)))
    f.write("\t{:<25}|{:^15}|{:^15}|{:^15}|{:^15}\n"
            .format("Total line of space", '----', '----',
                    total_space_lines, "%.2f%%" % (total_space_lines / total_file_lines * 100)))

    total_files = 0

    # py|java|c|cpp|js|pde|kt|dart
    for _, count in files_of_language.items():
        total_files += count

    for tp, count in files_of_language.items():
        code_line = lines_of_language[tp]
        f.write("\t{:<25}|{:^15}|{:^15}|{:^15}|{:^15}\n".format(
            "For '.%s' files" % tp, count, '%.2f%%' % (count / total_files * 100),
            code_line, '%.2f%%' % (code_line / total_code_lines * 100)))

    f.close()


def args_parser():
    parser = argparse.ArgumentParser(prog="code-counter", description="Let's get count your code")
    parser.add_argument('-i', '--input', dest='input',
                        help="the file contains a list of file path, "
                             "which can make you search more than one file or directory")
    parser.add_argument('-p', '--path', dest='path',
                        help="specify a file or directory path you want to search")
    parser.add_argument('-o', '--output', dest='output',
                        help="specify a output path if you want to store the result")

    args = parser.parse_args()

    if not args.path and not args.input:
        print('\033[0;31;0m[ERROR] Please specify a input: specify <--path> or <--input>\033[0m')
        print(parser.print_help())
        exit(0)

    if args.path and args.input:
        print('\033[0;33;0m[WARN] Specify one input is sufficient, the <--path> will be cover <--input>\033[0m')

    return args.path, args.input, args.output


if __name__ == '__main__':

    path, input_path, output_path = args_parser()

    time_start = time.time()
    search(path, input_path, output_path)
    time_end = time.time()

    with open(output_path) as f:
        for line in f:
            print(line, end='')

    print('\n\tTotally cost {}s.'.format(time_end - time_start))
