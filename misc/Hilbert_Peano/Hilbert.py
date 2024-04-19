from PIL import Image
from tqdm import tqdm

def Hilbert(n):
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