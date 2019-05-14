# -*- coding: utf-8 -*-


"""pyshare.pyshare: provides entry point main()."""


__version__ = "0.0.1"


import os
import sys
import getopt

from .config import *


def parsearg(argv):
    """Parse arguments.

    :param argv: arguments
    :type argv: array
    """
    service = defaultService

    try:
        opts, args = getopt.getopt(argv, "hc:", ["help", "custom="])
    except getopt.GetoptError:
        print('Invalid argument')
        raise SystemExit

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            helpMe()
            raise SystemExit
        elif opt in ("-c", "--custom"):
            service = str(arg)

    print(f'Uploaded file to {service}.')
    raise SystemExit

def helpMe():
    """Help formatter.
    """
    helpMessage: str = """Usage: python3 pyshare.py [args]

 -h, --help              Display this message.
 -c, --custom <string>   Custom file uploader."""
    print(helpMessage)


parsearg(sys.argv[1:])
raise SystemExit
