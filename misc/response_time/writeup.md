# Response Time

其实也算是个签到题，不过没多少人做/(ㄒoㄒ)/~~

使用nc(netcat)连接之后，尝试输入flag头，猜测出每次输入时，如果当前位输入正确，输出响应的时间就会较长，然后会进入下一位的输入检测判断。

为了方便大家理解，我在此贴出服务端代码：

```python
import time
import os
banner ='''
                                                                                       /$$     /$$
                                                                                      | $$    |__/
  /$$$$$$   /$$$$$$   /$$$$$$$  /$$$$$$   /$$$$$$  /$$$$$$$   /$$$$$$$  /$$$$$$      /$$$$$$   /$$ /$$$$$$/$$$$   /$$$$$$
 /$$__  $$ /$$__  $$ /$$_____/ /$$__  $$ /$$__  $$| $$__  $$ /$$_____/ /$$__  $$    |_  $$_/  | $$| $$_  $$_  $$ /$$__  $$
| $$  \__/| $$$$$$$$|  $$$$$$ | $$  \ $$| $$  \ $$| $$  \ $$|  $$$$$$ | $$$$$$$$      | $$    | $$| $$ \ $$ \ $$| $$$$$$$$
| $$      | $$_____/ \____  $$| $$  | $$| $$  | $$| $$  | $$ \____  $$| $$_____/      | $$ /$$| $$| $$ | $$ | $$| $$_____/
| $$      |  $$$$$$$ /$$$$$$$/| $$$$$$$/|  $$$$$$/| $$  | $$ /$$$$$$$/|  $$$$$$$      |  $$$$/| $$| $$ | $$ | $$|  $$$$$$$
|__/       \_______/|_______/ | $$____/  \______/ |__/  |__/|_______/  \_______//$$$$$$\___/  |__/|__/ |__/ |__/ \_______/
                              | $$                                             |______/
                              | $$
                              |__/

'''
print(banner)
flag=''
with open('/flag', 'r') as file:
    flag = file.read()
flag=flag.strip()

sum=0
print("Can you find the secret of the response time?")
print()
print()
while(True):
    if sum==len(flag) :
        print('Congratulations! you get it!')
        exit(0)
    print('Please input one character:')
    ans=input('> ')
    if ans != flag[sum] and len(ans)==1:
        print('Who knows whether it is the right character?')
        print()
    if ans == flag[sum] and len(ans)==1:
        time.sleep(1.5)
        print('Who knows whether it is the right character?')
        print()
        sum=sum+1
    if len(ans)!=1:
        print('Invalid input!')
        print()

```

然后根据这个响应时间的特性，我们使用pwntools写出解题脚本

exp：

```python
from pwn import *
import time

from tqdm import tqdm
io = remote("127.0.0.1",45559)
table = '-{}abcdefghigklmnopqrstuvwxyz1234567890!_ABCDEFGHIJKLMNOPQRSTUVWXYZ'#定义的字符表
flag=''
for j in table:
    for i in table:
        io.sendline(bytes(i.encode()))
        start_time = time.time()
        io.recvuntil('Who knows whether it is the right character?\n',timeout=100000)
        end_time=time.time()
        response_time = end_time-start_time
        if(response_time>1): #如果响应时间大于1s，就添加进flag
            flag=flag+i
            print(flag)
            break  #退出当次循环
```


![image.png](https://s2.loli.net/2024/04/24/Sm6wuTxOGbYo3R4.png)
爆一会就出来了