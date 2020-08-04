import pyautogui
import keyboard
import numpy as np
import cv2
from solver import SudokuSolver
from mss import mss
from tensorflow import keras

# import matplotlib.pyplot as plt
# import pandas as pd


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
        # cv2.imshow('Image', sct_img)

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
    square = img[first_point[1]:(second_point[1] + 1),
                 first_point[0]:(second_point[0] + 1)]
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
                            if square.size > 500:
                                squares.append(square)

    return squares


def check_sq(field, x, y, num):
    square_x = (x // 3) * 3
    square_y = (y // 3) * 3
    square = field[square_y:square_y + 3, square_x: square_x + 3]
    set_num = (0 == square)
    sq_zr = (0 == square).mean()
    ln_zr = (0 == field[y]).mean()
    cl_zr = (0 == field[:, x]).mean()
    if (sq_zr < 0.12) or (ln_zr < 0.12) or (cl_zr < 0.12):
        return True
    else:
        for t_i in range(3):
            for t_j in range(3):
                t_x = square_x + t_i
                t_y = square_y + t_j
                if ((x != t_x) or (y != t_y)) and (square[t_j][t_i] == 0):
                    if num in field[t_y]:
                        set_num[t_j][t_i] = False
                    if num in field[:, t_x]:
                        set_num[t_j][t_i] = False

    if(set_num.mean() < 0.12):
        return True
    else:
        return False


def insert_num(field, x, y):
    square_x = (x // 3) * 3
    square_y = (y // 3) * 3
    square = field[square_y:square_y + 3, square_x: square_x + 3]
    for num in range(1, 10):
        if num not in field[y]:
            if num not in field[:, x]:
                if num not in square:
                    if(check_sq(field, x, y, num)):
                        field[y][x] = num
                        return
    return


def solve(field):
    while(0 in field):
        for x in range(field.shape[1]):
            for y in range(field.shape[0]):
                if field[y][x] != 0:
                    continue
                else:
                    insert_num(field, x, y)


if __name__ == '__main__':
    monitor = get_positions()
    image = grab_monitor(monitor)
    field_without_num = get_field_1(image)
    scaled_img = cv2.resize(image, (500, 500))
    model = keras.models.load_model('sudoku_recognition.h5')
    predict = model.predict(np.array([scaled_img]))
    if(predict[0][1] == 1):
        print('It\'s Sudoku')
        squares = get_squares(field_without_num, image)
        if len(squares) != 81:
            print('Error squares more than 81 or less')
        else:
            # df = pd.read_pickle('new_squares.pickle')
            model = keras.models.load_model('num_recognition.h5')
            nums = []
            for square in squares:
                temp_sq = cv2.resize(square, (50, 50))
                predict = (model.predict(np.array([temp_sq])))[0]
                for i in range(predict.size):
                    if abs(1 - predict[i]) < 0.02:
                        nums.append(i)
                        break

                # save square in same size and label it
                # scaled_img = cv2.resize(square, (50, 50))
                # plt.imshow(scaled_img)
                # plt.show()
                # print('Number: ')
                # num = int(input())
                # df.loc[df.shape[0]] = (scaled_img, num)
                # df.to_pickle('new_squares.pickle')
                # print(df.loc[df.shape[0] - 1])

            field = np.array(nums)
            field.shape = (9, 9)
            while(True):
                print(field)
                print('Correct? (Y)')
                answer = str(input())
                if answer == 'Y':
                    # solve(field)
                    field = SudokuSolver.solve(field)
                    break
                else:
                    print('x = ')
                    temp_x = int(input())
                    print('y = ')
                    temp_y = int(input())
                    print('num = ')
                    number = int(input())
                    field[temp_y][temp_x] = number
            if field is not None:
                print(field)
    else:
        print('It\'s not Sudoku')
