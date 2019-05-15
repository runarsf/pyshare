# -*- coding: utf-8 -*-


"""pyshare.pyshare: provides entry point main()."""


__version__ = "0.0.1"


import os
import sys
import getopt

from .config import *

def parsecfg(path: str = f'{os.path.expanduser("~")}/.pyshare.json'):
    """Parse json config.

    :param path: path of json file
    :type path: str
    """
    pass

def parsearg(argv):
    """Parse arguments.

    :param argv: arguments
    :type argv: array
    """
    selection = False
    coords = False
    full = False

    try:
        opts, args = getopt.getopt(argv, "hfsc:", ["help", "full", "selection", "custom="])
    except getopt.GetoptError:
        print('Invalid argument')
        raise SystemExit

    print(opts)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            helpMe()
            raise SystemExit
        if opt in ("-s", "--selection"):
            selection = True
        elif opt in ("-f","--full"):
            full = True
        #elif opt in ("-t", "--type"):
        #    type = str(arg)

    # Use an xor gate to check if there are multiple screenshot modes
    if bool(selection) + bool(full) != 1:
        print('Exactly one screenshot mode is required.')
        raise SystemExit

    config = str(parsecfg())

def helpMe():
    """Help formatter.
    """
    helpMessage: str = """Usage: python3 pyshare.py [args]

 -h, --help              Display this message.
 -f, --full              Capture entire view.
 -s, --selection         Manually define screenshot coords.
 -c, --custom <string>   Custom json path."""
    print(helpMessage)


parsearg(sys.argv[1:])
raise SystemExit
