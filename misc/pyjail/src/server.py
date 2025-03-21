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