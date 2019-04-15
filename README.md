# Code Counter

Do you wander how many code you have been written? Come on, let's get count it.

English | [中文](README_zh.md)

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

If you want to add the file type you want to count, add some comment symbols, or ignore some directories, you can make some configuration.

Please see [config.py](config.py)

```
config = {
    # Which suffix code file do you want to count?
    # more than as follow, also html, css, clj, lisp, etc.
    'suffix': ('py', 'java', 'c', 'cpp', 'js', 'pde', 'kt', 'dart'),

    # the comment symbol, which can be judged whether the current line is a comment.
    # However, if the current lines are between the comment symbol
    # and there is not any comment symbol at the beginning of it, it will be misjudged.
    # If the following comment symbol miss any other you want to add, you can do it by yourself
    'comment': ('#', '//', '/*', '/**', '*', ':', ';'),

    # Ignore some directories or files which are not write by yourself,
    # but generate by the projects, just add what you want to add.
    'ignore': ('out', 'venv', '.git', '.idea', 'build', 'target', 'node_modules'),
}

```

> **NOTE** `ignore` is important, the reason is that if you want to count how many code you have written and there are some code generate by the project automatically which is not belong to you, so ignore them is fair.

<h2 id="example">Example</h2>

### Specify a file path directly

```shell
$ python code-counter.py -p code-counter.py

        SEARCHING
        ====================
         File Type  |     Lines  |      Code  |     Blank  |   Comment  |  File Path
        ------------------------------------------------------------------------------------------
                py  |       192  |       149  |        30  |        13  |  code-counter.py

        RESULT
        ====================
        Total file lines    :     192 (100.00%)
        Total code lines    :     149 ( 77.60%)
        Total blank lines   :      30 ( 15.62%)
        Total comment lines :      13 (  6.77%)

              Type  |     Files  |     Ratio  |     Codes  |     Ratio
        -----------------------------------------------------------------
                py  |         1  |   100.00%  |       149  |   100.00%

        Totally cost 0.00102996826171875s.

```

### Specify a directory path directly

```shell
$ python code-counter.py -p .

        SEARCHING
        ====================
         File Type  |     Lines  |      Code  |     Blank  |   Comment  |  File Path
        ------------------------------------------------------------------------------------------
                py  |       192  |       149  |        30  |        13  |  .\code-counter.py
                py  |        15  |         5  |         2  |         8  |  .\config.py

        RESULT
        ====================
        Total file lines    :     207 (100.00%)
        Total code lines    :     154 ( 74.40%)
        Total blank lines   :      32 ( 15.46%)
        Total comment lines :      21 ( 10.14%)

              Type  |     Files  |     Ratio  |     Codes  |     Ratio
        -----------------------------------------------------------------
                py  |         2  |   100.00%  |       154  |   100.00%

        Totally cost 0.003002166748046875s.

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
         File Type  |     Lines  |      Code  |     Blank  |   Comment  |  File Path
        ------------------------------------------------------------------------------------------
                py  |       126  |        73  |        31  |        22  |  F:\Github\playground\Python\basic\BasicDataType.py
                py  |        21  |        17  |         3  |         1  |  F:\Github\playground\Python\basic\closure_test.py
                py  |        15  |        10  |         4  |         1  |  F:\Github\playground\Python\basic\count_words_num.py
                ...          ...          ...         ...           ...    ...
                ...          ...          ...         ...           ...    ...
                ...          ...          ...         ...           ...    ...
              java  |        20  |        13  |         4  |         3  |  F:\Github\playground\Java\SpringDemo\src\test\java\io\innofang\loosely_coupled\OutputHelperTest.java
              java  |        22  |        14  |         5  |         3  |  F:\Github\playground\Java\SpringDemo\src\test\java\io\innofang\post_processor\MessageTest.java
              java  |        21  |        14  |         4  |         3  |  F:\Github\playground\Java\SpringDemo\src\test\java\io\innofang\spring_auto\service\CustomerServiceTest.java

        RESULT
        ====================
        Total file lines    :   13460 (100.00%)
        Total code lines    :    9348 ( 69.45%)
        Total blank lines   :    2640 ( 19.61%)
        Total comment lines :    1472 ( 10.94%)

              Type  |     Files  |     Ratio  |     Codes  |     Ratio
        -----------------------------------------------------------------
                py  |       158  |    48.17%  |      5602  |    59.93%
                js  |         6  |     1.83%  |       179  |     1.91%
              java  |       162  |    49.39%  |      3567  |    38.16%
               cpp  |         1  |     0.30%  |         0  |     0.00%
                 c  |         1  |     0.30%  |         0  |     0.00%

        Totally cost 0.14635539054870605s.

```

> **TIPS** Some output is ommited for dispaly

Use a path or a file input is your free, but choose one of them is enough.
If you choose both of them at the same time, the option `[-p PATH]` will be cover the option `[-i INPUT]`.

### Also, you can specify an output path

```shell
$ python code-counter.py -p code-counter.py -o result.txt
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
