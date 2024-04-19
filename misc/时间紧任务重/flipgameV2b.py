import random
import os
import time

FLAG=os.environ.get('GZCTF_FLAG') 

def header():
    print(
        " _    _  ____  __    ___  _____  __  __  ____ \n"+
        "( \/\/ )( ___)(  )  / __)(  _  )(  \/  )( ___)\n"+
        " )    (  )__)  )(__( (__  )(_)(  )    (  )__) \n"+
        "(__/\__)(____)(____)\___)(_____)(_/\/\_)(____)\n"
    )
    print("欢迎来到翻转棋游戏！这个游戏的目标是将棋盘上所有的方块变成相同颜色。每一次，你可以选择一个方块，将其十字区域的方块颜色翻转。")
    print("例如，对于5*5的棋盘，如果你选择了第二行第二列的方块，也就是输入了“2 2”，那么第二行和第二列的十字区域方块都会被翻转。\n"
          "原始棋盘：\n"+
          "⬛ ⬛ ⬛ ⬛ ⬛\n"+
          "⬛ ⬛ ⬛ ⬛ ⬛\n"+
          "⬛ ⬛ ⬛ ⬛ ⬛\n"+
          "⬛ ⬛ ⬛ ⬛ ⬛\n"+
          "⬛ ⬛ ⬛ ⬛ ⬛\n"+
          "翻转后：\n"+
          "⬛ ⬜ ⬛ ⬛ ⬛\n"+
          "⬜ ⬜ ⬜ ⬜ ⬜\n"+
          "⬛ ⬜ ⬛ ⬛ ⬛\n"+
          "⬛ ⬜ ⬛ ⬛ ⬛\n"+
          "⬛ ⬜ ⬛ ⬛ ⬛\n"+
          "你可以通过输入坐标来选择方块。现在开始游戏吧！"
          )

def change_map(map, pos, n):
    pos[0] -= 1
    pos[1] -= 1
    for i in range(0, n):
        if map[pos[0]][i] == 1:
            map[pos[0]][i] = 0
        else:
            map[pos[0]][i] = 1
        if map[i][pos[1]] == 1:
            map[i][pos[1]] = 0
        else:
            map[i][pos[1]] = 1
    if map[pos[0]][pos[1]] == 1:
        map[pos[0]][pos[1]] = 0
    else:
        map[pos[0]][pos[1]] = 1


def clear_screen():
    # Windows 使用 cls 清除屏幕，其他系统使用 clear
    os.system('cls' if os.name == 'nt' else 'clear')


def show_map(map, n):
    for i in range(0, n):
        for j in range(0, n):
            if map[i][j] == 1:
                print("⬜", end=" ")
            else:
                print("⬛", end=" ")
        print()


def check_map(map, n):
    for i in range(0, n):
        for j in range(0, n):
            if map[i][j] == 0:
                return False
    return True


def check_map_2(map, n):
    for i in range(0, n):
        for j in range(0, n):
            if map[i][j] == 1:
                return False
    return True


def gen_map(n, step=50):
    map = [[0 for i in range(0, n)] for j in range(0, n)]
    for k in range(step):
        change_map(map, [random.randint(0, n-1), random.randint(0, n-1)], n)
    return map

def game(SIZE=5):
    map = gen_map(SIZE, 100)
    print(map)
    show_map(map, SIZE)
    step = 0
    while True:
        pos = input("输入你选择的位置，用空格分隔横纵坐标：")
        pos = pos.split(" ")
        if len(pos) != 2:
            print("请以空格分隔横纵坐标并输入两个数字！")
            continue
        try:
            pos = [int(pos[0]), int(pos[1])]
            if pos[0] < 1 or pos[0] > SIZE or pos[1] < 1 or pos[1] > SIZE:
                print("请输入有效的坐标！")
                continue
        except ValueError:
            print("请输入有效的数字！")
            continue
        change_map(map, pos, SIZE)
        #clear_screen()  # 清屏
        show_map(map, SIZE)
        step += 1
        print(f"已经进行了{step}步")
        if check_map(map, SIZE) or check_map_2(map, SIZE):
            clear_screen()
            print('Success!')
            return step

if __name__ == "__main__":
    header()
    print("时间紧任务重")
    total_step = 0
    start_time = time.time()
    for i in range(0, 10):
        total_step += game(7)
    end_time = time.time()
    total_time = end_time - start_time
    if total_step < 150 and total_time < 10:
        print(f"恭喜你完成了！这是flag：{FLAG}")
        print(
        " _  _  _____  __  __    _    _  ____  _  _ /\ \n"+
        "( \/ )(  _  )(  )(  )  ( \/\/ )(_  _)( \( ))( \n"+
        " \  /  )(_)(  )(__)(    )    (  _)(_  )  ( \/ \n"+
        " (__) (_____)(______)  (__/\__)(____)(_)\_)() \n"
        )
    else:
        print("你的步数太多或时间太长，再试一次吧！～(∠・ω< )⌒★")
        exit(0)

