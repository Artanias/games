import numpy as np
import cv2
from mss import mss
import pyautogui as pg
import keyboard

monitor = {'top': 180, 'left': 505, 'width': 40, 'height': 60}
list_img = []


def process_image(original_image):
    image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    image = cv2.Canny(image, threshold1=200, threshold2=100)
    return image


def screen_record():
    sct = mss()

    num = 0
    while(True):
        # if you want to start code below press Y
        if keyboard.is_pressed('Y'):
            while(True):
                img = sct.grab(monitor)
                img = np.array(img)
                processed_image = process_image(img)
                # mean use for find changes in image
                mean = np.mean(processed_image)
                # Debug list with screenshots and mean
                # list_img.append({'img': img, 'mean': 0})
                print('mean = {}, num = {}'.format(mean, num))

                if mean > float(14):
                    pg.press('space')

                # if you want to end script press q
                if keyboard.is_pressed('q'):
                    print("break with button q")
                    return
                num += 1


screen_record()
