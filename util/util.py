# -*- coding: utf-8 -*-
"""
@author: HeSY
Date:  2016/4/25
Email:	lion_117@126.com
All Rights Reserved Licensed under the Apache License
"""

import os
import hashlib

g_file_md5=''
g_filename=os.getcwd()+'/'+ 'util.py'

def getFileMD5(filepath):
    if os.path.isfile(filepath):
        with open(filepath, 'rb') as f:
            md5obj = hashlib.md5()
            md5obj.update(f.read())
            hash = md5obj.hexdigest()
            return str(hash).upper()
    return  None


def isFileChanged():
    i_md5 = getFileMD5(g_filename)
    global  g_file_md5
    if g_file_md5 == i_md5:
        return True
    else:
        g_file_md5 = i_md5


def isProcessRun(t_process_name):
    import win32com.client
    WMI = win32com.client.GetObject('winmgmts:')
    processCodeCov = WMI.ExecQuery('select * from Win32_Process where Name="%s"' % t_process_name)
    if len(processCodeCov) > 0:
        print '%s is exists' % t_process_name
        return True
    else:
        print '%s is not exists' % t_process_name
        return False


def killProcess(t_process_name):
    import psutil
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == t_process_name:
            proc.kill()



if __name__ == '__main__':
    killProcess('Wechat.exe')