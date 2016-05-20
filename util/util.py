# -*- coding: utf-8 -*-
"""
@author: HeSY
Date:  2016/4/25
Email:	lion_117@126.com
All Rights Reserved Licensed under the Apache License
"""

import os , time
import hashlib
import psutil
from  SetupProcess import *


g_filename=os.getcwd()+'/'+ 'test_process.py'
g_dir = os.getcwd()+'/'
g_process_name ='python.exe'
g_pid =0
g_file_md5=''



def getFileMD5(filepath):
    if os.path.isfile(filepath):
        with open(filepath, 'rb') as f:
            md5obj = hashlib.md5()
            md5obj.update(f.read())
            hash = md5obj.hexdigest()
            return str(hash).upper()
    return  None





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
    for proc in psutil.process_iter():
        # check whether the process name matches
        if proc.name() == t_process_name:
            proc.kill()


def killProcessByID(t_id):
    if t_id != 0:
        i_process = psutil.Process(t_id)
        i_process.kill()
        g_pid = 0


def beginMonitor(t_filename):
    g_file_md5 = getFileMD5(g_filename)
    print('watch dog wake up ')

    global  g_pid
    global  g_dir

    while(True):
        print('watch dog checking ...')

        i_md5 = getFileMD5(g_filename)
        if i_md5 != g_file_md5:
            print  'file changed: old file md5 :%s , new file md5: %s'%(g_file_md5 , i_md5)
            if g_pid !=0 :
                killProcessByID(g_pid)
            g_file_md5 = i_md5
            # setup process
            g_pid = setupProcessABS('python', t_filename,g_dir)
        else:
            if g_pid == 0:
                g_pid = setupProcessABS('python', t_filename, g_dir)
            time.sleep(5)








if __name__ == '__main__':
    beginMonitor('../app.py')


