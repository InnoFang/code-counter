# Code Counter

[![](https://img.shields.io/pypi/v/code-counter)](https://pypi.org/project/code-counter/) ![](https://img.shields.io/pypi/dm/code-counter)

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
pip install -r requirements.txt
python setup.py install
```

## 快速开始

打开终端，直接对想要统计的代码路径进行搜索。

比如使用 `cocnt search` 来统计 `code-counter` 的代码行数。（`cocnt` 即 `codecounter` 的缩写）

```shell
$ cocnt search ./code-counter/

        RESULT
        ====================
        Total file lines    :    1420 (100.00%)
        Total code lines    :    1132 ( 79.72%)
        Total blank lines   :     252 ( 17.75%)
        Total comment lines :      36 (  2.54%)

              Type  |     Files  |     Ratio  |     Lines  |     Ratio
        -----------------------------------------------------------------
                py  |        19  |   100.00%  |      1132  |   100.00%

        Totally cost 0.11359143257141113 s.
```

以下是详细的使用说明。单击展开详细信息：

<details>
<summary><b>详细的使用说明</b></summary>

- [用法](#用法)
    - [`search`](#search)
      - [直接搜索给定的路径](#直接搜索给定的路径)
      - [同时搜索多个路径](#同时搜索多个路径)
      - [展示详细搜索信息](#展示详细搜索信息)
      - [搜索指定后缀的代码文件](#搜索指定后缀的代码文件)
      - [搜索时忽略指定的目录或文件](#搜索时忽略指定的目录或文件)
      - [指定搜索结果的保存路径](#指定搜索结果的保存路径)
      - [可视化统计结果](#可视化统计结果)
    - [`remote`](#remote)
      - [搜索并统计远端仓库的代码](#搜索并统计远端仓库的代码)
    - [`config`](#config)
      - [显示配置信息](#显示配置信息)
      - [重置配置信息](#重置配置信息)
      - [追加配置信息](#追加配置信息)
      - [删除配置信息](#删除配置信息)
      - [更新访问令牌](#更新访问令牌)
      - [恢复默认配置](#恢复默认配置)

## 用法

`code-counter` 的帮助信息如下。 

```shell 
$ cocnt --help
usage: cocnt <command> [<args>]
These are common Code-Counter commands used in various situations:
    search     Search and count code lines for the given path(s)
    remote     Search and count the remote repository
    config     Configure Code-Counter

A command-line interface (CLI) utility that can help you easily count code and display detailed results.

positional arguments:
  command     Subcommand to run, `search` or `config`

optional arguments:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
```

`code-counter` 支持 3 个子命令：[`search`](#search), [`remote`](#remote) 和 [`config`](#config)

### `search`

搜索给定的路径并统计，`cocnt search` 的帮助信息如下。

```shell
$ cocnt search --help
usage: cocnt search input_path [-h] [-v] [-g] [-o OUTPUT_PATH] [--suffix SUFFIX] [--comment COMMENT] [--ignore IGNORE]

Search and count code lines for the given path(s)

positional arguments:
  paths                 counting the code lines according to the given path(s)

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
        Total file lines    :    1420 (100.00%)
        Total code lines    :    1132 ( 79.72%)
        Total blank lines   :     252 ( 17.75%)
        Total comment lines :      36 (  2.54%)

              Type  |     Files  |     Ratio  |     Lines  |     Ratio
        -----------------------------------------------------------------
                py  |        19  |   100.00%  |      1132  |   100.00%

        Totally cost 0.11359143257141113 s.
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
$ cocnt search ./code-counter/ -v

        SEARCHING
        ====================
         File Type  |     Lines  |      Code  |     Blank  |   Comment  |  File Path
        ------------------------------------------------------------------------------------------
                py  |       156  |       126  |        28  |         2  |  ./code-counter/code_counter\conf\config.py
                py  |         0  |         0  |         0  |         0  |  ./code-counter/code_counter\conf\__init__.py
                py  |       183  |       154  |        23  |         6  |  ./code-counter/code_counter\core\args.py
                py  |        86  |        68  |        13  |         5  |  ./code-counter/code_counter\core\countable\file.py
                py  |        56  |        45  |         9  |         2  |  ./code-counter/code_counter\core\countable\iterator.py
                py  |         0  |         0  |         0  |         0  |  ./code-counter/code_counter\core\countable\__init__.py
                py  |       133  |       108  |        23  |         2  |  ./code-counter/code_counter\core\counter.py
                py  |        68  |        57  |         8  |         3  |  ./code-counter/code_counter\core\visualization.py
                py  |         0  |         0  |         0  |         0  |  ./code-counter/code_counter\core\__init__.py
                py  |        45  |        35  |         8  |         2  |  ./code-counter/code_counter\tools\progress.py
                py  |        63  |        51  |        10  |         2  |  ./code-counter/code_counter\tools\request.py
                py  |         0  |         0  |         0  |         0  |  ./code-counter/code_counter\tools\__init__.py
                py  |         1  |         1  |         0  |         0  |  ./code-counter/code_counter\__init__.py
                py  |        44  |        30  |        12  |         2  |  ./code-counter/code_counter\__main__.py
                py  |        52  |        44  |         6  |         2  |  ./code-counter/setup.py
                py  |       146  |       123  |        21  |         2  |  ./code-counter/tests\test_args.py
                py  |       327  |       244  |        81  |         2  |  ./code-counter/tests\test_config.py
                py  |        33  |        26  |         5  |         2  |  ./code-counter/tests\test_remote.py
                py  |        27  |        20  |         5  |         2  |  ./code-counter/tests\test_search.py

        RESULT
        ====================
        Total file lines    :    1420 (100.00%)
        Total code lines    :    1132 ( 79.72%)
        Total blank lines   :     252 ( 17.75%)
        Total comment lines :      36 (  2.54%)

              Type  |     Files  |     Ratio  |     Lines  |     Ratio
        -----------------------------------------------------------------
                py  |        19  |   100.00%  |      1132  |   100.00%

        Totally cost 0.11509132385253906 s.

```

#### 搜索指定后缀的代码文件

`code-counter` 有默认的配置，默认配置中包含了常见的代码文件后缀、注释符号以及需要忽略的目录或文件名。因此在使用的时候如果没有特别的需求，可以直接使用 `cocnt search` 进行代码的统计。

如果在搜索的时候，只想统计某一些特定的代码文件的情况，那么可以使用 `--suffix` 来指定代码文件后缀。比如：

```shell
$ cocnt search ./project --suffix="cpp,java"
```

当然，在搜索时也可以指定编程语言的注释符号，这有利于更好的统计代码中注释的数量。

```shell
$ cocnt search ./project --suffix="cpp,java" --comment="//,/*,*"
```

#### 搜索时忽略指定的目录或文件

在搜索代码文件的时候，容易统计到不想统计的代码文件或者目录，因此可以使用 `--ignore` 来指定在搜索时需要过滤的目录或者文件名。
c

一般来说，`code-counter` 的配置文件里已经包含了很多常见的默认配置，比如 `ignore` 的默认值如下所示。

```
"ignore": [
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

因此，如果在某些情况下，要搜索的目录或文件与 `ignore` 的默认值相同，那么可以通过设置 `--ignore=""` 来置空 `ignore` 的默认值，当然这是临时的。如果想要持久化这些修改，可以参考后面介绍 [`cocnt config`](#config) 时会提及的 [`--ignore-reset` 标志](#重置配置信息)。

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

### `remote`

搜索并统计远端 `Git` 仓库，`cocnt remote` 的帮助信息如下。

```shell
$ cocnt remote --help
usage: cocnt remote <repository> [-h] [-v] [-g] [-o OUTPUT_PATH] [--suffix SUFFIX] [--comment COMMENT] [--ignore IGNORE]

Search and count the remote repository with a given Github or Gitee HTTP link

positional arguments:
  repository            search and count a remote repository

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

`cocnt remote` 除了支持搜索远端仓库外，其各个标志的用法与 `cocnt search` 相同。

#### 搜索并统计远端仓库的代码

给定远端仓库的 HTTPS 或 SSH 链接，`code-counter` 就可以对远端仓库进行搜索，目前支持对 `Github` 和 `Gitee` 的仓库进行访问。

由于 `Github` 和 `Gitee` 的 API 访问次数限制，因此每天只有很少的使用次数。所以我们建议用户按照提示，在初次搜索时将 `Github` 或 `Gitee` 对应的访问令牌输入到 `code-counter` 中，这样每天至少有 5000 次的使用次数。

初次访问 `Github` 仓库时，会提示用户输入 `Github` 的访问令牌，访问 `Gitee` 的仓库也是一样的。 `code-counter` 会为不同的远端仓库展示不同的提示信息。
当然你不输入访问令牌也可以使用远端搜索的功能，但是当 API 使用次数达到上限时，`code-counter` 仍然会提示用户输入访问令牌，否则当天无法继续使用。

不同远端仓库的访问令牌的生成方式：
 + `Github`: [https://github.com/settings/tokens/new](https://github.com/settings/tokens/new)
   + 只需要在 `Select scopes` 中选择 `public_repo`、，然后点击 `Generate token` 生成令牌并把令牌输入到 `code-counter` 中即可
 + `Gitee`: [https://gitee.com/profile/personal_access_tokens/new](https://gitee.com/profile/personal_access_tokens/new)
   + 只需要选择 `projects` 并点击 `提交` 就可以生成访问令牌，然后把令牌输入到 `code-counter` 中即可

当输入了正确的访问令牌后就可以正常使用了。

```shell
$ cocnt remote https://github.com/InnoFang/code-counter.git

        RESULT
        ====================
        Total file lines    :    1403 (100.00%)
        Total code lines    :     997 ( 71.06%)
        Total blank lines   :     264 ( 18.82%)
        Total comment lines :     142 ( 10.12%)

              Type  |     Files  |     Ratio  |     Lines  |     Ratio
        -----------------------------------------------------------------
                py  |        18  |   100.00%  |       997  |   100.00%

        Totally cost 37.77419900894165 s.
```

如果想随时更新访问令牌，那么可以参考后面介绍 [`cocnt config`](#config) 时会提及的 [`--github-token` 和 `--gitee-token` 标志](#更新访问令牌)。

### `config`

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
$ cocnt config --suffix-reset="cpp,java" --comment-reset="//,/*,*" --ignore-reset="build,target"
'suffix' will be replaced with ['cpp', 'java'] . (y/n) y
'comment' will be replaced with ['//', '/*', '*'] . (y/n) y
'ignore' will be replaced with ['build', 'target'] . (y/n) y
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

#### 更新访问令牌

对于 `Github` 和 `Gitee` 的访问令牌的更新，`code-counter` 提供以下标志：
 + `--github-token` 更新 `Github` 的访问令牌
 + `--gitee-token` 更新 `Gitee` 的访问令牌

这两个标志可以组合使用，也可以单独使用。对于每个会修改配置文件的操作都会对你进行询问，此时你可以检查要修改的内容是否正确，如果确认修改可以输入 `y`，否则输入 `n` 不执行修改。

```shell
$ cocnt config  --github-token=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  --gitee-token=d7ca1490523aac54a38434bf96c76ff8
the old Github access token will be updated to `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` . (y/n) y
the old Gitee access token will be updated to `d7ca1490523aac54a38434bf96c76ff8` . (y/n) y
```

#### 恢复默认配置

使用 `--restore` 来恢复 `code-counter` 自带的默认配置。恢复默认配置不会重置访问令牌。

```shell
$ cocnt config --restore
The default configuration will be restored. (y/n) y
```

</details>

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
