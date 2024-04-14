from pwn import *

p = remote('127.0.0.1', 44296)

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

print(strxx)
