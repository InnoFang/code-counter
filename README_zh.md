# Code Counter

你想知道自己到底写过多少行代码吗？来吧，让我们来测一测。

[English](README.md) | [中文](README_zh.md)

## 如何运行

```shell
$ git clone https://github.com/innofang/code-counter.git
$ cd code-counter/
$ python code-counter.py -p code-counter.py
```

更多使用方法请参考下方的 [用法](#usage) 和 [案例](#example)。 

<h2 id="usage">用法</h2>

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

## 配置

如果你想忽略一些文件夹或者添加你想计数的文件类型，你可以进行一些配置。
请查看 [config.py](config.py)

```
config = {
    # 那些后缀代码文件是你想统计的？
    # 不只是如下的文件类型，html、css、clj、lisp等也可以
    'suffix': ('py', 'java', 'c', 'cpp', 'js', 'pde', 'kt', 'dart'),

    # 注释符号，可以用来判断当前行是否是一个注释
    # 然而，如果当前行是在注释符号之间，并且行首没有注释符号的话，那么当前行可能会被错判
    # 如果下面的注释符号确实了任何你想添加的符号，请自行添加
    'comment': ('#', '//', '/*', '/**', '*', ':', ';'),

    # 忽略一些不是你自己写的而是由项目自身产生的文件夹或者文件，你想添加哪些都可以
    'ignore': ('out', 'venv', '.git', '.idea', 'build', 'target', 'node_modules'),
}

```

> **注意** `ignore` 很重要, 理由是如果你想统计你写了多少行代码，但是有很多项目生成的代码不是你写的，那么忽略这些代码会公平点

<h2 id="example">案例</h2>

### 直接指定一个文件路径

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

### 直接指定一个目录路径

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

### 使用一个包含一系列文件路径和目录路径的文件作为输入

首先，在当前目录创建一个名为 `list.txt` 或者任何你想命名的文件，该文件将包含多个文件路径或目录路径，如下所示
```
F:\Github\playground\Python
F:\Github\playground\Java
```

> **提示** 如果你不想在当前目录创建文件，那么你可以在任何地方创建并把文件路径作为输入

然后使用 `list.txt` 作为输入：

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

> **提示** 为了展示省略了一些输出

使用路径还是文件作为输入是你的自由，但是选择其中一个就足够了。如果你同时指定了两者，那么选项 `[-p PATH]` 将会覆盖选项  `[-i INPUT]`。

### 此外，你也可以指定一个输出路径

```shell
$ python code-counter.py -p code-counter.py -o result.txt
$ python code-counter.py -i list.txt -o output.txt
```

输出路径是可选的，如果你制定了它的话，输出将不会显示在控制台。

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
