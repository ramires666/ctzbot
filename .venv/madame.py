#%% imports
import time
import timeit
import pytesseract
from PIL import Image,ImageEnhance,ImageOps
import pyautogui
import time
import pandas as pd
import random
from datetime import datetime as dt
from datetime import timedelta as td
from mousebez import *

dir= r'C:\Users\name\PycharmProjects\pythonProject'
pytesseract.pytesseract.tesseract_cmd =r'C:\Program Files\Tesseract-OCR\tesseract.exe'
custom_config = r'--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789'
# custom_config = r'--oem 3 --psm 13 outputbase digits'
num_coords = [(0, 0), (182, 0), (364, 0), (545, 0),
              (0, 139), (182, 139), (364, 139), (545, 139),
              (0, 280), (182, 280), (364, 280), (545, 280)]
cycles = 1


mouse = MouseUtils()
# cords = (500, 500)
# mouse.move_to(cords, mouseSpeed='slow', knotsCount=1)

# # Any duration less than this is rounded to 0.0 to instantly move the mouse.
# pyautogui.MINIMUM_DURATION = 0  # Default: 0.1
# # Minimal number of seconds to sleep between mouse moves.
# pyautogui.MINIMUM_SLEEP = 0  # Default: 0.05
# # The number of seconds to pause after EVERY public function call.
# pyautogui.PAUSE = 0  # Default: 0.1



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
    x = 179
    y= 1154
    num_coords = [(0, 0), (178, 0), (356, 0), (534, 0),
                  (0, 138), (178, 138), (356, 138), (534, 138),
                  (0, 276), (178, 276), (356, 276), (534, 276)]
    num_coords = [(first + x , second + y) for first, second in num_coords]
    x,y=num_coords[1]
    pyautogui.click(x, y)
    print(x,y," ",getnumbers(x,y,True))
#%%
    return num_coords
#%%
# im = pyautogui.screenshot(region=(205,760, 18, 16))
def getnumbers(x,y,save):
    im = pyautogui.screenshot(region=(x,y, 27, 20))
    # im = pyautogui.screenshot(region=(305, 1085, 508, 270))

    new_Kwidth = im.width +7
    new_Kheight = im.height + 7
    nim = ImageOps.grayscale(Image.new("RGB", (new_Kwidth, new_Kheight), 'white'))
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



def c():
    while 1==1:
        print(pyautogui.position())
        time.sleep(2)

speeds = ['slow','medium','fast']
def mc(x,y,strict=False,retrace=False):
    speed = random.choice(speeds)
    knots = random.choice(range(1,7))
    mouse.move_to((x,y), mouseSpeed=speed, knotsCount=knots)
    pyautogui.click(x, y)
    x = random.randint(100, 820) #int(820 * random())
    y = random.randint(1145, 1545) #int(1545 * random())
    speed = random.choice(speeds)
    knots = random.choice(range(1, 7))
    mouse.move_to((x,y), mouseSpeed=speed, knotsCount=knots)



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

def check_bonus_cat(x,y):
    im = pyautogui.screenshot(region=(x, y, 3, 3))
    pixel_color = im.getpixel((1, 1))
    if pixel_color == (242, 67, 67):
        print(f'BONUS CAT!')
        mc(x, y)

        mc(x=551, y=1540)
        # print(f"Цвет пикселя на позиции ({x}, {y}) - {pixel_color}")
        mc(x=777, y=364)
        cats = read_cats()
        find(cats)




def init():
    initAnimals()
    return [{n:0} for n in range(12)]

# start = timeit.default_timer()
def read_cats():
    global cycles
    # cats =[]
    for n in range(0,12):
        cycles +=1
        # time.sleep(0.5)
        # if cycles % 10 != 0 and cats[n].get(n) == 0 : continue
        x,y = num_coords[n]
        number = getnumbers(x, y,False)
        try: number=int(number)
        except: number = 0
        print(f'n={n} = {number}')
        cats[n]={n:number}
        find(cats)

    return cats

def check_empty_cats():
    global cycles,cars
    # cats =[]
    n2read = None
    for catN in range(0,12):
        # print(cats[catN][catN])
        if cats[catN][catN] == 0:
            print(catN)
            n2read = catN
            # break
    # if n2read:
            x, y = num_coords[n2read]
            number = getnumbers(x, y, False)
            try: number=int(number)
            except: number = 0
            if number != 0:
                print(f'EXTRA n={n2read} = {number}')
                cats[n2read] = {n2read: number}
                find(cats)


    # for n in range(0,12):
    #     cycles +=1
    #     x,y = num_coords[n]
    #     print(f"{n},{x},{y}")
    #     # number = getnumbers(x, y,False)
    #     # try: number=int(number)
    #     # except: number = 0
    #     # print(f'n={n} = {number}')
    #     # cats[n]={n:number}
    #     # find(cats)

    return cats



def breed(x1,y1,x2,y2):
    # pyautogui.moveTo(,0.3, pyautogui.easeInQuad)
    # mc(x1-20, y1+50)
    x_displacement = random.choice(range(1, 30))
    y_displacement = random.choice(range(1, 50))
    from_ = (x1-x_displacement, y1+y_displacement, )

    x_displacement = random.choice(range(1, 30))
    y_displacement = random.choice(range(1, 50))
    to_ = (x2-x_displacement, y2+y_displacement, )

    speed = random.choice(speeds)
    knots = random.choice(range(1, 8))
    mouse.move_to(from_, mouseSpeed=speed, knotsCount=knots)
    # pyautogui.dragTo(x2-10, y2+10, 0.5, pyautogui.easeInQuad, button='left')
    speedChoice = int(random.random()*5)
    speed = 'medium'
    match speedChoice:
        # case 0:
        #     speed = 'slowest'
        case 1:
            speed = 'slow'
        case 2:
            speed = 'medium'
        case 3:
            speed = 'fast'
        # case 4:
        #     speed = 'fastest'
    # mouse.drag_to(x1-20,y1+50,x2-20,y2+50, mouseSpeed=speed, knotsCount=1)

    order = random.choice(range(0, 3))
    if order == 2:
        # print(f'order = {order}')
        from_,to_ = to_,from_
        mouse.move_to(from_, mouseSpeed=speed, knotsCount=knots)
    mouse.drag_to(*from_, *to_, mouseSpeed=speed, knotsCount=1)
    return order



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
                order = breed(*num_coords[pair[0]], *num_coords[pair[1]])
                mouse.rnd(100)
                # bonus_check()
                # pyautogui.click(x=516, y=1340)
                if order == 2:
                    data[pair[1]] = {pair[1]: 0}
                    data[pair[0]] = {pair[0]: data[pair[0]][pair[0]] + 1}
                else:
                    data[pair[0]] = {pair[0]:0}
                    data[pair[1]] = {pair[1]:data[pair[1]][pair[1]] +1}
        else: break


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

def restart():
    mc(41,129) # cross
    mc(610, 1046)  # confirm
    mc(91, 1832)  # run
    time.sleep(9)


start_time = dt.now()
def check_restart():
    global start_time
    now = dt.now()
    timePassed = now-start_time
    print(f'time passed: {int(timePassed.total_seconds())}')
    rt =random.randint(200,2000)
    # rt = random.randint(100, 200)
    if (timePassed.seconds+rt)//3000 >= 1:
    # if (timePassed.seconds + rt) // 130 >= 1:
        print('retarting..')
        restart()
        start_time = dt.now()

#%%
def main():
#%%
    global num_coords,cats
    mc(424,1371)
    num_coords = initcoords(num_coords)
    cats=init()

    while 1==1 :
        # mc(253, 1238, False, True)
        mc(435,1390,False,True)
        time.sleep(.2)
        mc(291, 1268,False,True) # anti-offline
        time.sleep(.5)
        mc(291, 1268,False,True) # anti-offline
        check_bonus_time(554,1045)
        cats = read_cats()
        find(cats)
        check_bonus_cat(653,1711)
        # mc(428,1307,False,True)
        check_empty_cats()
        time.sleep(10)
        check_restart()
        totalCats = sum([sum(c.values()) for c in cats])
        if totalCats  == 0:
            print(f'totalCats={totalCats}')
            mc(85,16)
            mc(62, 1340)


#%%
if __name__ == '__main__':
    main()

    #%%


