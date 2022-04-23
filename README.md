# Code Counter

A command-line interface (CLI) utility that can help you easily count code lines and display detailed results.

English | [中文](https://github.com/InnoFang/code-counter/blob/master/README_CN.md)

## Installation

Install by PyPI:

```shell
pip install code-counter
```

Also, you can install it from the source code: 

```shell
git clone https://github.com/innofang/code-counter.git
cd code-counter/
python setup.py install
```

## Quick Start

Open the terminal and directly search the path you want to count.

比如使用 `cocnt search` 来统计 `code-counter` 的代码行数。（`cocnt` 即 `codecounter` 的缩写）

For example, use `cocnt search` to count the number of code lines of `code counter`. (`cocnt` is the abbreviation of `code count`)

```shell
$ cocnt search ./code-counter

        RESULT
        ====================
        Total file lines    :     884 (100.00%)
        Total code lines    :     698 ( 78.96%)
        Total blank lines   :     157 ( 17.76%)
        Total comment lines :      29 (  3.28%)

              Type  |     Files  |     Ratio  |     Lines  |     Ratio
        -----------------------------------------------------------------
                py  |         9  |   100.00%  |       698  |   100.00%

        Totally cost 0.02192854881286621 s.
```

Please refer to [Usage](#usage) for more usage.

<h2 id="usage">Usage</h2>

The help information of `code-counter ` is as follows.

```shell 
$ cocnt --help
usage: cocnt <command> [<args>]
These are common Code-Counter commands used in various situations:
    search     Search code in the given path(s)
    config     Configure Code-Counter

A command-line interface (CLI) utility that can help you easily count code and display detailed results.

positional arguments:
  command     Subcommand to run, `search` or `config`

optional arguments:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
```

`code-counter ` supports two subcommands: [`search`](#search) and [`config`](#config)

<h3 id="search">search</h3>

Search the given path and make statistics. The help information of `cocnt search` is as follows.

```shell
$ cocnt search --help
usage: cocnt search input_path [-h] [-v] [-g] [-o OUTPUT_PATH] [--suffix SUFFIX] [--comment COMMENT] [--ignore IGNORE]

Search code in the given path(s)

positional arguments:
  input_path            counting the code lines according to the given path(s)

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         show verbose information
  -g, --graph           choose to whether to visualize the result
  -o OUTPUT_PATH, --output OUTPUT_PATH
                        specify an output path if you want to store the result
  --suffix SUFFIX       what code files do you want to count
  --comment COMMENT     the comment symbol, which can be judged whether the current line is a comment
  --ignore IGNORE       ignore some directories or files that you don't want to count
```

#### Search the given path directly

```shell
$ cocnt search ./code-counter/

        RESULT
        ====================
        Total file lines    :     860 (100.00%)
        Total code lines    :     689 ( 80.12%)
        Total blank lines   :     142 ( 16.51%)
        Total comment lines :      29 (  3.37%)

              Type  |     Files  |     Ratio  |     Lines  |     Ratio
        -----------------------------------------------------------------
                py  |         9  |   100.00%  |       689  |   100.00%

        Totally cost 0.005997896194458008 s.
```

#### Search multiple paths at the same time

You can specify more than one path separated by commas. For example, if you want to count the code files under the directory `./Cpp`, `./Go`, `./Rust` at the same time, the command can be like this.

```shell
$ cocnt search ./Cpp,./Go,./Rust

        RESULT
        ====================
        Total file lines    :   17485 (100.00%)
        Total code lines    :   10679 ( 61.08%)
        Total blank lines   :    1704 (  9.75%)
        Total comment lines :    5102 ( 29.18%)

              Type  |     Files  |     Ratio  |     Lines  |     Ratio
        -----------------------------------------------------------------
                 c  |        29  |    14.15%  |      2683  |    25.12%
                 h  |         7  |     3.41%  |       503  |     4.71%
               cpp  |        77  |    37.56%  |      3267  |    30.59%
               hpp  |         1  |     0.49%  |       238  |     2.23%
                go  |        60  |    29.27%  |      2624  |    24.57%
                rs  |        31  |    15.12%  |      1364  |    12.77%

        Totally cost 0.0940864086151123 s.
```

`code-counter` supports searching paths in different directories at the same time, so the given paths do not need to be in the same directory.

#### Show verbose searching information

Searching information is not displayed by default. If you play more attention to the search information, you can use the `[-v --verbose]` flag to show it when searching.

```shell
$ cocnt search ./code-counter -v

        SEARCHING
        ====================
         File Type  |     Lines  |      Code  |     Blank  |   Comment  |  File Path
        ------------------------------------------------------------------------------------------
                py  |        80  |        62  |        16  |         2  |  ./code-counter\code_counter\conf\config.py
                py  |         0  |         0  |         0  |         0  |  ./code-counter\code_counter\conf\__init__.py
                py  |        88  |        75  |        11  |         2  |  ./code-counter\code_counter\core\argspaser.py
                py  |       257  |       198  |        38  |        21  |  ./code-counter\code_counter\core\codecounter.py
                py  |         0  |         0  |         0  |         0  |  ./code-counter\code_counter\core\__init__.py
                py  |         1  |         1  |         0  |         0  |  ./code-counter\code_counter\__init__.py
                py  |        35  |        22  |        11  |         2  |  ./code-counter\code_counter\__main__.py
                py  |        48  |        44  |         4  |         0  |  ./code-counter\setup.py
                py  |       351  |       287  |        62  |         2  |  ./code-counter\test\test.py

        RESULT
        ====================
        Total file lines    :     860 (100.00%)
        Total code lines    :     689 ( 80.12%)
        Total blank lines   :     142 ( 16.51%)
        Total comment lines :      29 (  3.37%)

              Type  |     Files  |     Ratio  |     Lines  |     Ratio
        -----------------------------------------------------------------
                py  |         9  |   100.00%  |       689  |   100.00%

        Totally cost 0.006999015808105469 s.
```


#### Search code files for specific file suffixes

`code-counter` has a default configuration, which includes common code file suffixes, comment symbols, and directory or file names that need to be ignored. Therefore, if there are no special requirements during use, you can directly use `cocnt search` for code statistics.

If you only want to count some specific code files when searching, you can use the `--suffix` to specify the code file suffix. For example:

```shell
$ cocnt search ./project --suffix="py,java"
```

Of course, specify the comment symbols during searching the code, which is helpful to count the number of comments in the code.

```shell
$ cocnt search ./project --suffix="py,java" --comment="#,//,/**"
```

#### Ignore directories or files during the search

During the search, it is easy to count the code files or directories that you do not want to count, so you can use the `--ignore` to specify the directory or file names that need to be ignored during the search.

```shell
$ cocnt search ./project --suffix="py,java" --comment="#,//,/**" --ignore="target,__pycache__"
```

Generally speaking, the configuration file of `code-counter` already contains many common default configurations. For example, the default value of `ignore` is shown below.

```json
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
```

Therefore, in some cases, if the directory or file to be searched is the same as the default value of `ignore`, you can set `--ignore=""` to empty the default value of `ignore`. Of course, this is temporary. If you want to persist with these changes, you can refer to the `--ignore-reset` flag mentioned later when introducing `cocnt config`.

### Specify the output path to save the search results

If you want to save the statistical results, you can specify the path to save the search results through the `[-o -- output]` flag. If an output path is specified, the output information will not be displayed on the console.

```shell
$ cocnt search ./code-counter -v -o result.txt

        Totally cost 0.0050046443939208984 s.
```

verbose search information and results will be written to `result.txt`

### Visualize statistical results

Data visualization can provide a more intuitive feeling, so you can specify the `[-g -- graph]` flag to visualize the statistical results during the search.

```
$ cocnt search ./miscode -g
```

In addition to the statistical data displayed on the terminal, the statistical chart shown in the figure below will also be displayed.

![](https://cdn.jsdelivr.net/gh/innofang/jotter/source/code-counter/result.png)

<h3 id="config">config</h3>

Configure `code-counter`, and the help information of `cocnt config` is as follows.

```shell
$ cocnt config --help
usage: cocnt config [-h] [--list] [--suffix-reset SUFFIX_RESET] [--suffix-add SUFFIX_ADD] [--comment-reset COMMENT_RESET] [--comment-add COMMENT_ADD] [--ignore-reset IGNORE_RESET] [--ignore-add IGNORE_ADD] [--restore]

configure code-counter

optional arguments:
  -h, --help            show this help message and exit
  --list                list all variables set in the config file, along with their values
  --suffix-reset SUFFIX_RESET
                        reset the 'suffix' in the config and count code lines according to this value
  --suffix-add SUFFIX_ADD
                        append new value for the 'suffix' in the config and count code lines according to this value
  --suffix-del SUFFIX_DEL
                        delete some values of the 'suffix' in the config
  --comment-reset COMMENT_RESET
                        reset the 'comment' in the config and count comment lines according to this value
  --comment-add COMMENT_ADD
                        append new value for the 'comment' in the config and count comment lines according to this value
  --comment-del COMMENT_DEL
                        delete some values of the 'comment' in the config
  --ignore-reset IGNORE_RESET
                        reset the 'ignore' in the config and ignore some files or directories according to this value
  --ignore-add IGNORE_ADD
                        append new value for the 'ignore' in the config and ignore some files or directories according to this value
  --ignore-del IGNORE_DEL
                        delete some values of the 'ignore' in the config
  --restore             restore default config
```

#### List configuration information

Under the `config` subcommand, specify the `--list` to display configuration information. The default configuration of `code-counter` is shown below.

```shell
$ cocnt config --list
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

 + **`suffix`**: Code file suffix that will be counted during the search
 + **`comment`**: Comment symbol that can be judged whether the current line is comment during the search
 + **`ignore`**: Directories or files you want to ignore during the search

#### Reset the value of the configuration variable

The default configuration of `code-counter` basically includes common code file suffixes, comment symbols, and directory or file names that need to be ignored. But if you don't think so many variable values would be used during the search, you can choose to reset the default values.

 + `--suffix-reset` can reset the default code file suffixes.
 + `--comment-reset` can reset the default comment symbols
 + `--ignore-reset` can reset the default directory or files to ignore

These 3 flags can be used in combination or separately. You will be asked for each operation that will modify the configuration file, you can check whether the content to be modified is correct. If you are sure to modify, you can enter `y`, otherwise enter `n` to not modify.

Multiple values can be separated by commas, as shown in the following example.

```shell
$ cocnt config --suffix-reset="python,java" --comment-reset="#,/**,//" --ignore-reset="__pycache_,.pytest_cache,target"
'suffix' will be replaced with ['python', 'java'] . (y/n) y
'comment' will be replaced with ['#', '/**', '//'] . (y/n) y
'ignore' will be replaced with ['__pycache_', '.pytest_cache', 'target'] . (y/n) y
```

#### Add the value of the configuration variable

For the case of adding the value of the configuration variable, the following flags can be used:
 + `--suffix-add` add code file suffixes
 + `--comment-add` add comment symbols
 + `--ignore-add` add the directories or files to ignore

These 3 flags can be used in combination or separately. You will be asked for each operation that will modify the configuration file, you can check whether the content to be modified is correct. If you are sure to modify, you can enter `y`, otherwise enter `n` to not modify.

Multiple values can be separated by commas, as shown in the following example.

```shell
$ cocnt config --suffix-add="js,lisp" --comment-add=";" --ignore-add="node_modules"
'suffix' will be appended with ['js', 'lisp'] . (y/n) y
'comment' will be appended with [';'] . (y/n) y
'ignore' will be appended with ['node_modules'] . (y/n) y
```

#### Delete some configuration variable values

For the deletion of configuration variable values, `code-counter` provides the following flags:
+ `--suffix-del` delete unwanted code file suffixes from the default configuration
+ `--comment-del` delete unwanted comment symbols from the default configuration
+ `--ignore-del` delete the directory or file names that don't need to be ignored from the default configuration

These 3 flags can be used in combination or separately. You will be asked for each operation that will modify the configuration file, you can check whether the content to be modified is correct. If you are sure to modify, you can enter `y`, otherwise enter `n` to not modify.

Multiple values can be separated by commas, as shown in the following example.

```shell
$ cocnt config --suffix-del="clj,lisp" --comment-del=";" --ignore-del="build,target"
'suffix' will remove ['clj', 'lisp'] . (y/n) y
'comment' will remove [';'] . (y/n) y
'ignore' will remove ['build', 'target'] . (y/n) y
```

### Restore default configuration

Use the `--restore` flag to restore the default configuration of `code-counter`.

```shell
$ cocnt config --restore
The default configuration will be restored. (y/n) y
```

## [License](https://github.com/InnoFang/code-counter/blob/master/LICENSE)

        Copyright 2019-2022 Inno Fang

        Licensed under the Apache License, Version 2.0 (the "License");
        you may not use this file except in compliance with the License.
        You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

        Unless required by applicable law or agreed to in writing, software
        distributed under the License is distributed on an "AS IS" BASIS,
        WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
        See the License for the specific language governing permissions and
        limitations under the License.
