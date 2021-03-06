# Code Counter

你想知道自己到底写过多少行代码吗？来吧，让我们来测一测。

[English](README.md) | 中文

## 如何运行

```shell
$ git clone https://github.com/innofang/code-counter.git
$ cd code-counter/
$ python code-counter.py -p code-counter.py
```

更多使用方法请参考下方的 [用法](#usage) 和 [案例](#example)。 

<h2 id="usage">用法</h2>

```shell 
usage: code-counter [-h] [-i INPUT] [-p PATH] [-o OUTPUT] [-v]

Let's get count your code

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        the file contains a list of file path, which can make
                        you search more than one file or directory
  -p PATH, --path PATH  specify a file or directory path you want to search
  -o OUTPUT, --output OUTPUT
                        specify a output path if you want to store the result
  -v, --visual          choose to whether to visualize the result

```

## 配置

如果你想添加你想计数的文件类型、增加注释符号、或者忽略一些文件夹，你可以进行一些配置。

请查看 [config.py](config.py)

```
config = {
    # 哪些代码文件是你想统计的？请将文件后缀填写在下面
    'suffix': ('py', 'java', 'c', 'cpp', 'js', 'pde', 'kt', 'dart'),

    # 注释符号，可以用来判断当前行是否是一个注释，可自行补充
    # 若当前行是在注释符号之间，且行首无注释符号，则当前行可能会被错判
    'comment': ('#', '//', '/*', '/**', '*', ':', ';'),

    # 忽略一些由项目生成的文件夹或者文件，可自行补充
    'ignore': ('out', 'venv', '.git', '.idea', 'build', 'target', 'node_modules'),
}

```

> 若你想统计某个项目自己写了多少行代码，那么利用 `ignore` 来忽略项目生成的代码文件会更客观点

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
F:\Github\playground\
F:\IDEA\jokul
...
```

> **提示** 如果你不想在当前目录创建文件，那么你可以在任何地方创建并把文件路径作为输入

然后使用 `list.txt` 作为输入：

```shell
$ python code-counter.py -i list.txt

	SEARCHING
	====================
	 File Type  |     Lines  |      Code  |     Blank  |   Comment  |  File Path
	------------------------------------------------------------------------------------------
	      java  |        47  |        31  |        12  |         4  |  F:\Github\playground\Android\ActivityCollector.java
	      java  |        53  |        32  |         8  |        13  |  F:\Github\playground\Android\AppUtil.java
	      java  |       192  |       141  |        29  |        22  |  F:\Github\playground\Android\CircularAnimUtil.java
                ...          ...          ...         ...           ...    ...
                ...          ...          ...         ...           ...    ...
                ...          ...          ...         ...           ...    ...
	      java  |        37  |        28  |         6  |         3  |  F:\IDEA\jokul\jokul-server\src\test\java\io\innofang\jokul\controller\MovieControllerTest.java
	      java  |       305  |       266  |        24  |        15  |  F:\IDEA\jokul\jokul-server\src\test\java\io\innofang\jokul\repositories\MovieRepositoryTest.java
	      java  |        61  |        51  |         7  |         3  |  F:\IDEA\jokul\jokul-server\src\test\java\io\innofang\jokul\repositories\TypeRepositoryTest.java

	RESULT
	====================
	Total file lines    :   31890 (100.00%)
	Total code lines    :   21842 ( 68.49%)
	Total blank lines   :    4518 ( 14.17%)
	Total comment lines :    5530 ( 17.34%)

	      Type  |     Files  |     Ratio  |     Codes  |     Ratio
	-----------------------------------------------------------------
	        js  |        21  |     3.61%  |      1664  |     7.62%
	        py  |       158  |    27.19%  |      5602  |    25.65%
	        kt  |        26  |     4.48%  |       696  |     3.19%
	         c  |        28  |     4.82%  |      2533  |    11.60%
	      java  |       211  |    36.32%  |      6235  |    28.55%
	       cpp  |        75  |    12.91%  |      3094  |    14.17%
	       pde  |        62  |    10.67%  |      2018  |     9.24%


        Totally cost 0.23161602020263672s.

```

> **提示** 为了展示省略了一些输出

使用路径还是文件作为输入是你的自由，但是选择其中一个就足够了。如果你同时指定了两者，那么选项 `[-p PATH]` 将会覆盖选项  `[-i INPUT]`。

### 此外，你也可以指定一个输出路径

通过 `[-o --output]` 来指定输出路径，如下所示：

```shell
$ python code-counter.py -p code-counter.py -o result.txt
$ python code-counter.py -i list.txt -o output.txt
```

输出路径是可选的，如果你指定了它的话，输出将直接到文件中而不会显示在控制台。

### 统计结果可视化

数据可视化可以给我们更直观的感受，所以我们提供了将统计结果可视化的指令  `[-v --visual]`。使用示例如下：

```
$ python code-counter.py -i list.txt -v
```

上面已经粗略的展示了最终的统计结果，现在来看看更直观的可视化结果

![](https://cdn.jsdelivr.net/gh/innofang/jotter/source/code-counter/result.png)

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
