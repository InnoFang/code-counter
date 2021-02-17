# Code Counter

A command-line interface (CLI) utility that can help you easily count code and display detailed results.

English | [中文](https://github.com/InnoFang/code-counter/blob/master/README_CN.md)

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
$ codecount -h
usage: code-counter [-h] [-V] [-l] [-v] [-g] [-o OUTPUT] [--suffix SUFFIX] [--suffix-save SUFFIX_SAVE] [--suffix-add SUFFIX_ADD] [--comment COMMENT]
                    [--comment-save COMMENT_SAVE] [--comment-add COMMENT_ADD] [--ignore IGNORE] [--ignore-save IGNORE_SAVE] [--ignore-add IGNORE_ADD]
                    [--restore]
                    [path, CONFIG]

A command-line interface (CLI) utility that can help you easily count code and display detailed results.

positional arguments:
  [path, CONFIG]        specify a file or directory path you want to count or use CONFIG placeholder to configure

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
  -l, --list            the file contains a list of file path, which can make you search more than one file or directory
  -v, --verbose         show verbose infomation
  -g, --graph           choose to whether to visualize the result
  -o OUTPUT, --output OUTPUT
                        specify a output path if you want to store the result
  --suffix SUFFIX       what code files do you want to count, this parameter is disposable
  --suffix-save SUFFIX_SAVE
                        override 'suffix' in config and count codes according to this value
  --suffix-add SUFFIX_ADD
                        append new value for 'suffix' in config and count codes according to this value
  --comment COMMENT     the comment symbol, which can be judged whether the current line is a comment, this parameter is disposable
  --comment-save COMMENT_SAVE
                        override 'comment' in config and count comment lines according to this value
  --comment-add COMMENT_ADD
                        append new value for 'comment' in config and count comment lines according to this value
  --ignore IGNORE       ignore some directories or files that you don't want to count, this parameter is disposable
  --ignore-save IGNORE_SAVE
                        override 'ignore' in config and ignore some files or directory according to this value
  --ignore-add IGNORE_ADD
                        append new value for 'ignore' in config and ignore some files or directory according to this value
  --restore             restore default config

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
    "suffix": [
        "c",
        "cc",
        "clj",
        "cpp",
        "cs",
        "cu",
        "cuh",
        "dart",
        "go",
        "h",
        "hpp",
        "java",
        "jl",
        "js",
        "kt",
        "lisp",
        "lua",
        "pde",
        "m",
        "php",
        "py",
        "R",
        "rb",
        "rs",
        "rust",
        "sh",
        "scala",
        "swift",
        "ts",
        "vb"
    ],
    "comment": [
        "#",
        "//",
        "/*",
        "*",
        "*/",
        ":",
        ";",
        "\"\"\"\""
    ],
    "ignore": [
        "out",
        "venv",
        ".git",
        ".idea",
        "build",
        "target",
        "node_modules",
        ".vscode",
        "dist"
    ]
}
```

 + **`suffix`**: what code files do you want to count;
 + **`comment`**: the comment symbol, which can be judged whether the current line is a comment;
 + **`ignore`**: ignore some directories or files that you don't want to count.

> **NOTE**
> 
> + For **`suffix`**, for example, `Python` file's suffix is  `py`, `C++` file's suffix is `cpp`
> + For **`ignore`**, if you want to count how much code you have written, but there are some code generated automatically by the project, ignoring the generated code will make the statistics more accurate
> + For **`comment`**, if a comment is between two comment symbols and there is no other comment symbol at the beginning of the line, the content of the line may be misjudged, such as identifying the comment as code

### Specify `suffix`

The default suffix already contains common code suffixes, but if you know exactly what type of code you want to count, you can specify suffixes directly, which can ignore files that don't need to be counted and speed up the counting. [--suffix]` receive a parameter list (split by `,`).

```shell
$ codecount ./jokul --suffix="html,css,java,js"

        RESULT
        ====================
        Total file lines    :    3977 (100.00%)
        Total code lines    :    3061 ( 76.97%)
        Total blank lines   :     493 ( 12.40%)
        Total comment lines :     423 ( 10.64%)

              Type  |     Files  |     Ratio  |     Lines  |     Ratio
        -----------------------------------------------------------------
                js  |        15  |    28.30%  |      1485  |    48.51%
              html  |         1  |     1.89%  |        38  |     1.24%
               css  |         9  |    16.98%  |       338  |    11.04%
              java  |        28  |    52.83%  |      1200  |    39.20%

        Totally cost 0.0800015926361084s.
```

But this way of setting parameters is one-time. If you want to set parameters and save them, you can use `[--suffix-save]`.

#### Specify `suffix` and override

Use instruction `[--suffix-save]` and receive a parameter list (split by `,`).

```shell
$ codecount ./jokul --suffix-save="html,css,java,js"
'suffix' will be replaced with ['html', 'css', 'java', 'js'] (y/n)y

        RESULT
        ====================
        Total file lines    :    3977 (100.00%)
        Total code lines    :    3061 ( 76.97%)
        Total blank lines   :     493 ( 12.40%)
        Total comment lines :     423 ( 10.64%)

              Type  |     Files  |     Ratio  |     Lines  |     Ratio
        -----------------------------------------------------------------
                js  |        15  |    28.30%  |      1485  |    48.51%
              html  |         1  |     1.89%  |        38  |     1.24%
               css  |         9  |    16.98%  |       338  |    11.04%
              java  |        28  |    52.83%  |      1200  |    39.20%

        Totally cost 0.07199478149414062s.

```

#### Add `suffix` parameters

If you don't want to override the default config, but just want to add some new suffix for config, you can use `[--suffix-add]`. This way will still modify the `config.json`, so need you to confirm to perform.

```shell
$ codecount ./jokul --suffix-add="html,css,java,js"
'suffix' will be appended with ['html', 'css', 'java', 'js'] (y/n)y

        RESULT
        ====================
        Total file lines    :    3977 (100.00%)
        Total code lines    :    3061 ( 76.97%)
        Total blank lines   :     493 ( 12.40%)
        Total comment lines :     423 ( 10.64%)

              Type  |     Files  |     Ratio  |     Lines  |     Ratio
        -----------------------------------------------------------------
                js  |        15  |    28.30%  |      1485  |    48.51%
              html  |         1  |     1.89%  |        38  |     1.24%
               css  |         9  |    16.98%  |       338  |    11.04%
              java  |        28  |    52.83%  |      1200  |    39.20%

        Totally cost 0.06599712371826172s.
```

### Specify `comment`

If you know the type of code to be counted, and know what the comment symbols of the language are, you can use `[--comment]` to set.

```shell
$ codecount ./code-counter --comment='#,"""'

        RESULT
        ====================
        Total file lines    :     449 (100.00%)
        Total code lines    :     353 ( 78.62%)
        Total blank lines   :      76 ( 16.93%)
        Total comment lines :      20 (  4.45%)

              Type  |     Files  |     Ratio  |     Lines  |     Ratio
        -----------------------------------------------------------------
                py  |         7  |   100.00%  |       353  |   100.00%

        Totally cost 0.023006200790405273s.
```

This way also is one-time.

#### Specify `comment` and override

In the default config, `comment` already contains common comment symbols, so you don't need to modify it. If you need to override the default value of 'comment' indeed, you can use `[--comment-save]` to override it.

#### Add `comment` parameters

If you want to add some new comment symbols, you can use `[--comment-add]`.

### Specify `ignore`

Ignoring unnecessary folders can speed up the count, use `[--ignore]` to set.

```shell
$ codecount ./code-counter/ --ignore="__pycache__"

        RESULT
        ====================
        Total file lines    :     449 (100.00%)
        Total code lines    :     349 ( 77.73%)
        Total blank lines   :      76 ( 16.93%)
        Total comment lines :      24 (  5.35%)

              Type  |     Files  |     Ratio  |     Lines  |     Ratio
        -----------------------------------------------------------------
                py  |         7  |   100.00%  |       349  |   100.00%

        Totally cost 0.15700435638427734s.
```

This way also is one-time.

#### Specify `ignore` and override

If the default `ignore` is not what you want, you can use `[--ignore-save]` to modify it.

#### Add `ignore` parameters

If the default `ignore` is missing the value you need, and you don't want to override the default value,  you can use `[--ignore-add]` to add some new value for `ignore`.

### Show config

Use placeholder `CONFIG` to show the content of `config.json`.

```shell
$ codecount CONFIG
```

### The better way to modify the config

Sometimes we don't want to search and count when we modify `config.json`, so we can use the placeholder `CONFIG` to indicate that we only modify the config without searching and counting. Using the placeholder 'config' to set the parameter will display the updated value after modifying the parameter.

```shell
$ codecount CONFIG --suffix-save="java,js,html,py" --comment-save="//,#,/**" --ignore-add="__pycache__"
'ignore' will be appended with ['__pycache__'] (y/n)y
'suffix' will be replaced with ['java', 'js', 'html', 'py'] (y/n)y
'comment' will be replaced with ['//', '#', '/**'] (y/n)y
{
    "suffix": [ 
        "java", 
        "js",
        "html",
        "py"
    ],
    "comment": [
        "//",
        "#",
        "/**"
    ],
    "ignore": [
        "out",
        "venv",
        ".git",
        ".idea",
        "build",
        "target",
        "node_modules",
        ".vscode",
        "dist",
        "__pycache__"
    ]
}
```

### Restore default config

Use `[--restore]` to restore the default config.

```shell
$ codecount CONFIG --restore
Default configuration will be restored (y/n)?y
{
    "suffix": [
        "c",   
        "cc",  
        "clj", 
        "cpp", 
        "cs",  
        "cu",  
        "cuh", 
        "dart",
        "go",  
        "h",   
        "hpp", 
        "java",
        "jl",  
        "js",  
        "kt",  
        "lisp",
        "lua", 
        "pde",
        "m",
        "php",
        "py",
        "R",
        "rb",
        "rs",
        "rust",
        "sh",
        "scala",
        "swift",
        "ts",
        "vb"
    ],
    "comment": [
        "#",
        "//",
        "/*",
        "*",
        "*/",
        ":",
        ";",
        "\"\"\"\""
    ],
    "ignore": [
        "out",
        "venv",
        ".git",
        ".idea",
        "build",
        "target",
        "node_modules",
        ".vscode",
        "dist"
    ]
}
```

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
