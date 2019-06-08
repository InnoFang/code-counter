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
usage: code-counter [-h] [-i INPUT] [-p PATH] [-o OUTPUT] [-v VISUAL]

Let's get count your code

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        the file contains a list of file path, which can make
                        you search more than one file or directory
  -p PATH, --path PATH  specify a file or directory path you want to search
  -o OUTPUT, --output OUTPUT
                        specify a output path if you want to store the result
  -v VISUAL, --visual VISUAL
                        choose to whether to visualize the result
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
F:\Github\playground\
F:\IDEA\jokul
...
```

> **TIPS** If you don't want to create a file in the current directory, you can create it any where and use a file path of it as input.

then use `list.txt` as input:

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

> **TIPS** Some output is ommited for dispaly

Use a path or a file input is your free, but choose one of them is enough.
If you choose both of them at the same time, the option `[-p PATH]` will be cover the option `[-i INPUT]`.

### Also, you can specify an output path

The output path is specified by `[-o--output]`, as follows:

```shell
$ python code-counter.py -p code-counter.py -o result.txt
$ python code-counter.py -i list.txt -o output.txt
```

The output path is optional, if you have specify it, the output information would not display on the console.

### Visualization of Statistical Results

As we all know, data visualization can give us a more intuitive feeling, so we provide the visualization instruction `[-v --visual]`, whose default value is `false`, passing the `true` value will visualize the statistics. Add visual instruction based on the example of using file input as follows:

```
$ python code-counter.py -i list.txt -v true
```

The final statistical results have been roughly shown above, let's take a look at the more intuitive visualization results

![](https://raw.githubusercontent.com/InnoFang/jotter/image-hosting/code-counter/Visualization%20of%20Statistical%20Results.png)


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
