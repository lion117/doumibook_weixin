# -*- coding: utf-8 -*-
"""
@author: HeSY
Date:  2016/4/29
Email:	lion_117@126.com
All Rights Reserved Licensed under the Apache License
"""

import os


import ctypes
g_dll = ctypes.CDLL('ProcessApi.dll')


def setupProcess(t_cmd , t_file ):
    i_pid = g_dll.setProcess('python','test_process')
    return i_pid

def setupProcessABS(t_cmd , t_file , t_dir):
    i_pid = g_dll.setProcess(t_cmd , t_file , t_dir)
    return i_pid



if __name__ == '__main__':
    print(setupProcessABS('NetAssist.exe', '../app.py' , 'D:/software program/'))
    pass
