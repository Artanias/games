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


def info():
    print('Hi, this is a bot for playing in Timberman.')
    print('If you want to run the bot, then:')
    print('1) Open your game;')
    print('2) Press the start button;')
    print('3) Then press "Y".')
    print('If you want to stop the bot then press "q".')
    print('The bot works in a green summer forest.')


def process_image(original_image):
    image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    image = cv2.Canny(image, threshold1=200, threshold2=100)

    return image


def screen_record():
    with mss() as sct:
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

                while(True):
                    list_img.append({'img1': img1, 'img2': img2,
                                     'button': button})
                    # Debug
                    # cv2.imshow('Image', img1)
                    # cv2.imshow('Image', img2)
                    # return

                    if mean1 > 20.:
                        if button == 'left':
                            pg.press('right')
                            button = 'right'
                        else:
                            pg.press('left')
                            button = 'left'
                    elif mean2 > 22. and mean2 < 25.:
                        if button == 'left':
                            pg.press('right')
                            button = 'right'
                        else:
                            pg.press('left')
                            button = 'left'
                    else:
                        if button == 'left':
                            pg.press('left')
                        else:
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

                    if keyboard.is_pressed('q'):
                        print("Break with button q")
                        return


if __name__ == '__main__':
    info()
    screen_record()
