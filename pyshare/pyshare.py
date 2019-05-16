# -*- coding: utf-8 -*-


"""pyshare.pyshare: provides entry point main()."""


__version__ = "0.0.1"


import os
import sys
import getopt
import tkinter
import pyscreenshot as ImageGrab

from .config import *


def createMatrix(stringMatrix: str):
    matrix = []
    b = stringMatrix.replace('[[', '').replace(']]', '').replace(' ', '')  # to remove head [[ and tail ]]
    for line in b.split('],['):
        row = list(map(int, line.split(',')))  # map = to convert the number from string (some has also space ) to integer
        matrix.append(row)
    return matrix

def uploadfile(path: str):
    pass

def parsecfg(path: str = f'{os.path.expanduser("~")}/.pyshare.json'):
    pass

def screenshot(coords, display: bool = False):
    if str(coords) == 'full':
        im = ImageGrab.grab()
    else:
        im = ImageGrab.grab(bbox=(coords[0][0], coords[0][1], coords[1][0], coords[1][1]))

    if display:
        im.show()

# to file
ImageGrab.grab_to_file('im.png')

def parsearg(argv):
    selection = False
    upload = False
    display = False

    root = tkinter.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.withdraw()
    root.destroy()
    coords = [[0, 0], [width, height]]

    try:
        opts, args = getopt.getopt(argv, "hfsc:ud", ["help", "full", "selection", "coords=", "upload", "display"])
    except getopt.GetoptError:
        print('Invalid argument.')
        raise SystemExit

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            helpMe()
            #raise SystemExit
        if opt in ("-s", "--selection"):
            selection = True
        elif opt in ("-f", "--full"):
            coords = 'full'
        elif opt in ("-c", "--coords"):
            coords = createMatrix(str(arg))
        elif opt in ("-u", "--upload"):
            upload = True
        elif opt in ("-d", "--display"):
            display = True
    
    print(opts)
    print(coords)

    # Use an xor gate to check if there are multiple screenshot modes
    #if bool(selection) + bool(full) + bool(coords) != 1:
    #    print('Exactly one screenshot mode is required.')
    #    raise SystemExit
    screenshot(coords, display)
    config = str(parsecfg())


def helpMe():
    helpMessage: str = """Usage: python3 pyshare.py [args]
  -h, --help              Display this message.
  -f, --full              Capture entire view.
  -s, --selection         Manually define screenshot coords.
  -c, --coords <string>   Custom coordinates.
        format <string>   '[[0,0],[1920,1080]]'
  -d, --display           Display image after capture."""
    print(helpMessage)


parsearg(sys.argv[1:])
raise SystemExit
