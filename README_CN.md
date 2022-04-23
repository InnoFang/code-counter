# Code Counter

一个可以帮助你轻松进行代码行数统计的命令行小工具。

[English](./README.md) | 中文

## 安装

可以直接使用 PyPI 进行安装。

```shell
pip install code-counter
```

也可以下载源码后再安装。

```shell
git clone https://github.com/innofang/code-counter.git
cd code-counter/
python setup.py install
```

## 快速开始

打开终端，直接对想要统计的代码路径进行搜索。

比如使用 `cocnt search` 来统计 `code-counter` 的代码行数。（`cocnt` 即 `codecounter` 的缩写）

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

更多使用方法请参考[用法](#usage)。 

<h2 id="usage">用法</h2>

`code-counter` 的帮助信息如下。 

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

`code-counter` 支持两个子命令：[`search`](#search) 和 [`config`](#config)

<h3 id="search">search</h3>

搜索给定的路径并统计，`cocnt search` 的帮助信息如下。

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

#### 直接搜索给定的路径

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

#### 同时搜索多个路径

你可以指定多个路径，路径用逗号隔开。比如你想同时搜索 `./Cpp`，`./Go`，`./Rust` 这几个目录下的代码文件，则可以这样写。

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

`code-counter` 支持同时搜索不同目录下的路径，因此搜索路径不需要都在同一个目录下。

#### 展示详细搜索信息

搜索信息默认是不显示的。如果你比较关注搜索信息，可以在搜索时使用 `[-v --verbose]` 标志。

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

#### 搜索特定文件后缀的代码文件

`code-counter` 有默认的配置，默认配置中包含了常见的代码文件后缀、注释符号以及需要忽略的目录或文件名。因此在使用的时候如果没有特别的需求，可以直接使用 `cocnt search` 进行代码的统计。

如果在搜索的时候，只想统计某一些特定的代码文件的情况，那么可以使用 `--suffix` 来指定代码文件后缀。比如：

```shell
$ cocnt search ./project --suffix="py,java"
```

当然，在搜索时也可以指定编程语言的注释符号，这有利于更好的统计代码中注释的数量。

```shell
$ cocnt search ./project --suffix="py,java" --comment="#,//,/**"
```

#### 搜索时过忽略指定的目录或文件

在搜索代码文件的时候，容易统计到不想统计的代码文件或者目录，因此可以使用 `--ignore` 来指定在搜索时需要过滤的目录或者文件名。

```shell
$ cocnt search ./project --suffix="py,java" --comment="#,//,/**" --ignore="target,__pycache__"
```

一般来说，`code-counter` 的配置文件里已经包含了很多常见的默认配置，比如 `ignore` 的默认值如下所示。

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

因此，如果在某些情况下，要搜索的目录或文件与 `ignore` 的默认值相同，那么可以通过设置 `--ignore=""` 来置空 `ignore` 的默认值，当然这是临时的。如果想要持久化这些修改，可以参考后面介绍`cocnt config` 时会提及的 `--ignore-reset` 标志。

#### 指定搜索结果的保存路径

如果想保存统计结果，则可以通过 `[-o --output]` 标志来指定搜索结果的保存路径。如果指定了输出路径，那么输出信息将不会显示在控制台。

```shell
$ cocnt search ./code-counter -v -o result.txt

        Totally cost 0.0050046443939208984 s.
```

详细的搜索信息和结果将写入到 `./result.txt` 中。

#### 可视化统计结果

数据可视化可以提供更直观的感受，所以在搜索时可以指定 `[-g --graph]` 标志来可视化统计结果。

```shell
$ cocnt search ./miscode -g
```

除了在终端显示统计数据外，还会显示如下图的的统计图表。

![](https://cdn.jsdelivr.net/gh/innofang/jotter/source/code-counter/result.png)

<h3 id="config">config</h3>

对 `code-counter` 进行设置，`cocnt config` 的帮助信息如下。

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

#### 显示配置信息

在 `config` 子命令下，指定 `--list` 来显示配置信息。`code-counter` 的默认配置如下所示。

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

 + **`suffix`**: 搜索时会进行统计的代码文件后缀
 + **`comment`**: 注释符号，搜索时会判断当前行是否为注释
 + **`ignore`**: 搜索时想忽略的目录或文件

#### 重置配置信息

`code-counter` 的默认配置信息基本包含了常见的代码文件后缀、注释符号以及需要忽略的目录或文件名。但如果你认为在搜索时用不到这么多变量值，那么可以选择覆盖掉默认值。

 + `--suffix-reset` 可以覆盖掉默认的代码文件后缀
 + `--comment-reset` 可以覆盖掉默认的注释符号
 + `--ignore-reset` 可以覆盖掉默认的要忽略的目录或文件

这三个标志可以组合使用，也可以单独使用。对于每个会修改配置文件的操作都会对你进行询问，此时你可以检查要修改的内容是否正确，如果确认修改可以输入 `y`，否则输入 `n` 不执行修改。

对于要输入的多个值可以用逗号分隔，示例如下。

```shell
$ cocnt config --suffix-reset="python,java" --comment-reset="#,/**,//" --ignore-reset="__pycache_,.pytest_cache,target"
'suffix' will be replaced with ['python', 'java'] . (y/n) y
'comment' will be replaced with ['#', '/**', '//'] . (y/n) y
'ignore' will be replaced with ['__pycache_', '.pytest_cache', 'target'] . (y/n) y
```

#### 追加配置信息

对于要追加配置信息的情况，可以使用以下标志：
 + `--suffix-add` 追加默认情况下的代码文件后缀
 + `--comment-add` 追加默认情况下的注释符号
 + `--ignore-add` 追加默认情况下要忽略的文件类型

这三个标志可以组合使用，也可以单独使用。对于每个会修改配置文件的操作都会对你进行询问，此时你可以检查要修改的内容是否正确，如果确认修改可以输入 `y`，否则输入 `n` 不执行修改。

对于要输入的多个值可以用逗号分隔，示例如下。

```shell
$ cocnt config --suffix-add="js,lisp" --comment-add=";" --ignore-add="node_modules"
'suffix' will be appended with ['js', 'lisp'] . (y/n) y
'comment' will be appended with [';'] . (y/n) y
'ignore' will be appended with ['node_modules'] . (y/n) y
```

#### 删除配置信息

对于配置变量值的删除，`code-counter` 提供以下标志：
 + `--suffix-del` 从默认配置中，删除不需要的代码文件后缀
 + `--comment-del` 从默认配置中，删除不需要的注释符号
 + `--ignore-del` 从默认配置中，删除不需要忽略的目录或文件名

这三个标志可以组合使用，也可以单独使用。对于每个会修改配置文件的操作都会对你进行询问，此时你可以检查要修改的内容是否正确，如果确认修改可以输入 `y`，否则输入 `n` 不执行修改。

对于要输入的多个值可以用逗号分隔，示例如下。

```shell
$ cocnt config --suffix-del="clj,lisp" --comment-del=";" --ignore-del="build,target"
'suffix' will remove ['clj', 'lisp'] . (y/n) y
'comment' will remove [';'] . (y/n) y
'ignore' will remove ['build', 'target'] . (y/n) y
```

#### 恢复默认配置

使用 `--restore` 来恢复 `code-counter` 自带的默认配置。

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
