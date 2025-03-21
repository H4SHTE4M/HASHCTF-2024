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
 