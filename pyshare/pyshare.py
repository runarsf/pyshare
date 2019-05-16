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
import pyscreenshot as ImageGrab

from cv2 import cv2
import numpy as np

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
    filedir = f'{os.path.expanduser("~")}/.pyshare'
    filename = f'img-{str(datetime.datetime.now()).replace(" ", "-").replace(":", "_")}.png'
    filepath = f'{filedir}/{filename}'
    config['Headers']['token'] = os.environ[str(config['Headers']['token'])[1:]] if config['Headers']['token'].startswith('$') else config['Headers']['token']

    try:
        os.makedirs(filedir)
    except FileExistsError:
        pass

    try:
        opts, args = getopt.getopt(argv, "hfsc:ud", ["help", "full", "selection", "coords=", "upload", "display"])
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
        elif opt in ("-c", "--coords"):
            coords = createMatrix(str(arg))
        elif opt in ("-u", "--upload"):
            upload = True
        elif opt in ("-d", "--display"):
            display = True
    
    if bool(coords) + bool(selection) != 1:
        print('Please make sure you passed the correct arguments.')
        raise SystemExit
    if bool(selection):
        #    getSelection()
        raise SystemExit

    screenshot(coords, filepath, display)
    if bool(upload):
        uploadfile(filename, filepath, config)


def screenshot(coords, filepath: str, display: bool = False):
    try:
        validate = f'{int(coords[0][0])}{int(coords[0][1])}{int(coords[1][0])}{int(coords[1][1])}' # validate coordinates
        im = ImageGrab.grab(bbox=(coords[0][0], coords[0][1], coords[1][0], coords[1][1]))
    except:
        im = ImageGrab.grab()

    if display:
        im.show()

    im.save(filepath, 'PNG')


def uploadfile(filename: str, filepath: str, config):
    headers = {'token': config['Headers']['token']}
    files = {'files[]': open(filepath, 'rb')}
    r = requests.post(config['RequestURL'], files=files, headers=headers)
    print(json.loads(r.text)['files'][0]['url'])


# def getSelection():
#     # Read image
#     im = cv2.imread("image.jpg")

#     # Select ROI
#     r = cv2.selectROI(im)

#     # Crop image
#     imCrop = im[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

#     # Display cropped image
#     cv2.imshow("Image", imCrop)
#     cv2.waitKey(0)


def helpMe():
    helpMessage: str = """Usage: python3 pyshare.py [args]
  -h, --help              Display this message.
  -f, --full              Capture entire view.
  -s, --selection         Manually define screenshot coords.
  -c, --coords <string>   Custom coordinates.
        coords <format>   '[[0,0],[1920,1080]]'
  -d, --display           Display image after capture.
  -u, --upload            Upload picture after capture."""
    print(helpMessage)


parsearg(sys.argv[1:])
raise SystemExit
