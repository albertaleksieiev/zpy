Zpy shell
=================
![ZpyContent](https://github.com/albertaleksieiev/zpy/raw/content/img/screenshot-1.png)
**Next level command line shell with script languages, like python or js. Work in shell with your favorite language.**
```
(Zpy) pwd | "Current folder %s" % z | cat
Current folder /Users/XXXX/pytho-nal
(Zpy) j request = require('request')
(Zpy) j ['New York', 'Paris', 'London', 'Berlin', 'San Francisco'] 
      |[for] j request(`http://weathers.co/api.php?city=${z}`, (err,res,body) => sync(JSON.parse(body).data)) 
      |j z.map((data) => `${data.location} has temperature ${data.temperature} °F`) 
      |[for] echo $z >> weather.txt
['', '', '', '', '']
(Zpy) cat weather.txt
New York has temperature -7 °F
Paris has temperature -7 °F
London has temperature -7 °F
Berlin has temperature 4 °F
San Francisco has temperature 24 °F
```


### Pipeline
Zpy ideology says - pipeline make work in terminal great again! Pipeline play the major role in zpy. If you want to use every opportunity of Zpy you should know a few things about the pipeline. Input command will be splited by pipeline character, each of token will be evaluated by shell,python or js interpreter, and tokens will be chained into 1 chain. Zpy pass previous token evaluation result as stdin to next token and you have access to z-variable if token not expects to stdin. So Zpy pipes work like standard unix pipes.

### Syntax
If you want use Zpy you should a few rules.
 * Command will be evaluated by **unix system** if you add **`** symbol in begin of the token, or you command begin with [142 linux commands](http://www.mediacollege.com/linux/command/linux-command.html)
 * Command will be evaluated by [**javascript**](#javascript) language if you add `j` at begining of token. 
 * Command will be evaluated by [**Chain Pool**](#chain-pool) if you add specific characters like `for` in the begin the line.
 * Command will be evaluated by [**python**](#python) command **in any other case**(by default just evaluate python code - python is default language)
 
#### From Python to Unix 
```
(Zpy) "\n".join(["Zpy so awesome #review #1e%s"%i for i in range(10)]) | grep "5\|6\|8"
Zpy so awesome #review #1e5
Zpy so awesome #review #1e6
Zpy so awesome #review #1e8
```
Generate array with text joined with number from zero to ten, join it by using `\n` character, that we can use it in **unix pipe** cause grep use data splited by `\n` characher. Filtering results by using **grep** command, show only string which contrains 5,6 or 8 digits.
```
(Zpy) "%s.%s" % ('index','php') | cat $z
cat: index.php: No such file or directory
(Zpy) "%s.%s" % ('index','cpp') | touch $z
```
Generate "index.php" as z-value, and send it to next pipe. Last pipe will be evaluated by unix system, we have access to z-variable as like path variable or stdin. So you can write `$z` to access variable `...|touch $z` or stdin `...|grep "index"`.
#### From Unix to Python
```
(Zpy) ls | z.split('\n') | filter(lambda x : 'index' in x, z) | list(z)
['index.py']
```
Get current files, convert it into array and filter it by some condition
We have access to z-variable as `z`.
#### From (Unix or Python) to Js and back
As you can see abowe, we have access to `z` variable from unix or python just use `z` or `$z` variables, this rule works the same way in js. 
```
(Zpy) 'http://weathers.co/api.php?city=New+York' | j req(z, (err,res,body) => sync(body)) | j JSON.parse(z).data | "Today is %s and current temperature %s" % (z['date'], z['temperature'])
Today is 03-12-2017 and current temperature -14
```
`python` -> `javascript`-> `javascript`->  `python` 
Get current temperature and date from weather.co.
**Note** here we use `sync` function from javascript, this command will send data from **Async** function call (see description in javascript section).

#### Salad of languages
```
(Zpy) j [1,2,3,4].map((e) => `js ${e}`) | ["python + %s" %x for x in z] | "\n".join(z) | sed -e 's/$/ + bash = Zpy/'
python + js 1 + bash = Zpy
python + js 2 + bash = Zpy
python + js 3 + bash = Zpy
python + js 4 + bash = Zpy
```
How about dah? `javascript` -> `python` -> `bash`

### Requirements
* Python 3
* pip3
* compgen
* nodejs or any other js runtime.

### Install
Install via pip
```
pip3 install zpyshell
```
Install from github sources:
```
git clone git@github.com:albertaleksieiev/zpy.git
cd zpy;pip3 install -r requirements.txt
```
If you want use power of js, install [nodejs](https://nodejs.org/en/). 

### Run
If you install zpy via pip just run in terminal
```
$ zpy
```
But if you install from sources, navigate to repository root folder and run it like python script
```
python3 Zpy/main.py   
```
### Test
```
python3 tests/main_test.py
```

-----
## Languages
Currently zpy support 3 languages
* [Python](#python)
* [Javascript](#javascript)
* Unix shell script
* [Chain Pool](#chain-pool) (additional language)

### More languages
 Now Zpy supports python and js, but in the first release, we will add more languages!
 
## Python
Zpy written in python, so python it's the first language which was be added and supported.
* [Imports](#python-imports)
* [Default imports](#default-imports)
* [Own modules](#adding-new-module)
  * [Create python module](#1create-python-module)
  * [Import module](#2add-module-to-zpy)
  * [Advanced usage pipe and module](#3processing-input-from-pipe)


### Python Imports
If you wan't import some modules into zpy, just add `~` in the begging and type your import command.
```
(Zpy) ~import random,os
(Zpy) ~from PIL import Image
(Zpy) find /Users/XXXX/Pictures -name "*.jpg" | z.split('\n') | z[random.randint(0,len(z))] | Image.open(z).show()
```
Show random Image from your Pictures folder. 
**Note: change /Users/XXXX/Pictures to your folder with images**
```
(Zpy) ~import os
(Zpy) pwd | os.listdir(z)
['__pycache__', 'a.txt', 'index.py', 'linux-command-to-list-all-available-commands-and-aliases', 'README.md', 'Zpy']
(Zpy) ~from Zpy.Utils import get_linux_commands
['adduser', 'arch', 'awk', 'bc', 'cal', 'cat', 'chdir', 'chgrp', 'chkconfig', 'chmod', 'chown', 'chroot', 'cksum', 'clear', 'cmp', 'comm', 'cp', 'cron', 'crontab', 'csplit', 'cut', 'date', 'dc', 'dd', 'df', 'diff', 'diff3', 'dir', 'dircolors', 'dirname', 'du', 'echo', 'ed', 'egrep', 'eject', 'env', 'expand', 'expr', 'factor', 'FALSE', 'fdformat', 'fdisk', 'fgrep', 'find', 'fmt', 'fold', 'format', 'free', 'fsck', 'gawk', 'grep', 'groups', 'gzip', 'head', 'hostname', 'id', 'info', 'install', 'join', 'kill', 'less', 'ln', 'locate', 'logname', 'lpc', 'lpr', 'lprm', 'ls', 'man', 'mkdir', 'mkfifo', 'mknod', 'more', 'mount', 'mv', 'nice', 'nl', 'nohup', 'passwd', 'paste', 'pathchk', 'pr', 'printcap', 'printenv', 'printf', 'ps', 'pwd', 'quota', 'quotacheck', 'quotactl', 'ram', 'rcp', 'rm', 'rmdir', 'rpm', 'rsync', 'screen', 'sdiff', 'sed', 'select', 'seq', 'shutdown', 'sleep', 'sort', 'split', 'su', 'sum', 'symlink', 'sync', 'tac', 'tail', 'tar', 'tee', 'test', 'time', 'touch', 'top', 'traceroute', 'tr', 'TRUE', 'tsort', 'tty', 'umount', 'uname', 'unexpand', 'uniq', 'units', 'unshar', 'useradd', 'usermod', 'users', 'uuencode', 'uudecode', 'vdir', 'watch', 'wc', 'whereis', 'which', 'who', 'whoami', 'xargs', 'yes']
 ```
Print all linux commands defined in zpy.
#### Default imports
If you don't want import general modules like `os` every time when you launch zpy, you can use **default imports**
You just need execute zpy method `add_def_imports`.
```
(Zpy) zpy.add_def_imports("numpy","import numpy as np")
(Zpy) zpy.get_def_imports()
numpy => import numpy as np
```
Done! When you launch Zpy, this modules will be imported automatically. Let's try evaluate something.
```
(Zpy) np.arange(20)
[ 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19]
(Zpy) np.arange(20) | np.std
5.76628129734
```
**Note** Here we use np.std without input arguments, Zpy will pass z-value as 1 argument to function and evaluate it.
Function will be evaluated with z parameter as argument by default, if return type of evaluation is function. 
#### Modules
Zpy have some cool things, like modules! Modules is your own script which will be imported by default. Zpy have own zpy module.
```
(Zpy) zpy
<Zpy.languages.zpy.zpy object at 0x10268d2e8>
```
zpy is just python class, which can storage some information (like scripts).
zpy Methods : 
- get_scripts() - return list of scripts
- add_script(name) - Currying `add_new_script` method, returns `add_new_script(name=name)` 
- add_new_script(name, script) - create new script
- remove_script(name) - remove script
- eval(name, input='') - eval script and send input
- eval_with_input(name) - Currying `eval` method, returns `eval(name=name)`
- last_zcommand() - return last z-command. **Note** after evaluation `last_zcommand()` method and value returns,, last z-command will be `last_zcommand()`
- add_module(module_name, path_to_module_file_py) - add module, it will be available from zpy like `module_name`
- get_modules() - returns all modules
- remove_module(name) - remove module by name, **file will not be deleted**
- as_table(data) - trying to convert string to table data
```
(Zpy) zpy.get_scripts()
(Zpy) zpy.add_new_script("ls", "ls -lah")
(Zpy) zpy.get_scripts()
ls => ls -lah
(Zpy) zpy.eval('ls')
total 408
drwxr-xr-x   9 albert  staff   306B Feb 27 22:29 .
drwxr-xr-x  33 albert  staff   1.1K Feb 24 22:47 ..
drwxr-xr-x   8 albert  staff   272B Feb 27 22:36 .idea
-rw-r--r--   1 albert  staff   6.1K Feb 27 22:13 README.md
drwxr-xr-x   7 albert  staff   238B Feb 27 22:35 Zpy
-rw-r--r--   1 albert  staff   685B Feb 27 22:25 index.py
-rw-r--r--   1 albert  staff   182K Feb  1 20:00 linux-command-to-list-all-available-commands-and-aliases
-rw-r--r--   1 albert  staff    36B Feb 27 15:47 random.file
-rw-r--r--   1 albert  staff    24B Feb 27 22:13 zpy.conf
```
Some advanced stuff
```
(Zpy) ~import requests, json
(Zpy) requests.get('http://finance.google.com/finance/info?client=ig&q=NSE:HDFC') | z.text | z.replace('//','') | json.loads(z)[0] | z['pcls_fix']
1375.7
(Zpy) zpy.last_zcommand()
requests.get('http://finance.google.com/finance/info?client=ig&q=NSE:HDFC') | z.text | z.replace('//','') | json.loads(z)[0] | z['pcls_fix']
(Zpy) zpy.last_zcommand()
zpy.last_zcommand()
(Zpy) requests.get('http://finance.google.com/finance/info?client=ig&q=NSE:HDFC') | z.text | z.replace('//','') | json.loads(z)[0] | z['pcls_fix']
1375.7
(Zpy) zpy.last_zcommand() | zpy.add_script("Get stock NSE:HDFC")
(Zpy) zpy.eval('Get stock NSE:HDFC')
1375.7
```
#### Adding new module
You may want to add the module to Zpy functionality written in python, in Zpy you can do this in few steps
##### 1)Create python module

```
(Zpy) pwd
/path
(Zpy) cd to
(Zpy) pwd
/path/to
(Zpy) ['def square(a):','\treturn a * a'] | "\n".join(z) | cat > some_module.py
(Zpy) cat some_module.py
def square(a):
    return a * a
```
##### 2)Add module to Zpy
Run zpy method `add_module` from zpy python module.
 ```
(Zpy) zpy.add_module("some_model","/path/to/some_module.py"
 ```
Or edit **zpy.conf** file - add name and py file location to [MODULE] section :
```
....
[MODULE]
....
some_model = /path/to/some_module.py
```
*zpy.conf*

And try evaluate method from some_module
```
(Zpy) some_module.square(4)
16
```
##### 3)Processing input from pipe
Passing pipe output to your module function - really easy. You just need declare `zpy_input` in your function argument list :
```
def square(a):
    return a * a
def square_from_pipe(zpy_input):
   return square(zpy_input)
```
*some_module.py*
```
(Zpy) 12 | some_module.square_from_pipe
144
```
Also, we can use currying if we want implement pow function, we should pass 2 variables - base value and exponent value. But pipe can send only 1 variable, we can pass them as string array and parse them inside our function **OR** we can use carrying,
```
import math
def square(a):
    return a * a

def square_from_pipe(zpy_input):
   return square(zpy_input)
   
def power(base, exponent=None):
    if exponent is None:
        def currying_function(zpy_input):
            return math.pow(base, zpy_input)

        return currying_function
    else:
        return math.pow(base, exponent)
```
*zpy.conf*
Universal function power is done! Let's test it
```
(Zpy) some_module.power(2)(2)
4.0
(Zpy) some_module.power(2)(4)
16.0
(Zpy) 5 | some_module.power(2)
32.0
```

## Javascript
Javascript one of the most popular language ever, so zpy work with them. You can use nodejs with some features like File System I/O, or other JS runtime. Special thanks for [PyExecJS](https://github.com/doloopwhile/PyExecJS)! Zpy use this module inside, so you can see the full list of available runtimes in the link above.
Everybody knows javascript use async functions, this is a problem cause pipes do not works async. This problem will be solved bu using [`sync`](#sync-function) or [`sync_err`](#sync_err) functions.
* [Syntax](#js-syntax)
* [Imports](#js-imports)
  *  [Default imports](#js-default-imports)
* [Async](#async-to-sync)
  * [`sync` function](#sync-function)
  * [`sync_err` function](#sync_err)

### JS Syntax
Command will be evaluated by **javascript** command if you add `j` at begining of token. 
```
(Zpy) j 2 + 3
5
```
### JS Imports
If you wan't import some modules into js chain, use `require`.
```
npm i request --global
...
(Zpy) j request = require('request')
Added new requirements : { [['request', 'request']] }
```
**Note** your modules should be installed globaly 
##### JS Default imports
If you want import general modules like `request` every time when you launch Zpy, you can use **default imports**.
You just need execute method `add_def_imports` from `zjs` object.
```
(Zpy) zjs.add_def_imports('request', 'require("request")')
(Zpy) zjs.get_def_imports()
request => require("request")
```
Done!
### Async to Sync
As I wrote above, we should have ability going from async function to sync function, but why we cannot use async without any modification? If we want make a request and after request send data to next chain, request should be fineshed before we go to next chain.
```
(Zpy) j [1,2,3].join("-") | z.split("-")
['1', '2', '3'] //It's work great! Cause js chain not async.
(Zpy) j request('http://weathers.co/api.php?city=New+York', (err,res,body) => "") 
{'method': 'GET', 'uri': {'auth': None, 'path': '/api.php?city=New+York', 'host': 'weathers.co', 'hostname': 'weathers.co', 'hash': None, 'query': 'city=New+York', 'protocol': 'http:', 'port': 80, 'search': '?city=New+York', 'href': 'http://weathers.co/api.php?city=New+York', 'pathname': '/api.php', 'slashes': True}, 'headers': {'host': 'weathers.co'}}
```
As we can see result of evaluation request function is object with request properties like href, headers, host etc. Zpy trying convert it to JSON format. If result of evaluation is `function` and this function has attribute `skip_print='zkip_'` zpy skip result of evaluation  (it will be helpfull in async function calls). **Zpy do not return evaluation result if this is a func and func has properties `skip_print='zkip_'` or we use `sync`, `sync_err` function call.**
#### `sync` function
`sync` command will send data from **Async** function call and finish current chain. It's realy easy to use.
```
(Zpy) j request('http://weathers.co/api.php?city=New+York', (err,res,body) => sync(body)) | "Python retreive requests results from js `%s`" %z
Python retreive requests results from js `{"apiVersion":"1.0", "data":{ "location":"New York", "temperature":"-14", "skytext":"Light snow", "humidity":"64", "wind":"7.56 km/h", "date":"03-12-2017", "day":"Sunday" } }`
```
#### `sync_err`
Throw error from async function call.
```
(Zpy) j setTimeout(function(){ sync_err('SOME ERROR') },200)
Traceback (most recent call last):
  File ....
  ...
  execjs._exceptions.ProgramError: SOME ERROR
```


## Chain Pool
Chain pool is programming language which have a lot of usefull functions inside Zpy. To start use functions like `[for]` just type this keyword after pipe character `|`, like `|[for]`. Square brackets` []` indicate *Chain pool* function `for`. Chain pool take **stdin** as input stdin, and do some work with stdin, what work you enter after `|[CHAIN_FUNCTION]` keyword, you can use your **favorite language** with Chain pool function.
### `[for]` function
`[for]` function iterate throught every item in *array* or *data splited by `\n`* character as stdin and evaluate every iterated item by any other language.
#### Syntax
**`[`** `for` **`]`** `any other language command`, where `[]` is *Chain pool* syntax, `for` - for function. 
![Chain pool [for] function](https://raw.githubusercontent.com/albertaleksieiev/zpy/content/img/Chain%20Pool%20%5Bfor%5D%20function.jpg)

Here we generate data by python, simply by typing array initialization keyword, after that we use `[for]` keyword, split this array to 2 stdin arguments, evaluate shell function `ls` for every argument ('folder1' and 'folder2') and finally join result into array, and send into next chain. And in the last chain we just concatenate array by `,` character.
```
(Zpy) ['.', '..'] |[for] ls $z | ','.join(z)
LICENSE.txt
README.md
Zpy ...., parent_folder content
```


#### Examples
```
(Zpy) ~import os
(Zpy) pwd | os.listdir(z) | "Files divided by commma %s" % ",".join(z)
Files divided by commma .idea,__pycache__,a.txt,index.py,linux-command-to-list-all-available-commands-and-aliases,README.md,Zpy
```
Get current directory using shell command, pipe into python code as z-variable and print result of last chain
```
(Zpy) ~from terminaltables import AsciiTable, SingleTable
(Zpy) ls -lah | z.split('\n') | [' '.join(x.split()).split(' ') for x in z] | SingleTable(z).table
┌────────────┬────┬────────┬───────┬──────┬─────┬───┬───────┬────────────────┐
│ total      │ 8  │        │       │      │     │   │       │                │
├────────────┼────┼────────┼───────┼──────┼─────┼───┼───────┼────────────────┤
│ drwxr-xr-x │ 4  │ albert │ staff │ 136B │ Mar │ 4 │ 23:32 │ .              │
│ drwxr-xr-x │ 10 │ albert │ staff │ 340B │ Mar │ 4 │ 23:34 │ ..             │
│ -rw-r--r-- │ 1  │ albert │ staff │ 0B   │ Mar │ 4 │ 23:32 │ empty_file.txt │
│ -rw-r--r-- │ 1  │ albert │ staff │ 9B   │ Mar │ 4 │ 23:32 │ not_empy.txt   │
│            │    │        │       │      │     │   │       │                │
└────────────┴────┴────────┴───────┴──────┴─────┴───┴───────┴────────────────┘
```
Convert ugly result after evaluation `ls -lah` to great table!
**Note** This functionality available inside zpy module `ls -lah | zpy.as_table`

```
(Zpy) ~import numpy as np
(Zpy) np.arange(10).reshape(2,5).tolist() |[for] [for] z**2
[[0, 1, 4, 9, 16], [25, 36, 49, 64, 81]]
```
Iterate every row and column and change every value, by `power` function.

```
(Zpy) ['http://google.com','http://yandex.ru'] |[for] j request(z, (err,res,body) => sync(body))
```

```
(Zpy) `wget -qO- http://example.com | z.split(" ") | filter(lambda x : "head" in x,z) | list(z) 
['html>\n<html>\n<head>\n', '\n</head>\n\n<body>\n<div>\n']
(Zpy) `wget -qO- http://example.com | z.split(" ") | filter(lambda x : "head" in x,z) | list(z) | "Total size : %s" % len(z) 
Total size : 2
```
Download content from page and count current entrance word 'head'
```
(Zpy) find ./ -name "*.py" | z.split("\n")[:2]
['.//index.py', './/Zpy/languages/LanguageAnalyzer.py']
(Zpy) find ./ -name "*.py" | z.split("\n")[:2] | "\n".join(z) |grep "an"
.//Zppy/languages/LanguageAnalyzer.py
```
First evaluation will find file in current directory and get first 2 results. Second evaluation do the same plus filter results by shell command `grep`
```
(Zpy) ~import re
(Zpy) "https://www.reddit.com/r/books/" | `wget -qO- $z |  re.findall(r"Book[^\.].*?",z,re.IGNORECASE) | "COUNT : %s" % len(z)
COUNT : 645
```
```
(Zpy) ~import uuid
(Zpy) uuid.uuid4() | str(z) | cat > random.file
(Zpy) cat random.file
7ff48f51-b31d-44c2-9aaf-428a63099739
```

### **Danger tricks** (Do not evaluate)
```
(Zpy) ~from Zpy.Utils import get_linux_commands

(Zpy) ~import random,os

(Zpy) get_linux_commands() | z[random.randint(0,len(z))] | os.system(z)
staff com.apple.sharepoint.group.1 everyone localaccounts _appserverusr admin _appserveradm _lpadmin _appstore _lpoperator _develope...
```
Get all shell commands declared in Zpy, and execute random one

```
(Zpy) ~import random,os

(Zpy) ['you are lucky','displaysleepnow','lock'] | z[random.randint(0,len(z))] | os.system("pmset %s" %z)
0
```
If you run on OSX, 33% nothing happens
### License
The module is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).
