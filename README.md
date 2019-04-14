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

If you want to ignore some directories or add the file type you want to count, you make some configuration,
see [config.py](config.py)

```
config = {
    # Which suffix code file do you want to count?
    # more than as follow, also html, css, clj, lisp, etc.
    'suffix': ['py', 'java', 'c', 'cpp', 'js', 'pde', 'kt', 'dart'],

    # Ignore some directories or files which are not write by yourself
    # but generate by the projects, just add what you want to add.
    'ignore': ['out', 'venv', '.git', '.idea', 'build', 'target'],
}
```

**TIPS** `ignore` is important, the reason is that if you want to count how many code you have written 
and there are some code generate by the project automatically which is not belong to you, 
so ignore them is fair

<h2 id="example">Example</h2>

### Specify a file or directory path directly

specify a file path

```shell
$ python code-counter.py -p code-counter.py

        SEARCHING
        ====================
    File Type  |   Line of File  |   Code of File  |  Space of File  |  File Path
        ----------------------------------------------------------------------------------------------------
           py  |            159  |            130  |             29  |  code-counter.py

        RESULT
        ====================
                  Item           |  File Count   |  File Ratio   |  Code Count   |  Code Ratio
        ------------------------------------------------------------------------------------------
        Total line of files      |     ----      |     ----      |      159      |    100.00%
        Total line of codes      |     ----      |     ----      |      130      |    81.76%
        Total line of space      |     ----      |     ----      |      29       |    18.24%
        For '.py' files          |       1       |    100.00%    |      130      |    100.00%

        Totally cost 0.0029420852661132812s.

```

specify a directory path

```shell
$ python code-counter.py -p .

        SEARCHING
        ====================
    File Type  |   Line of File  |   Code of File  |  Space of File  |  File Path
        ----------------------------------------------------------------------------------------------------
           py  |            159  |            130  |             29  |  .\code-counter.py
           py  |              9  |              8  |              1  |  .\config.py

        RESULT
        ====================
                  Item           |  File Count   |  File Ratio   |  Code Count   |  Code Ratio
        ------------------------------------------------------------------------------------------
        Total line of files      |     ----      |     ----      |      168      |    100.00%
        Total line of codes      |     ----      |     ----      |      138      |    82.14%
        Total line of space      |     ----      |     ----      |      30       |    17.86%
        For '.py' files          |       2       |    100.00%    |      138      |    100.00%

        Totally cost 0.004011392593383789s.

```   

### Use a file that contain a list of files or directories path as input

Firstly, create a file named `files.txt` or whatever you like in the current directory,
which contain a list of files or directories path, just as follow:

```
F:\Android\
F:\Github\code-counter\
...
```
then use it as input:

```shell
$ python code-counter.py -i files.txt
```

Use a path or a file as input is your free, but choose one of them is enough.
If you choose both of them at the same time, the `path` will be cover the `file` 

### Also, you can specify a output path

Just like this

```shell
$ python code-counter.py -p code-counter -o result.txt
$ python code-counter.py -i files.txt -o output.txt
```

the output path is optional.

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
