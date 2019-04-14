# Code Counter

Do you wander how many code you have been written? Come on, let's get count it.

## How to run

```shell
$ git clone https://github.com/innofang/code-counter.git
$ cd code-counter/
$ python code-counter.py -p code-counter.py
```

Refer to [Usage](#usage) and [Example](#example) below for more usage

<h2 id="usage">Usage</h2>

```shell 
usage: code-counter [-h] [-i INPUT] [-p PATH] [-o OUTPUT]

Let's get count your code

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        the file contains a list of file path, which can make
                        you search more than one file or directory
  -p PATH, --path PATH  specify a file or directory path you want to search
  -o OUTPUT, --output OUTPUT
                        specify a output path if you want to store the result

```

## Configuration

If you want to ignore some directories or add the file type you want to count, you can make some configuration.

Please see [config.py](config.py)

```
config = {
    # Which suffix code file do you want to count?
    # more than as follow, also html, css, clj, lisp, etc.
    'suffix': ['py', 'java', 'c', 'cpp', 'js', 'pde', 'kt', 'dart'],

    # Ignore some directories or files which are not write by yourself
    # but generate by the projects, just add what you want to add.
    'ignore': ['out', 'venv', '.git', '.idea', 'build', 'target', 'node_modules'],
}
```

> **NOTE** `ignore` is important, the reason is that if you want to count how many code you have written and there are some code generate by the project automatically which is not belong to you, so ignore them is fair.

<h2 id="example">Example</h2>

### Specify a file path directly

```shell
$ python code-counter.py -p code-counter.py

        SEARCHING
        ====================
         File Type  |   Line of File  |   Code of File  |  Blank of File  |  File Path
        ----------------------------------------------------------------------------------------------------
                py  |            159  |            130  |             29  |  code-counter.py

        RESULT
        ====================
                  Item           |  File Count   |  File Ratio   |  Code Count   |  Code Ratio
        ------------------------------------------------------------------------------------------
        Total line of files      |     ----      |     ----      |      159      |    100.00%
        Total line of codes      |     ----      |     ----      |      130      |    81.76%
        Total line of blank      |     ----      |     ----      |      29       |    18.24%
        For '.py' files          |       1       |    100.00%    |      130      |    100.00%

        Totally cost 0.0010030269622802734s.

```

### Specify a directory path directly

```shell
$ python code-counter.py -p .

        SEARCHING
        ====================
         File Type  |   Line of File  |   Code of File  |  Blank of File  |  File Path
        ----------------------------------------------------------------------------------------------------
                py  |            159  |            130  |             29  |  .\code-counter.py
                py  |              9  |              8  |              1  |  .\config.py

        RESULT
        ====================
                  Item           |  File Count   |  File Ratio   |  Code Count   |  Code Ratio
        ------------------------------------------------------------------------------------------
        Total line of files      |     ----      |     ----      |      168      |    100.00%
        Total line of codes      |     ----      |     ----      |      138      |    82.14%
        Total line of blank      |     ----      |     ----      |      30       |    17.86%
        For '.py' files          |       2       |    100.00%    |      138      |    100.00%

        Totally cost 0.0020160675048828125s.

```

### Use a file that contain a list of file path or directory path as input

Firstly, create a file named `list.txt` or whatever you want to named in the current directory, which contain various file path or directory path, just as follow:

```
F:\Github\playground\Python
F:\Github\playground\Java
```

> **TIPS** If you don't want to create a file in the current directory, you can create it any where and use a file path of it as input.

then use `list.txt` as input:

```shell
$ python code-counter.py -i list.txt

        SEARCHING
        ====================
         File Type  |   Line of File  |   Code of File  |  Blank of File  |  File Path
        ----------------------------------------------------------------------------------------------------
                py  |            126  |             95  |             31  |  F:\Github\playground\Python\basic\BasicDataType.py
                py  |             21  |             18  |              3  |  F:\Github\playground\Python\basic\closure_test.py
                py  |             15  |             11  |              4  |  F:\Github\playground\Python\basic\count_words_num.py
                py  |             17  |             13  |              4  |  F:\Github\playground\Python\basic\CUDA_test.py
               ...               ...               ...               ...     ...
               ...               ...               ...               ...     ...
               ...               ...               ...               ...     ...
              java  |             43  |             34  |              9  |  F:\Github\playground\Java\SpringDemo\src\test\java\io\innofang\jdbc\StudentJdbcTemplateTest.java
              java  |             20  |             16  |              4  |  F:\Github\playground\Java\SpringDemo\src\test\java\io\innofang\loosely_coupled\OutputHelperTest.java
              java  |             22  |             17  |              5  |  F:\Github\playground\Java\SpringDemo\src\test\java\io\innofang\post_processor\MessageTest.java
              java  |             21  |             17  |              4  |  F:\Github\playground\Java\SpringDemo\src\test\java\io\innofang\spring_auto\service\CustomerServiceTest.java

        RESULT
        ====================
                  Item           |  File Count   |  File Ratio   |  Code Count   |  Code Ratio
        ------------------------------------------------------------------------------------------
        Total line of files      |     ----      |     ----      |     13460     |    100.00%
        Total line of codes      |     ----      |     ----      |     10820     |    80.39%
        Total line of blank      |     ----      |     ----      |     2640      |    19.61%
        For '.c' files           |       1       |     0.30%     |       0       |     0.00%
        For '.java' files        |      162      |    49.39%     |     4337      |    40.08%
        For '.js' files          |       6       |     1.83%     |      214      |     1.98%
        For '.py' files          |      158      |    48.17%     |     6269      |    57.94%
        For '.cpp' files         |       1       |     0.30%     |       0       |     0.00%

        Totally cost 0.1353609561920166s.

```

> **TIPS** Some output is ommited for dispaly

Use a path or a file input is your free, but choose one of them is enough.
If you choose both of them at the same time, the option `[-p PATH]` will be cover the option `[-i INPUT]`.

### Also, you can specify an output path

```shell
$ python code-counter.py -p code-counter -o result.txt
$ python code-counter.py -i list.txt -o output.txt
```

The output path is optional, if you have specify it, the output information would not display on the console.

## [License](./LICENSE)

    Code Counter: Count your code lines
    Copyright (C) 2019  InnoFang

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
