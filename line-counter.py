import os
import re
import sys
import time
from collections import defaultdict

total_file_lines  = 0
total_code_lines  = 0
total_space_lines = 0
ignore = ['output', 'venv', 'build', 'target', '.git']
pattern = re.compile('.*\.(py|java||c|cpp|js|pde|kt|dart)$')
file_dict = defaultdict(int)


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


def listDir(path):
    global total_file_lines, total_code_lines, total_space_lines, pattern, file_dict

    files = os.listdir(path)
    for file in files:
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            if os.path.split(file_path)[-1] in ignore:
                continue
            listDir(file_path)
        elif os.path:
            try:
                res = re.match(pattern, file)
                if res:
                    line_of_file, line_of_code, line_of_space = countFileLines(file_path)
                    file_type = os.path.splitext(file)[1][1:]
                    file_dict[file_type] += 1
                    print('{:>13}  |  {:>13}  |  {:>13}  |  {:>13}  |  {}'.format(file_type, line_of_file, line_of_code, line_of_space, file_path))
                    total_file_lines  += line_of_file
                    total_code_lines  += line_of_code
                    total_space_lines += line_of_space
            except AttributeError as e:
                print(e)


def main(input_path, output_path):
    global total_file_lines, total_code_lines, total_space_lines

    if not os.path.exists(input_path):
        print('{} is not exist, please create it and add some file path you want to count.'.format(input_path)) 
        exit(0)
 
    f = open(output_path, 'w')

    with open(input_path) as file:
        print('\n\t{}'.format("SEARCHING"))
        print("\t{}".format('=' * 20))
        print('{:>13}  |  {:>13}  |  {:>13}  |  {:>13}  |  {}'.format("File Type", "Line of File", "Code of File", "Space of File", "File Path"))
        print("\t{}".format('-' * 100))
        for line in file.readlines():
            line = line.strip()
            if os.path.exists(line):
                listDir(line)
            else:
                print('{} is not a validate path.'.format(line))
    
    f.write('\n\t{}\n'.format("RESULT"))
    f.write("\t{}\n".format('=' * 20))
    f.write("\t{:^25}|{:^10}|{:^10}\n".format("Item", "Count",  'Ratio'))
    f.write("\t{}\n".format('-' * 45))
    f.write("\t{:<25}|{:^10}|{:^10}\n".format("Total line of files", total_file_lines,  '100%'))
    f.write("\t{:<25}|{:^10}|{:^10}\n".format("Total line of codes", total_code_lines,  "%.2f%%" % (total_code_lines/total_file_lines*100)))
    f.write("\t{:<25}|{:^10}|{:^10}\n".format("Total line of space", total_space_lines, "%.2f%%" % (total_space_lines/total_file_lines*100)))
 
    total_files = 0
 
    # py|java||c|cpp|js|pde|kt|dart
    for _, count in file_dict.items():
        total_files += count
    
    for tp, count in file_dict.items():
        f.write("\t{:<25}|{:^10}|{:^10}\n".format("For '.%s' files" % (tp), count,  '%.2f%%' % (count / total_files * 100)))

    f.close()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Please specify the input file and output file.')
        print('Usage: python line-counter.py <input file> <output file>\n')
        print("""
TIPS: for the format of input file, it's content should be a list of file path (or directory path), just as follow:

    F:/Github/Android
    F:/Github/Java
    F:/Github/Python/line-counter/line-counter.py
    ...
        """)
        exit(1)
    
    intput_path = sys.argv[1]
    output_path = sys.argv[2]

    time_start = time.time()
    main(intput_path, output_path)
    time_end = time.time()

    with open(output_path) as f:
        for line in f:
            print(line, end='')

    print('\n\tTotally cost {}s.'.format(time_end - time_start))

    """
    Total number of lines of code:  181840
    The number of  c  file:  29  , ratio is 1.26%
    The number of  cpp  file:  129  , ratio is 5.61%
    The number of  java  file:  1409  , ratio is 61.31%
    The number of  js  file:  83  , ratio is 3.61%
    The number of  kt  file:  289  , ratio is 12.58%
    The number of  py  file:  263  , ratio is 11.44%
    The number of  pde  file:  85  , ratio is 3.70%
    The number of  dart  file:  11  , ratio is 0.48%
    Totally cost:  3.1801540851593018 s
    """
