import numpy as np
import cv2
import pyautogui
from PIL import Image
import pytesseract
import pyttsx3
import win32api
import time

# -----------------------
# BOARD IS CALIBRATED FOR 1920 X 1080 WINDOW SIZE
# ----------------------

# Board Position
start_position = (362, 208)
end_position = (0, 0)

# Board Tile Size
tile_size = 56

# Mouse Attributes
state_left = win32api.GetKeyState(0x01)
num_spaces = 0


# Creates an image of each tile on the board
# Images are outputted into the output folder
def read_board():
    global start_position, tile_size
    engine = pyttsx3.init()

    time.sleep(3)
    count = 0
    xs = 0
    ys = 0
    for y in range(9):
        if y + 1 % 3 == 0:
            ys -= 1
        for x in range(9):
            if x == 0:
                xs = ys = 0
            if x % 3 == 0:
                xs += 1
            image = pyautogui.screenshot(
                region=(start_position[0] + (x * tile_size + xs), start_position[1] + (y * tile_size + ys), tile_size,
                        tile_size))
            image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
            thresh = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

            result = thresh

            cv2.imwrite("output/image{0}.png".format(count), result)
            count += 1
    engine.say("Completed reading the board")
    engine.runAndWait()


# Uses PyTesseract to identify the number in each tile and output
# each tile into a NumPy array
# returns a filled NumPy array where every blank tile is a 0
def load_board_to_array():
    global num_spaces
    engine = pyttsx3.init()
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
    board = np.zeros((9, 9))
    count = 0
    for y in range(9):
        for x in range(9):
            value = [pytesseract.image_to_string(Image.open("output/image{0}.png".format(count)),
                                                 config='--psm 10')[0]]
            position = [int(9 * y + x)]
            # small cases
            if value[0] == 'r':
                value[0] = '9   '

            try:
                value[0] = int(value[0])
            except ValueError:
                num_spaces += 1
                value[0] = 0

            np.put(board, position, value)
            count += 1

    engine.say("Board array has been filled")
    engine.runAndWait()
    return board


# Params: Board (NumPy Array), x, y (tile position), num (Number to check if possible)
# Returns true if the number is a valid move at the tile location
def check_possible(board, x, y, num):
    # Check X row
    for i in range(9):
        if board[y][i] == num:
            return False
    # Check Y column
    for i in range(9):
        if board[i][x] == num:
            return False
    # Check grid
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[y0 + i][x0 + j] == num:
                return False
    return True


# A recursive backtracking algorithm that solves the sudoku puzzle
def solver(board):
    for y in range(9):
        for x in range(9):
            if board[y][x] == 0:
                for num in range(1, 10):
                    if check_possible(board, x, y, num):
                        board[y][x] = num
                        solver(board)
                        board[y][x] = 0
                return
    print("\n", np.matrix(board))
    check_output_number(board)


# Checks if the mouse is clicked within the bounds of the board
def in_bounds(pos):
    global start_position, tile_size
    if pos[0] < start_position[0] or pos[0] > start_position[0] + (9 * tile_size):
        return False
    elif pos[1] < start_position[1] or pos[1] > start_position[1] + (9 * tile_size):
        return False
    return True


# This function is to be used to automate inputting the answer into the board
# Unfortunately Sudoku.com doesn't let this function work so the function below is
# a better solution for solving this problem
def output_solution(board):
    for y in range(9):
        for x in range(9):
            pyautogui.moveTo(320 + (x * 65), 285 + (y * 65))
            pyautogui.click()
            time.sleep(0.5)
            pyautogui.hotkey('{0}'.format(int(board[y][x])))
            print('{0}'.format(str(board[y][x])))


# Checks which tile the mouse clicks on and returns the answer for that tile
# It will output the answer using the speaker so that the user can input the answer
def check_output_number(board):
    global state_left
    global num_spaces
    global start_position
    global tile_size

    engine = pyttsx3.init()
    engine.say("Ready to play Sudoku!")
    engine.runAndWait()

    while True:
        if num_spaces <= 0:
            engine.say("We have won the game!")
            engine.runAndWait()
            break

        pos = pyautogui.position()
        a = win32api.GetKeyState(0x01)

        tile_x = (pos[0] - start_position[0]) // tile_size
        tile_y = (pos[1] - start_position[1]) // tile_size

        if a != state_left and in_bounds(pos):
            state_left = a
            if a < 0:
                num = int(board[tile_y][tile_x])
                num_spaces -= 1
                print(num, tile_x, tile_y)
                engine.say("{0}".format(num))
                engine.runAndWait()


def main():
    read_board()
    board = load_board_to_array()
    solver(board)


if __name__ == '__main__':
    main()
