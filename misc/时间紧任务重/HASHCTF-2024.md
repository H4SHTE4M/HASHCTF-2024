---
title: HASHCTF_2024
date: 2024-04-14 15:58:04
tags:
- ctf
keywords:
description:
top_img: https://smms.app/image/5XwqgPpE2TM4V8c
comments:
cover: https://smms.app/image/5XwqgPpE2TM4V8c
toc_number:
toc_style_simple:
copyright:
copyright_author:
copyright_author_href:
copyright_url:
copyright_info:
mathjax:
katex: enable
aplayer:
highlight_shrink:
aside:
swiper_index:
top_group_index:
background: 
---

# 坚持与努力

其实就是一个数学问题，hash_hash老师提供了一种严谨的做法：

![798529e0ecf5f0a2225cb23fcd91376e.png](https://s2.loli.net/2024/04/14/dO4mMzSng65sbTX.png)

我这里提供一种不太严谨的做法：

统计每个十字中的黑格或白格出现的次数，可以发现黑格子和白格子的统计结果的奇偶性必然相反，举个例子：

![3960dc5e-6ba5-4d17-b457-d7e7fd6362cd.png](https://s2.loli.net/2024/04/14/AduZDXb7312rxph.png)

也就是说，将初始棋盘上的所有黑格或者白格全部翻一遍就能复原整个棋盘

顺便贴上出题人的思路来源：[七步之内必有最优？](https://www.bilibili.com/video/BV1XQ4y1t79G/)

# 时间紧任务重

坚持与努力plus！7*7的棋盘，10轮游戏，要求在10秒内总不超过150通关，实际就是加上了一个查找最少步数和pwntools使用

> *而且出题人还贴心地将棋盘列表输出出来了，不用你们自己整理数据生成列表*

首先翻转一整行或者一整列会将整个棋盘翻转。所以对于任意一个可行解，将这个可行解的任意一行或列翻转得到的解‘也是一个可行解，因为这就相当于在解之后又翻了一遍。这里的解翻转一行指的是，在本来是全点白色的时候，但是这一行白色太多，我就点这一行的黑色，相当于将这一行整体翻转了一遍。于是我们就可以遍历7行+7列一共2^14中行列翻转的可能找到最优的解

官方exp：

```python
from pwn import *
import itertools
#context(os="linux", arch="i386", log_level="debug")
import random
import time
io=remote('localhost',12345)
io.recvuntil('vel1！\n')
content = eval(io.recvline().strip().decode())
print(content)
print(type(content))
def change_row(map, pos, n): #用处不大，只是方便我检查
    for i in range(0, n):
        if map[pos][i] == 1:
            map[pos][i] = 0
        else:
            map[pos][i] = 1

def change_col(map, pos, n): #用处不大，只是方便我检查
    for i in range(0, n):
        if map[i][pos] == 1:
            map[i][pos] = 0
        else:
            map[i][pos] = 1
def show_map(map, n):        #用处不大，只是方便我检查
    for i in range(0, n):
        for j in range(0, n):
            if map[i][j] == 1:
                print("⬜", end=" ")
            else:
                print("⬛", end=" ")
        print()
def count(map):
    count = 0
    for row in map:
        for col in row:
            if col == 1:
                count += 1
    SIZE = len(map)
    return count if count < SIZE * SIZE - count else SIZE * SIZE - count
def tryflip(map):
    SIZE = len(map)
    combinations = [combo for r in range(SIZE) for combo in itertools.combinations(range(SIZE), r)]
    pnt_count = SIZE * SIZE//2
    temp_map = map
    final_map = temp_map
    for combo_r in combinations:
        for r in combo_r:
            change_row(temp_map, r, SIZE)
        for combo_c in combinations:
            for c in combo_c:
                change_col(temp_map, c, SIZE)
            now_count = count(temp_map)
            #print(now_count)
            if now_count < pnt_count:
                pnt_count = now_count
                final_map = [items[:] for items in temp_map[:] ]
                #show_map(final_map, SIZE)
            else:
                continue
    print(pnt_count)
    print(final_map)
    num=0
    for i in final_map:
        for j in i:
            if j ==0:
                num=num+1
            else:
                num=num-1
    if num >0:
        for m in range(SIZE):
            for n in range(SIZE):
                if final_map[m][n] == 1:
                    solution=f'{m+1} {n+1}'
                    print(solution)
                    io.sendline(bytes(solution.encode()))
                    io.recvuntil('纵坐标：')
    else:
        for m in range(SIZE):
            for n in range(SIZE):
                if final_map[m][n] == 0:
                    solution = f'{m + 1} {n + 1}'
                    print(solution)
                    io.sendline(bytes(solution.encode()))
                    io.recvuntil('纵坐标：')

    show_map(final_map, SIZE)
#tryflip(content)
a=io.recvuntil('时间紧任务重\n')

print(a.decode())

for s in range(10):
    b = io.recvline()
    print(b.decode())
    map = eval(b.strip().decode())
    tryflip(map)
    io.recvuntil('Success!\n')

final = io.recv()
print(final.decode())
```

# Hilbert_Peano

搜索可以发现这个标题代表一种分形几何，结合图片可以看到对应这一种

![v2-09e573518a0d016f866fa04cc0be8a0d_1440w.webp](https://s2.loli.net/2024/04/14/Ku6ErsAfdHLIJO5.webp)

然后编写脚本将图片的像素按照这种曲线的路径取出来再按从左到右从上到下的顺序排列成新的图片就行

官方exp：
```python
from PIL import Image
from tqdm import tqdm

def Hilbert(n): #生成曲线对应的坐标路径
    if n == 0:
        return [[0, 0]]
    else:
        in_lst = Hilbert(n - 1)
        lst = [[i[1], i[0]] for i in in_lst]
        px, py = lst[-1]
        lst.extend([px + i[0], py + 1 + i[1]] for i in in_lst)
        px, py = lst[-1]
        lst.extend([px + 1 + i[0], py + i[1]] for i in in_lst)
        px, py = lst[-1]
        lst.extend([px - i[1], py - 1 - i[0]] for i in in_lst)
        return lst
    
order = Hilbert(10)

img = Image.open(r"C:\Users\ASUSROG\Desktop\TRY\Hilbert_Peano.jpg")

def decode(img):
    width, height = img.size

    new_image = Image.new("RGB", (width, height))

    for i, (x, y) in tqdm(enumerate(order)):
        # 根据列表顺序获取新的坐标
        new_x, new_y = i % width, i // width
        # 获取原图像素
        pixel = img.getpixel((x, height - 1 - y))
        # 在新图像中放置像素
        new_image.putpixel((new_x, new_y), pixel)

    new_image.save("rearranged_image.jpg") 

def encode(img):
    width, height = img.size

    new_image = Image.new("RGB", (width, height))

    for i, (x, y) in tqdm(enumerate(order)):
        # 根据列表顺序获取新的坐标
        new_x, new_y = i % width, i // width
        # 获取原图像素
        pixel = img.getpixel((new_x, new_y))
        # 在新图像中放置像素
        new_image.putpixel((x, height - 1 - y), pixel)

    new_image.save("rearranged_image.jpg")

#encode(img)

decode(img)
```

最终得到结果：

![rearranged_image.jpg](https://s2.loli.net/2024/04/14/CdfVcBabsiWg2he.jpg)

> 最终只有一人欣赏到绫波的微笑😭😭😭