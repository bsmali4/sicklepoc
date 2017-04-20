# coding=utf-8

from multiprocessing import cpu_count
import sys
import os

BASEPATH = ''


def setDefaultEncoding():
    reload(sys)
    sys.setdefaultencoding('utf-8')


def get_cpu_count():
    return cpu_count()


def getPath():
    pass


def getplugspath(refresh=False):
    global BASEPATH
    if refresh:
        BASEPATH = None
    if BASEPATH:
        return BASEPATH
    BASEPATH = os.path.abspath(os.path.dirname(__file__))
    return BASEPATH