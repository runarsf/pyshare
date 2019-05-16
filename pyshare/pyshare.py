# -*- coding: utf-8 -*-


"""pyshare.pyshare: provides entry point main()."""


__version__ = "0.0.2"


import os
import sys
import json
import getopt
import pprint
import tkinter
import requests
import datetime
import pyperclip
import pyscreenshot as ImageGrab

from pynput.mouse import Listener
from pynput.mouse import Controller

from .config import *


def generateConfig(configFile: str = f'{os.path.expanduser("~")}/.pyshare.json'):
    with open(configFile) as cfg:
        data = json.load(cfg)

    for service in range(len(data['Services'])):
        if data['Services'][service]['Name'] == data['DefaultImageUploader']:
            serviceIndex = service
        else:
            pass

    config = data['Services'][serviceIndex]
    return config


def createMatrix(stringMatrix: str):
    matrix = []
    b = stringMatrix.replace('[[', '').replace(']]', '').replace(' ', '')  # to remove head [[ and tail ]]
    for line in b.split('],['):
        row = list(map(int, line.split(',')))  # map = to convert the number from string (some has also space ) to integer
        matrix.append(row)
    return matrix


def parsearg(argv):
    config = generateConfig()

    selection = False
    upload = False
    display = False
    coords = False
    copy = False
    filedir = f'{os.path.expanduser("~")}/.pyshare'
    filename = f'img-{str(datetime.datetime.now()).replace(" ", "-").replace(":", "_")}.png'
    filepath = f'{filedir}/{filename}'
    config['Headers']['token'] = os.environ[str(config['Headers']['token'])[1:]] if config['Headers']['token'].startswith('$') else config['Headers']['token']

    try:
        os.makedirs(filedir)
    except FileExistsError:
        pass

    try:
        opts, args = getopt.getopt(argv, "hfsp:udc", ["help", "full", "selection", "position=", "upload", "display", "copy"])
    except getopt.GetoptError:
        print('Invalid argument.')
        raise SystemExit

    if opts == []:
        print('Too few arguments.\n  --help for info.')
        raise SystemExit

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            helpMe()
            raise SystemExit
        if opt in ("-s", "--selection"):
            selection = True
        elif opt in ("-f", "--full"):
            coords = 'full'
        elif opt in ("-p", "--position"):
            coords = createMatrix(str(arg))
        elif opt in ("-u", "--upload"):
            upload = True
        elif opt in ("-d", "--display"):
            display = True
        elif opt in ("-c", "--copy"):
            copy = True
    
    if bool(coords) + bool(selection) != 1:
        print('Please make sure you passed the correct arguments.')
        raise SystemExit
    if bool(selection):
        coords = getSelection()

    screenshot(coords, filepath, display)
    if bool(upload):
        uploadfile(filename, filepath, config, copy)


def screenshot(coords, filepath: str, display: bool = False):
    try:
        validate = f'{int(coords[0][0])}{int(coords[0][1])}{int(coords[1][0])}{int(coords[1][1])}' # validate coordinates
        im = ImageGrab.grab(bbox=(coords[0][0], coords[0][1], coords[1][0], coords[1][1]))
    except:
        im = ImageGrab.grab()

    if display:
        im.show()

    im.save(filepath, 'PNG')


def uploadfile(filename: str, filepath: str, config, copy: bool = False):
    headers = {'token': config['Headers']['token']}
    files = {'files[]': open(filepath, 'rb')}
    r = requests.post(config['RequestURL'], files=files, headers=headers)
    print(json.loads(r.text)['files'][0]['url'])
    if copy:
        pyperclip.copy(json.loads(r.text)['files'][0]['url'])


def getSelection():
    coords = [[0,0],[0,0]]
    def on_move(x, y):
        pass
    def on_scroll(x, y, dx, dy):
        pass
    def on_click(x, y, button, pressed):
        #print(x, y, button, pressed)
        if str(button) == 'Button.left' and str(pressed) == 'True':
            coords[0][0] = x
            coords[0][1] = y
        if str(button) == 'Button.left' and str(pressed) == 'False':
            coords[1][0] = x
            coords[1][1] = y
            listener.stop()
    with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
        listener.join()
    return coords


def helpMe():
    helpMessage: str = """Usage: python3 pyshare.py [args]
  -h, --help              Display this message.
  -f, --full              Capture entire view.
  -s, --selection         Manually define screenshot coords.
  -c, --copy              Copy URL after capture.
  -p, --position <string> Custom coordinates.
        position <array>  '[[0,0],[1920,1080]]'
  -d, --display           Display image after capture.
  -u, --upload            Upload image after capture."""
    print(helpMessage)


parsearg(sys.argv[1:])
raise SystemExit
