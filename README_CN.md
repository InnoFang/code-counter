# Code Counter

一个可以帮助你轻松地统计代码并显示详细结果的命令行界面（CLI）小工具。

[English](https://github.com/InnoFang/code-counter/blob/master/README.md) | 中文

## 安装

使用 PyPI 安装 ( 暂未上传 PyPI ) :

```shell
pip install code-counter
```

也可以使用源码进行安装

```shell
git clone https://github.com/innofang/code-counter.git
cd code-counter/
python setup.py install
```

## 快速开始

切换到任意代码目录下 ( 比如 `code-counter` ) ，并键入如下命令

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

更多使用方法请参考 [用法](#usage) 和 [案例](#example)。 

<h2 id="usage">用法</h2>


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

<h2 id="example">案例</h2>

### 直接指定文件或目录路径

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

### 多路径输入（使用一个包含文件或目录路径列表的文件作为输入）

创建一个文件，比如叫 `list.txt`，该文件将包含多个文件或目录路径，如下所示

```
F:/Github/miscode
F:/IDEA/jokul
```

然后使用 `[-l --list]` 来指定 `list.txt` 是包含路径列表的文件：

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

### 展示详细搜索信息

搜索信息默认是不显示的。如果你比较关注搜索信息，可以使用 `[-v --verbose]` 来查看它：


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


### 指定输出路径

通过 `[-o --output]` 来指定输出路径，如果制定了输出路径，那么输出信息将不会显示在控制台，如下所示：

```shell
$ codecount ./code-counter -v -o ./result.txt

        Totally cost 0.012001991271972656s.

```

详细的搜索信息和结果将写入到 `./result.txt` 中
### 可视化统计结果

数据可视化可以给我们更直观的感受，所以我提供了将统计结果可视化的指令 `[-g --graph]`。使用示例如下：

```
$ codecount list.txt -l -g
```

除了显示文本统计数据之外，还会展示如下图的的统计图表

![](https://cdn.jsdelivr.net/gh/innofang/jotter/source/code-counter/result.png)


## 配置

默认的配置文件 `config.json` 如下所示:

```json
{
    "suffix": ["py", "java", "c", "h", "cpp", "hpp", "js", "pde", "kt", "dart", "go", "lisp", "cu", "cuh"],
    "comment": ["#", "//", "/*", "*", ":", ";"],
    "ignore": ["out", "venv", ".git", ".idea", "build", "target", "node_modules", ".vscode"]
}
```

 + **`suffix`**: 你想统计的代码文件的后缀
 + **`comment`**: 注释符号，用来判断当前行是否是注释
 + **`ignore`**: 忽略一些你不想统计的目录或文件

> **注意**
> 
> + 对于 **`suffix`**, 举例来说, `Python` 文件的后缀是  `py`, `C++` 文件的后缀是 `cpp`
> + 对于 **`ignore`**, 如果你想统计你写了多少代码，但存在一些项目自动生成的代码，那么忽略掉这些生成代码会使统计结果更准确
> + 对于 **`comment`**, 如果某一行注释位于两个注释符号之间，并且该行开头没有其它注释符号作为标记，那么这一行的内容可能会被误判，比如将该行注释识别为代码

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
