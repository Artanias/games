import pyautogui
import keyboard
import numpy as np
import cv2
from mss import mss
import pandas as pd
import matplotlib.pyplot as plt

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

        return sct_img


def save_in_pickle(img):
    df = pd.read_pickle('marked_img.pickle')
    print('It is sudoku?')
    is_sudocu = input()
    if is_sudocu == 'Y':
        df.loc[df.shape[0]] = (img, 1)
    else: 
        df.loc[df.shape[0]] = (img, 0)
    df.to_pickle('marked_img.pickle')
    print(df.iloc[-1, :])

        
if __name__ == '__main__':
    for i in range(10):
        monitor = get_positions()
        image = grab_monitor(monitor)
        scaled_img = cv2.resize(image, (500, 500))
        plt.imshow(scaled_img)
        plt.show()
        save_in_pickle(scaled_img)
