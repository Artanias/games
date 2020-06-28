import numpy as np
import cv2
from mss import mss
import pyautogui as pg
import keyboard

monitor_without_man_left = {'top': 390, 'left': 450,
                            'width': 180, 'height': 100}
monitor_with_man_left = {'top': 520, 'left': 450,
                         'width': 180, 'height': 150}
monitor_without_man_right = {'top': 390, 'left': 740,
                             'width': 180, 'height': 100}
monitor_with_man_right = {'top': 520, 'left': 740,
                          'width': 180, 'height': 150}
list_img = []


def process_image(original_image):
    image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    image = cv2.Canny(image, threshold1=200, threshold2=100)
    return image


def screen_record():
    sct = mss()
    # last_time = time.time()

    while(True):
        if keyboard.is_pressed('Y'):
            img1 = sct.grab(monitor_without_man_left)
            img1 = np.array(img1)
            processed_image = process_image(img1)
            mean1 = np.mean(processed_image)
            img2 = sct.grab(monitor_with_man_left)
            img2 = np.array(img2)
            processed_image = process_image(img2)
            mean2 = np.mean(processed_image)
            button = 'left'
            num = 0
            while(True):
                # Debug
                # print(num)
                # print('mean1 = ', mean1)
                # print('mean2 = ', mean2)
                list_img.append({'img1': img1, 'img2': img2, 'button': button})
                # cv2.imshow('Image', img1)
                # cv2.imshow('Image', img2)
                # return

                if mean1 > float(20):
                    if button == 'left':
                        pg.press('right')
                        button = 'right'
                    elif button == 'right':
                        pg.press('left')
                        button = 'left'
                elif mean2 > float(22) and mean2 < float(25):
                    if button == 'left':
                        pg.press('right')
                        button = 'right'
                    elif button == 'right':
                        pg.press('left')
                        button = 'left'
                else:
                    if button == 'left':
                        pg.press('left')
                    elif button == 'right':
                        pg.press('right')
                # print(button)

                if button == 'left':
                    img1 = sct.grab(monitor_without_man_left)
                    img1 = np.array(img1)
                    processed_image = process_image(img1)
                    mean1 = np.mean(processed_image)
                    img2 = sct.grab(monitor_with_man_left)
                    img2 = np.array(img2)
                    processed_image = process_image(img2)
                    mean2 = np.mean(processed_image)
                elif button == 'right':
                    img1 = sct.grab(monitor_without_man_right)
                    img1 = np.array(img1)
                    processed_image = process_image(img1)
                    mean1 = np.mean(processed_image)
                    img2 = sct.grab(monitor_with_man_right)
                    img2 = np.array(img2)
                    processed_image = process_image(img2)
                    mean2 = np.mean(processed_image)
                num += 1

                if keyboard.is_pressed('q'):
                    print("break with button q")
                    return


screen_record()
