import pyautogui
import keyboard
import numpy as np
import cv2
from mss import mss

def get_positions():
    print('Press x')
    while(True):
        if keyboard.is_pressed('x'):
            P1 = pyautogui.position()
            break
    print('Press y')
    while(True):
        if keyboard.is_pressed('y'):
            P2 = pyautogui.position()
            break
    top = P1.y
    left = P1.x
    width = P2.x - P1.x
    height = P2.y - P1.y
    return {'top': top, 'left': left,
            'width': width, 'height': height}


def grab_monitor(monitor):
    with mss() as sct:
        sct_img = sct.grab(monitor)
        sct_img = np.array(sct_img)
        sct_img = cv2.cvtColor(sct_img, cv2.COLOR_BGR2GRAY)
        sct_img = cv2.Canny(sct_img, 100, 200)
        max_x = sct_img.shape[1]
        max_y = sct_img.shape[0]
        x, y = 0, 0
        while(y < max_y):
            temp = sct_img[y]
            if temp.mean() < 5:                
                sct_img = np.delete(sct_img, y, axis=0)
                max_y -= 1
                y -= 1
            y += 1
        while(x < max_x):
            temp = sct_img[:, x]
            if temp.mean() < 5:
                sct_img = np.delete(sct_img, x, axis=1)
                max_x -= 1
                x -= 1
            x += 1
        #cv2.imshow('Image', sct_img)        

        return sct_img


def get_field_1(image):
    field = np.zeros((image.shape[0], image.shape[1]))
    max_x = image.shape[1]
    max_y = image.shape[0]
    for y in range(max_y):        
        temp = image[y]
        if temp.mean() > 100:            
            field[y] = temp
    for x in range(max_x):
        temp = image[:, x]
        if temp.mean() > 100:
            field[:, x] = temp
    return field


def get_square_coords(field, x, y):
    coords = [(x, y)]
    max_x = image.shape[1]
    max_y = image.shape[0]
    while(x < max_x):        
        if field[y].mean() > 100:
            if field[:, x].mean() > 100:
                coords.append((x, y))
                break
        x += 1

    if len(coords) < 2:
        return 

    y += 1
    while(y < max_y):        
        if field[y].mean() > 100:
            if field[:, x].mean() > 100:
                coords.append((x, y))
                break
        y += 1
        
    return coords


def get_img_square(img, coords):
    first_point = coords[0]
    second_point = coords[2]
    square = img[first_point[1]:(second_point[1] + 1), first_point[0]:(second_point[0] + 1)]
    return square
    
def get_squares(field, image):
    squares = []
    max_x = image.shape[1]
    max_y = image.shape[0]
    for y in range(max_y):
        if field[y].mean() > 100:
            for x in range(max_x):
                if field[:, x].mean() > 100:
                    coords = get_square_coords(field, x + 1, y)
                    if coords is not None and len(coords) == 3:
                        square = get_img_square(image, coords)
                        shape1 = square.shape[0]
                        shape2 = square.shape[1]
                        if abs(shape1-shape2) < 5 and square.mean() < 100:
                            squares.append(square)

    return squares
                    
    
if __name__ == '__main__':
    monitor = get_positions()
    image = grab_monitor(monitor)
    field_without_num = get_field_1(image)    
    squares = get_squares(field_without_num, image)
    if len(squares) != 81:
        print('Error squares more than 81 or less')
    else:
        pass
    #cv2.imshow('Image', )
