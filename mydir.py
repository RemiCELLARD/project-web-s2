## -*- coding: utf-8 -*-

import inspect, os

def getCurrentDir():
    try :
        return os.path.join(os.getcwd(), os.path.dirname(os.path.abspath(__file__)))
    except NameError :
        __file__ = inspect.getfile(inspect.currentframe())
        return os.path.join(os.getcwd(), os.path.dirname(os.path.abspath(__file__)))

