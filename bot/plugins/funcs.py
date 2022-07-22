'''Impoting Libraries and Modules'''
from bot.credentials import *
from inspect import currentframe
from os import path
from math import log2
from requests import head
import __main__


'''Defining Some Functions'''
#Function to find error in which file and in which line
def line_number():
    cf = currentframe()
    return f'In File {path.basename(__main__.__file__)} at line {cf.f_back.f_lineno}'
    
def humanbytes(size):
    if not size: return ""
    _suffixes = ['bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
    order = int(log2(size) / 10) if size else 0
    return '{:.4g} {}'.format(round(size / (1 << (order * 10)), 1), _suffixes[order])
    
#Task Updating or Status Checking
def task(status=None):
    if status:
        with open('task.txt', 'w') as newfile:
            newfile.writelines([status])
    else:
        try:
            with open('task.txt') as file:
                return file.readlines()[0]
        except FileNotFoundError:
            return "No Task"

