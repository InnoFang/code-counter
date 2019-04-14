import os
import re
import time
import argparse
from collections import defaultdict
from config import config

total_file_lines = 0
total_code_lines = 0
total_blank_lines = 0
files_of_language = defaultdict(int)
lines_of_language = {suffix: 0 for suffix in config['suffix']}

ignore = config['ignore']
regex = '.*\.({})$'.format('|'.join(config['suffix']))
pattern = re.compile(regex)


def countFileLines(filename):
    line_of_file = 0
    line_of_code = 0
    line_of_blank = 0
    with open(filename, 'rb') as handle:
        for l in handle:
            l_strip = l.strip()
            line_of_file += 1
            if not l_strip:
                line_of_blank += 1
            else:
                line_of_code += 1
    return line_of_file, line_of_code, line_of_blank


def formatOutput(file_path, f):
    global total_file_lines, total_code_lines, total_blank_lines
    try:
        res = re.match(pattern, file_path)
        if res:
            line_of_file, line_of_code, line_of_blank = countFileLines(file_path)
            file_type = os.path.splitext(file_path)[1][1:]
            files_of_language[file_type] += 1
            print('\t{:>10}  |  {:>13}  |  {:>13}  |  {:>13}  |  {}'.format(file_type, line_of_file, line_of_code,
                                                                          line_of_blank, file_path), file=f)
            total_file_lines += line_of_file
            total_code_lines += line_of_code
            total_blank_lines += line_of_blank
            lines_of_language[file_type] += line_of_code
    except AttributeError as e:
        print(e)


def listDir(path, f):
    if os.path.isdir(path):
        files = os.listdir(path)
        for file in files:
            file_path = os.path.join(path, file)
            if os.path.isdir(file_path):
                if os.path.split(file_path)[-1] in ignore:
                    continue
                listDir(file_path, f)
            elif os.path:
                file_path = os.path.join(path, file)
                formatOutput(file_path, f)
    elif os.path.isfile(path):
        formatOutput(path, f)


def search(path, input_path, output_path=None):
    global total_file_lines, total_code_lines, total_blank_lines

    f = open(output_path, 'w') if output_path else None

    print('\n\t{}'.format("SEARCHING"), file=f)
    print("\t{}".format('=' * 20), file=f)
    print('\t{:>10}  |  {:>13}  |  {:>13}  |  {:>13}  |  {}'.format("File Type", "Line of File", "Code of File",
                                                                  "Blank of File", "File Path"), file=f)
    print("\t{}".format('-' * 100), file=f)

    if not path:
        with open(input_path) as file:
            for l in file.readlines():
                l_strip = l.strip()
                if os.path.exists(l_strip):
                    listDir(l_strip, f)
                else:
                    print('{} is not a validate path.'.format(l))
    elif os.path.isdir(path):
        listDir(path, f)
    elif os.path.isfile(path):
        if os.path.exists(path):
            listDir(path, f)
        else:
            print('{} is not a validate path.'.format(path))
            exit(0)
    else:
        print('{} is not a validate path.'.format(path))
        exit(0)

    print('\n\t{}'.format("RESULT"), file=f)
    print("\t{}".format('=' * 20), file=f)
    print("\t{:^25}|{:^15}|{:^15}|{:^15}|{:^15}"
          .format("Item", "File Count", 'File Ratio', 'Code Count', 'Code Ratio'), file=f)
    print("\t{}".format('-' * 90), file=f)
    print("\t{:<25}|{:^15}|{:^15}|{:^15}|{:^15}"
          .format("Total line of files", '----', '----', total_file_lines, '100.00%'), file=f)
    print("\t{:<25}|{:^15}|{:^15}|{:^15}|{:^15}"
          .format("Total line of codes", '----', '----',
                  total_code_lines, "%.2f%%" % (total_code_lines / total_file_lines * 100)), file=f)
    print("\t{:<25}|{:^15}|{:^15}|{:^15}|{:^15}"
          .format("Total line of blank", '----', '----',
                  total_blank_lines, "%.2f%%" % (total_blank_lines / total_file_lines * 100)), file=f)

    total_files = 0

    for _, count in files_of_language.items():
        total_files += count

    for tp, count in files_of_language.items():
        code_line = lines_of_language[tp]
        print("\t{:<25}|{:^15}|{:^15}|{:^15}|{:^15}".format(
            "For '.%s' files" % tp, count, '%.2f%%' % (count / total_files * 100),
            code_line, '%.2f%%' % (code_line / total_code_lines * 100)), file=f)

    if f:
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
        print('\033[0;31;0m[ERROR] Please specify a input: specify [-p PATH] or [-i INPUT]\033[0m')
        print(parser.print_help())
        exit(0)

    if args.path and args.input:
        print('\033[0;33;0m[WARN] Specify one input is enough,'
              ' the option `[-p PATH]` will be cover the option `[-i INPUT]`\033[0m')

    return args.path, args.input, args.output


if __name__ == '__main__':

    path, input_path, output_path = args_parser()

    time_start = time.time()
    search(path, input_path, output_path)
    time_end = time.time()

    print('\n\tTotally cost {}s.'.format(time_end - time_start))
