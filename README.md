# Code Counter

A command-line interface (CLI) utility that can help you easily count code and display detailed results.

English | [中文](https://github.com/InnoFang/code-counter/blob/master/README_zh.md)

## Installation

Install by PyPI (It hasn't been uploaded to pypi yet):

```shell
pip install code-counter
```

Also you can install it from the source code:

```shell
git clone https://github.com/innofang/code-counter.git
cd code-counter/
python setup.py install
```

## Quick Start

Switch to any code directory (e.g. `code-counter`), and enter the following command:

```shell
$ codecount .

        RESULT
        ====================
        Total file lines    :     344 (100.00%)
        Total code lines    :     269 ( 78.20%)
        Total blank lines   :      55 ( 15.99%)
        Total comment lines :      20 (  5.81%)

              Type  |     Files  |     Ratio  |     Lines  |     Ratio
        -----------------------------------------------------------------
                py  |         7  |   100.00%  |       269  |   100.00%

        Totally cost 0.010030031204223633s.

```

Refer to [Usage](#usage) and [Example](#example) below for more usage.

<h2 id="usage">Usage</h2>

```shell 
usage: code-counter [-h] [-l] [-v] [-g] [-o OUTPUT_PATH] path

Let's get count your code

positional arguments:
  path                  specify a file or directory path you want to search

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            the file contains a list of file path, which can make you search more than one file or directory
  -v, --verbose         show verbose infomation
  -g, --graph           choose to whether to visualize the result
  -o OUTPUT_PATH, --output OUTPUT_PATH
                        specify a output path if you want to store the result
```

<h2 id="example">Example</h2>

### Specify a path (file or directory) directly

```shell
$ codecount ./code-counter

        RESULT
        ====================
        Total file lines    :     344 (100.00%)
        Total code lines    :     269 ( 78.20%)
        Total blank lines   :      55 ( 15.99%)
        Total comment lines :      20 (  5.81%)

              Type  |     Files  |     Ratio  |     Lines  |     Ratio
        -----------------------------------------------------------------
                py  |         7  |   100.00%  |       269  |   100.00%

        Totally cost 0.00899815559387207s.


```

### Multipath input (Use a file that contain a list of file or directory path as input)

Create a file, such as named `list.txt`, which contain various file path or directory path, just as follow:

```
F:/Github/miscode
F:/IDEA/jokul
```

then use `[-l --list]` to specify `list.txt` contain a list of path:

```shell
$ codecount ./list.txt -l

        RESULT
        ====================
        Total file lines    :   35137 (100.00%)
        Total code lines    :   24235 ( 68.97%)
        Total blank lines   :    5009 ( 14.26%)
        Total comment lines :    5893 ( 16.77%)

              Type  |     Files  |     Ratio  |     Lines  |     Ratio
        -----------------------------------------------------------------
              java  |       236  |    36.48%  |      7074  |    29.19%
                 c  |        28  |     4.33%  |      2533  |    10.45%
                 h  |         8  |     1.24%  |       503  |     2.08%
               cpp  |        75  |    11.59%  |      3094  |    12.77%
                go  |        33  |     5.10%  |      1036  |     4.27%
                js  |        21  |     3.25%  |      1664  |     6.87%
                kt  |        26  |     4.02%  |       696  |     2.87%
              lisp  |         1  |     0.15%  |        48  |     0.20%
               pde  |        59  |     9.12%  |      1930  |     7.96%
                py  |       160  |    24.73%  |      5657  |    23.34%

        Totally cost 6.179003953933716s.

```

### Show verbose searching information

Searching information is not displayed by default. If you concern about the searching information, you can use `[-v --verbose]` to view it:

```
$ codecount ./code-counter -v

        SEARCHING
        ====================
         File Type  |     Lines  |      Code  |     Blank  |   Comment  |  File Path
        ------------------------------------------------------------------------------------------
                py  |        12  |         8  |         2  |         2  |  ./code-counter/code_counter/conf/config.py
                py  |         0  |         0  |         0  |         0  |  ./code-counter/code_counter/conf/__init__.py
                py  |       240  |       187  |        37  |        16  |  ./code-counter/code_counter/core/codecounter.py
                py  |         0  |         0  |         0  |         0  |  ./code-counter/code_counter/core/__init__.py
                py  |         1  |         1  |         0  |         0  |  ./code-counter/code_counter/__init__.py
                py  |        43  |        29  |        12  |         2  |  ./code-counter/code_counter/__main__.py
                py  |        48  |        44  |         4  |         0  |  ./code-counter/setup.py

        RESULT
        ====================
        Total file lines    :     344 (100.00%)
        Total code lines    :     269 ( 78.20%)
        Total blank lines   :      55 ( 15.99%)
        Total comment lines :      20 (  5.81%)

              Type  |     Files  |     Ratio  |     Lines  |     Ratio
        -----------------------------------------------------------------
                py  |         7  |   100.00%  |       269  |   100.00%

        Totally cost 0.00899958610534668s.

```

### Specify an output path

The output path is specified by `[-o --output]`, if you have specified it, the output information would not display on the console, as follows:

```shell
$ codecount ./code-counter -v -o ./result.txt

        Totally cost 0.012001991271972656s.

```

Verbose searching information and results have been written in `./result.txt`

### Visualize statistical results

Data visualization can give us a more intuitive feeling, so I provide the visualization instruction `[-g --graph]` that used to visualize the statistics, just as follow:

```
$ codecount list.txt -l -g
```

In addition to the text statistics, the statistical chart as shown in the figure below will also be displayed

![](https://cdn.jsdelivr.net/gh/innofang/jotter/source/code-counter/result.png)


## Configuration

Default `config.json` is as follow:

```json
{
    "suffix": ["py", "java", "c", "h", "cpp", "hpp", "js", "pde", "kt", "dart", "go", "lisp", "cu", "cuh"],
    "comment": ["#", "//", "/*", "*", ":", ";"],
    "ignore": ["out", "venv", ".git", ".idea", "build", "target", "node_modules", ".vscode"]
}
```

 + **`suffix`**: what suffix code files that you want to count;
 + **`comment`**: the comment symbol, which can be judged whether the current line is a comment;
 + **`ignore`**: ignore some directories or files that you don't want to count.

> **NOTE**
> 
> + For **`suffix`**, for example, `Python` file's suffix is  `py`, `C++` file's suffix is `cpp`
> + For **`ignore`**, if you want to count how much code you have written, but there are some code generated automatically by the project, ignoring the generated code will make the statistics more accurate
> + For **`comment`**, if a comment is between two comment symbols and there is no other comment symbol at the beginning of the line, the content of the line may be misjudged, such as identifying the comment as code

## [License](https://github.com/InnoFang/code-counter/blob/master/LICENSE)

        Copyright 2019 Inno Fang

        Licensed under the Apache License, Version 2.0 (the "License");
        you may not use this file except in compliance with the License.
        You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

        Unless required by applicable law or agreed to in writing, software
        distributed under the License is distributed on an "AS IS" BASIS,
        WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
        See the License for the specific language governing permissions and
        limitations under the License.
