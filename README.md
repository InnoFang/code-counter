# Code Counter

A command-line interface (CLI) utility that can help you easily count code lines and display detailed results.

English | [中文](./README_CN.md)

## Installation

Install by PyPI:

```shell
pip install code-counter
```

Also, you can install it from the source code: 

```shell
git clone https://github.com/innofang/code-counter.git
cd code-counter/
pip install -r requirements.txt
python setup.py install
```

## Quick Start

Open the terminal and directly search the path you want to count.

For example, use `cocnt search` to count the number of code lines of `code counter`. (`cocnt` is the abbreviation of `code count`)

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

The following is the detailed usage instructions. Click to expand the details:

<details>
<summary><b>The detail usage instructions</b></summary>

* [Usage](#usage)
    + [`search`](#search)
      - [Search the given path directly](#search-the-given-path-directly)
      - [Search multiple paths at the same time](#search-multiple-paths-at-the-same-time)
      - [Show verbose searching information](#show-verbose-searching-information)
      - [Search code files for specific file suffixes](#search-code-files-for-specific-file-suffixes)
      - [Ignore directories or files during the search](#ignore-directories-or-files-during-the-search)
      - [Specify the output path to save the search results](#specify-the-output-path-to-save-the-search-results)
      - [Visualize statistical results](#visualize-statistical-results)
    + [`remote`](#remote)
      - [Search and count the remote repository](#search-and-count-the-remote-repository)
    + [`config`](#config)
      - [List configuration information](#list-configuration-information)
      - [Reset the value of the configuration variable](#reset-the-value-of-the-configuration-variable)
      - [Add the value of the configuration variable](#add-the-value-of-the-configuration-variable)
      - [Delete some configuration variable values](#delete-some-configuration-variable-values)
      - [Update the access tokens](#update-the-access-tokens)
      - [Restore default configuration](#restore-default-configuration)

## Usage

The help information of `code-counter ` is as follows.

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

`code-counter ` supports three subcommands: [`search`](#search), [`remote`](#remote), and [`config`](#config)

### `search`

Search the given path and make statistics. The help information of `cocnt search` is as follows.

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

#### Search the given path directly

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


#### Search code files for specific file suffixes

`code-counter` has a default configuration, which includes common code file suffixes, comment symbols, and directory or file names that need to be ignored. Therefore, if there are no special requirements during use, you can directly use `cocnt search` for code statistics.

If you only want to count some specific code files when searching, you can use the `--suffix` to specify the code file suffix. For example:

```shell
$ cocnt search ./project --suffix="cpp,java"
```

Of course, specify the comment symbols during searching the code, which is helpful to count the number of comments in the code.

```shell
$ cocnt search ./project --suffix="cpp,java" --comment="//,/*,*" --ignore="target,build"
```

#### Ignore directories or files during the search

During the search, it is easy to count the code files or directories that you do not want to count, so you can use the `--ignore` to specify the directory or file names that need to be ignored during the search.

```shell
$ cocnt search ./project --suffix="py,java" --comment="#,//,/**" --ignore="target,__pycache__"
```

Generally speaking, the configuration file of `code-counter` already contains many common default configurations. For example, the default value of `ignore` is shown below.

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

Therefore, in some cases, if the directory or file to be searched is the same as the default value of `ignore`, you can set `--ignore=""` to empty the default value of `ignore`. Of course, this is temporary. If you want to persist with these changes, you can refer to the [`--ignore-reset` flag](#reset-the-value-of-the-configuration-variable) mentioned later when introducing [`cocnt config`](#config).

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

### `remote`

Search and count the remote `Git` repository, the help information of `cocnt remote` is as follows.

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

`cocnt remote` in addition to supporting the searching of the remote repository, the usage of its various flags is the same as `cocnt search`

#### Search and count the remote repository

Given the `HTTPS` or `SSH` link of the remote repository, `code-counter` can search and count the remote repository.
At present, it supports access to the repository of `Github` and `Gitee`.

Because of the API access limit for `Github` and `Gitee`, they are only used a very small number of times per day. 
So we recommend that users follow the instructions and enter the access token corresponding to `Github` or `Gitee` into `code-counter` during the initial search to get at least 5000 uses per day.

When first accessing a `Github` repository, the user is prompted for a `Github` access token, and the same is true for accessing a `Gitee` repository. `code-counter` will display different prompts for different remote repositories.
Of course, you can use the remote search feature without entering an access token, but when the API usage limit is reached, `code-counter` will still prompt the user for an access token, otherwise you will not be able to continue using it that day.

The access tokens for different remote repositories are generated as follows.
 + `Github`: [https://github.com/settings/tokens/new](https://github.com/settings/tokens/new)
   + Just select `public_repo` in `Select scopes`, then click `Generate token` to generate the token and enter it into `code-counter`.
 + `Gitee`: [https://gitee.com/profile/personal_access_tokens/new](https://gitee.com/profile/personal_access_tokens/new)
   + Just select `projects` and click `Submit` to generate the access token and enter it into `code-counter`

Once the correct access token has been entered it will work properly.

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

If you want to update the access token at any time, then you can refer to the [`--github-token` and `--gitee-token` flags](#update-the-access-tokens) that will be mentioned later in the introduction of [`cocnt config`](#config).

### `config`

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

These 3 flags can be used in combination or separately. You will be asked for each operation that will modify the configuration file, you can check if what you want to change is correct. If you confirm the change you can enter `y`, otherwise enter `n` to not perform the change.

Multiple values can be separated by commas, as shown in the following example.

```shell
$ cocnt config --suffix-reset="cpp,java" --comment-reset="//,/*,*" --ignore-reset="build,target"
'suffix' will be replaced with ['cpp', 'java'] . (y/n) y
'comment' will be replaced with ['//', '/*', '*'] . (y/n) y
'ignore' will be replaced with ['build', 'target'] . (y/n) y
```

#### Add the value of the configuration variable

For the case of adding the value of the configuration variable, the following flags can be used:
 + `--suffix-add` add code file suffixes
 + `--comment-add` add comment symbols
 + `--ignore-add` add the directories or files to ignore

These 3 flags can be used in combination or separately. You will be asked for each operation that will modify the configuration file, you can check if what you want to change is correct. If you confirm the change you can enter `y`, otherwise enter `n` to not perform the change.

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

These 3 flags can be used in combination or separately. You will be asked for each operation that will modify the configuration file, you can check if what you want to change is correct. If you confirm the change you can enter `y`, otherwise enter `n` to not perform the change.

Multiple values can be separated by commas, as shown in the following example.

```shell
$ cocnt config --suffix-del="clj,lisp" --comment-del=";" --ignore-del="build,target"
'suffix' will remove ['clj', 'lisp'] . (y/n) y
'comment' will remove [';'] . (y/n) y
'ignore' will remove ['build', 'target'] . (y/n) y
```

#### Update the access tokens

For updates to access tokens for `Github` and `Gitee`, `code-counter` provides the following flags.
 + `--github-token` update the access token for `Github`
 + `--gitee-token` update the access token for `Gitee`

These 2 flags can be used in combination or separately. You will be asked for each operation that will modify the configuration file, you can check if what you want to change is correct. If you confirm the change you can enter `y`, otherwise enter `n` to not perform the change.

```shell
$ cocnt config  --github-token=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  --gitee-token=d7ca1490523aac54a38434bf96c76ff8
the old Github access token will be updated to `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` . (y/n) y
the old Gitee access token will be updated to `d7ca1490523aac54a38434bf96c76ff8` . (y/n) y
```

### Restore default configuration

Use the `--restore` flag to restore the default configuration of `code-counter`.

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
