## math？

这题实际上跟数学没啥关系，实际上是利用python的递归深度进行侧信道攻击

我们知道python默认的递归深度是1000层，我们希望能够通过让pow不断递归触发error来实现攻击

首先看看getbit函数，`flag[i // 8] & (1 << (i % 8))`表示flag的第i个比特，b是我们对第i个比特的猜测，而a是一个比较重要的数
$$
g^{a*2^{b\bigoplus{第i个比特}}}
$$
如果对b猜测正确，那么上面的式子就会变成
$$
g^{a}
$$
否则变成
$$
g^{2a}
$$
我们再回去看pow函数，决定其递归深度的实际上就是指数，而a和2a仅仅差一个比特长度，也就是只差一次递归。那么如果我们能找到一个a，在猜测正确的情况下，它使得程序的递归深度刚好是1000，不会触发error，而如果猜测错误，指数变成了2a，比a的比特长度多了1，进而导致递归深度超过了1000引发error，那么我们就能够通过程序是否报错来判断flag的第i个比特是0还是1，从而求出完整的flag



这个a必然是在
$$
2^{1000}
$$
附近，但因为程序中其它的函数调用，实际上会小一些。

经过尝试，
$$
2^{990}
$$
刚好满足我们的要求，因此我们直接通过回传的消息是否含有报错即可求出flag的第i个比特，遍历整个flag即可得到完整的flag

~~~python
from pwn import *

p = remote('127.0.0.1', 44296)#改成你的端口

strxx = ""
for _ in range(11):
    a = p.recvline()
    #print(a)
print("-------------------")
def getbytes(nthbytes):
    nthbits = 8 * nthbytes
    strbin = ""
    for i in range(nthbits, nthbits + 8):
        bit=b'0'

        for _ in range(4):
            a = p.recvline()
            #print(a)

        p.sendline(b'1')
        a = p.recvline()
        #print(a)

        to_send = "%s" % i
        p.sendline(to_send.encode())
        a = p.recvline()
        #print(a)

        p.sendline(bit)
        a = p.recvline()
        #print(a)

        magicalnum=2**990
        to_send = "%s" % magicalnum
        p.sendline(to_send.encode())
        a = p.recvline()
        #print(a)

        if a==b'Something Wrong?\n':
            strbin += '1'
            continue
        else:
            strbin += '0'
            continue

    return chr(int(strbin[::-1], 2))

for i in range(45):
    strxx += getbytes(i)
    print("str=", strxx, i)
~~~



