# Sudoku-Solver
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)

 Solves any game of Sudoku from Sudoku.com
 
 ## Table Of Contents:
[How It Works](https://github.com/DillanSpencer/Sudoku-Solver/blob/master/README.md#How-It-Works)

[Installation](https://github.com/DillanSpencer/Sudoku-Solver/blob/master/README.md#installation)

[Usage](https://github.com/DillanSpencer/Sudoku-Solver/blob/master/README.md#usage)

* [Setup for Use](https://github.com/DillanSpencer/Sudoku-Solver/blob/master/README.md#setup-for-use)
* [Running the program](https://github.com/DillanSpencer/Sudoku-Solver/blob/master/README.md#running-the-program)

## How It Works
1. Creates an image of each tile on the Sudoku board using [PyAutoGUI](https://pypi.org/project/PyAutoGUI/)
2. Uses [OpenCV](https://opencv.org/) to create an Image threshold to use in the character recognition step.
3. Using character recognition, determine the number in each image. To recognise digits and store them in a [NumPy](https://numpy.org/) array, [PyTesseract](https://pypi.org/project/pytesseract/) is used.
4. Solves the Sudoku Puzzle using a recursive backtracking algorithm. 
5. Tracks the user's mouse and determines which tile has been clicked. 
6. Using [Pyttsx3](https://pypi.org/project/pyttsx3/) the program will yell out the answer of the current tile such that the user can input the answer into the board.


## Installation

1. Download and install Python3 from [here](https://www.python.org/downloads/)
2. I recommend using [virtualenv](https://virtualenv.pypa.io/en/latest/). Download virtualenv by opening a terminal and typing:
    ```bash
    pip install virtualenv
    ```
3. Create a virtual environment with the name sudokuenv.

   * Windows
   ```bash
   virtualenv sudoku
   cd sudoku/Scripts
   activate
   ```
   * Linux:
   ```bash
   source sudoku/bin/activate
    ```
4. Clone this repository, extract it if you downloaded a .zip or .tar file and cd into the cloned repository.

    * For Example:
    ```bash
    cd C:\Sudoku-Solver-master
    ```
5. Install the required packages by typing:
   ```bash
   pip install -r requirements.txt
   ```
   
  ## Usage
  ### Setup For Use
  * First things first open up [Sudoku.com](www.sudoku.com). 
  * Once you run the program there is a 3 second interval where you can make your way to the webpage. 
  * Be sure to scroll all the way to the top of the page so that the images can be taken of the tiles correctly.
  * Make sure the volume is turned up so you can hear the program's current stage. When the sound "Let's play some sudoku" plays, you can press on any tile on the board to hear what value should be put there.

### Running The Program
To run the program:
 ```bash
   python3 solver.py
   ```
