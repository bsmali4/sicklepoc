# coding = utf-8
import os

BASEPATH = ''


def getplugspath(refresh=False):
    global BASEPATH
    if refresh:
        BASEPATH = None
    if BASEPATH:
        return BASEPATH
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    return BASEPATH