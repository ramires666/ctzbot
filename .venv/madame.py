#%% imports
import time
import timeit
import pytesseract
from PIL import Image,ImageEnhance,ImageOps
import pyautogui
import time
import pandas as pd
from random import random

dir= r'C:\Users\name\PycharmProjects\pythonProject'
pytesseract.pytesseract.tesseract_cmd =r'C:\Program Files\Tesseract-OCR\tesseract.exe'
custom_config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789'
# custom_config = r'--oem 3 --psm 13 outputbase digits'
num_coords = [(0, 0), (182, 0), (364, 0), (545, 0),
              (0, 139), (182, 139), (364, 139), (545, 139),
              (0, 280), (182, 280), (364, 280), (545, 280)]
cycles = 1


def loadImage(path):
    needleFileObj = open(path, 'rb')
    needleImage = Image.open(needleFileObj)

    return needleImage


def initAnimals():
    global shiba,shiba2,pepe,pep2,duck,duck2,dir
shiba = ImageOps.grayscale(loadImage(dir+ r'\shiba.png'))
shiba2 = shiba.transpose(method=Image.FLIP_LEFT_RIGHT)
pepe = ImageOps.grayscale(loadImage(dir+ r'\pepe.png'))
pepe2  = pepe.transpose(method=Image.FLIP_LEFT_RIGHT)
duck = ImageOps.grayscale(loadImage(dir+ r'\duck.png'))
duck2  = duck.transpose(method=Image.FLIP_LEFT_RIGHT)


#%%
def initcoords(num_coords):
#%%
    x = 191
    y= 1156
    num_coords = [(0, 0), (182, 0), (364, 0), (545, 0),
                  (1, 141), (182, 141), (364, 141), (545, 141),
                  (1, 280), (182, 280), (364, 280), (545, 280)]
    num_coords = [(first + x , second + y) for first, second in num_coords]
    x,y=num_coords[0]
    pyautogui.click(x, y)
    print(x,y," ",getnumbers(x,y,True))
#%%
    return num_coords
#%%
# im = pyautogui.screenshot(region=(205,760, 18, 16))
def getnumbers(x,y,save):
    im = pyautogui.screenshot(region=(x,y, 26, 20))
    # im = pyautogui.screenshot(region=(305, 1085, 508, 270))

    new_Kwidth = im.width +5
    new_Kheight = im.height + 5
    nim = Image.new("RGB", (new_Kwidth, new_Kheight), 'white')
    # Вставляем исходный скриншот в центр нового изображения
    x_offset = (new_Kwidth - im.width) // 2
    y_offset = (new_Kheight - im.height) // 2
    nim.paste(im, (x_offset, y_offset))

    # gray_image = ImageOps.grayscale(nim)
    new_width = nim.width * 10
    new_height = nim.height * 10
    im_resized = nim.resize((new_width, new_height), Image.Resampling.LANCZOS)
    enhancer = ImageEnhance.Contrast(im_resized)
    factor = 19.0  # Увеличиваем контраст в 2 раза
    enhanced_image = enhancer.enhance(factor)
    if save:
        enhanced_image.save(r'C:\Users\name\PycharmProjects\pythonProject\qqq.png')
    return pytesseract.image_to_string(enhanced_image, config=custom_config).strip()


#%%
def c():
    while 1==1:
        print(pyautogui.position())
        time.sleep(2)

def mc(x,y):
    x += int(4*random())
    y += int(4*random())
    pyautogui.moveTo(x, y, 0.3, pyautogui.easeInQuad)
    pyautogui.click(x, y)
#%%%
def check_bonus_time(x,y):
    im = pyautogui.screenshot(region=(x, y, 3, 3))
    pixel_color = im.getpixel((1, 1))
    # mc(x=967+x, y=1381+y)  # close

    if pixel_color == (242, 67, 67):
        print(f'BONUS TIME !')
        # mc(x=316, y=1717)
        mc(x=x, y=y)  # open
        mc(x=273, y=1318)  # click
        mc(x=777, y=364)
#%%
def check_bonus_cat(x,y):
    im = pyautogui.screenshot(region=(x, y, 3, 3))
    pixel_color = im.getpixel((1, 1))
    if pixel_color == (242, 67, 67):
        print(f'BONUS CAT!')
        mc(x, y)
        mc(x=551, y=1540)
        # print(f"Цвет пикселя на позиции ({x}, {y}) - {pixel_color}")
        mc(x=777, y=364)


#%%
def init():
    initAnimals()
    return [{n:0} for n in range(12)]
#%%
# start = timeit.default_timer()
def read_cats():
    global cycles
    # cats =[]
    for n in range(0,12):
        cycles +=1
        time.sleep(0.5)
        # if cycles % 10 != 0 and cats[n].get(n) == 0 : continue
        x,y = num_coords[n]
        number = getnumbers(x, y,False)
        try: number=int(number)
        except: number = 0
        print(f'n={n} = {number}')
        cats[n]={n:number}
        find(cats)

    return cats

#%%
def breed(x1,y1,x2,y2):
    # pyautogui.moveTo(,0.3, pyautogui.easeInQuad)
    mc(x1-10, y1+10)
    pyautogui.dragTo(x2-10, y2+10, 0.5, pyautogui.easeInQuad, button='left')

#%%
def find_and_breed(cats):
    sorted_data = sorted(cats, key=lambda x: int(list(x.values())[0]))
    for n in range(1,len(sorted_data)):
        # print(n)
        (X,Y), = sorted_data[n-1].items()
        (x,y), = sorted_data[n].items()
        if Y == y :
            print(f'n:{n-1},Y:{Y}  n:{n},y:{y},{num_coords[x]},{num_coords[X]}')
            # breed(*num_coords[x],*num_coords[X])

def bonus_check():
    hay = getHay()
    check_shiba(hay)
    check_pepe(hay)
    check_duck(hay)


#%%
def find(data):
    # Множество для отслеживания уникальных комбинаций (без учёта порядка)
    global cats
    while 1 == 1 :
        used_keys = set()  # Для отслеживания использованных ключей
        pairs = []  # Список для хранения уникальных пар ключей
        for i in range(len(data) - 1):
            for j in range(i + 1, len(data)):
                key_i, value_i = next(iter(data[i].items()))
                key_j, value_j = next(iter(data[j].items()))

                # Проверяем, что ключи не использовались, значения совпадают, и они не равны 0
                if key_i not in used_keys and key_j not in used_keys and value_i == value_j and value_i != 0:
                    pairs.append((key_i, key_j))  # Добавляем пару ключей
                    used_keys.add(key_i)  # Отмечаем ключи как использованные
                    used_keys.add(key_j)
        # bonus_check()
        if pairs:
            for pair in pairs:
                print(f"Парны: {pair[0]} и {pair[1]}")
                breed(*num_coords[pair[0]], *num_coords[pair[1]])
                # bonus_check()
                # pyautogui.click(x=516, y=1340)
                data[pair[0]] = {pair[0]:0}
                data[pair[1]] = {pair[1]:data[pair[1]][pair[1]] +1}
        else: break

#%%
def loc(needls,hay):
    x=0
    y=0
    try:
        x, y = pyautogui.locate(needleImage, haystackImage, grayscale=False)
    except:
        pass
    return x,y


def getHay():
    im = pyautogui.screenshot(region=(36, 460, 780, 600))
    im2 = ImageOps.grayscale(im)
    return im2

def acceptBonus():
    mc(255, 1307)


def check_shiba(hay):
    global dir,shiba,shiba2
    # hay = getHay()
    x,y = loc(shiba,hay)
    if x > 0:
        print('Found SHIBA)')
        mc(x, y)
        acceptBonus()
    x,y = loc(shiba2,hay)
    if x > 0:
        print('Found SHIBA2)')
        mc(x, y)
        acceptBonus()

def check_pepe(hay):
    #%%
    print('check 4 bonus')
    global dir,pepe,pepe2
    # hay = getHay()
    x,y = loc(pepe,hay)
    if x > 0:
        print('Found PEPE)')
        mc(x, y)
        acceptBonus()
    x,y = loc(pepe2,hay)
    if x > 0:
        print('Found PEPE2)')
        mc(x, y)
        acceptBonus()


def check_duck(hay):
    #%%
    global dir,duck,duck2
    # hay = getHay()
    x,y = loc(duck,hay)
    if x > 0:
        print('Found DUCK)')
        mc(x, y)
        acceptBonus()
    x,y = loc(duck2,hay)
    if x > 0:
        print('Found DUCK2)')
        mc(x, y)
        acceptBonus()


#%%
def main():
#%%
    global num_coords,cats
    mc(424,1371)
    num_coords = initcoords(num_coords)
    cats=init()

    while 1==1 :
        cats = read_cats()
        mc(435,1390)  # close
        find(cats)
        check_bonus_cat(685,1720)
        check_bonus_time(289,1716)
        mc(255,1307)

#%%
if __name__ == '__main__':
    main()

    #%%

