# Code Counter

Do you wander how many code you have been written? Come on, let's get count it.

## Usage

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

## Configuration

If you want to ignore some directories or add the file type you want to count, you make some configuration,
see [config.py](config.py)

```
config = {
    # Which suffix code file do you want to count?
    # more than as follow, also html, css, clj, lisp, etc.
    'suffix': ['py', 'java', 'c', 'cpp', 'js', 'pde', 'kt', 'dart'],

    # Ignore some directories or files which are not write by yourself
    # but generate by the projects, just add what you want to add.
    'ignore': ['out', 'venv', '.git', '.idea', 'build', 'target'],
}
```

**TIPS** `ignore` is important, the reason is that if you want to count how many code you have written 
and there are some code generate by the project automatically which is not belong to you, 
so ignore them is fair

## Example

#### Specify a file or directory path directly


```shell
$ python code-counter.py -p F:/Github/playground/Python/line-counter

	SEARCHING
	====================
    File Type  |   Line of File  |   Code of File  |  Space of File  |  File Path
	----------------------------------------------------------------------------------------------------
           py  |            134  |            110  |             24  |  F:/Github/playground/Python/line-counter\line-counter.py

	RESULT
	====================
	          Item           |  File Count   |  File Ratio   |  Code Count   |  Code Ratio   
	------------------------------------------------------------------------------------------
	Total line of files      |     ----      |     ----      |      134      |    100.00%    
	Total line of codes      |     ----      |     ----      |      110      |    82.09%     
	Total line of space      |     ----      |     ----      |      24       |    17.91%     
	For '.py' files          |       1       |    100.00%    |      110      |    100.00%    

	Totally cost 0.0005002021789550781s.

```

#### Use a file with a list of files or directories path as input

Firstly, create a file named `file.txt` or whatever you like,
which contain a list of files or directories path, just as follow:

```
F:\Android\
F:\Github\code-counter\
...
```
then use it as input:

```shell
$ python code-counter.py -i F:/Github/playground/Python/line-counter
```

Use a path or a file as input is your free, but choose one of them is enough.
If you choose both of them at the same time, the `path` will be cover the `file` 

#### Also, you can specify a output path

Just like this

```shell
$ python code-counter.py -p F:/Github/playground/Python/line-counter -o result.txt
$ python code-counter.py -i F:/Github/playground/Python/line-counter -o output.txt
```

the output path is optional.