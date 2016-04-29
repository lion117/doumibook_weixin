# -*- coding: utf-8 -*-
"""
@author: HeSY
Date:  2016/4/25
Email:	lion_117@126.com
All Rights Reserved Licensed under the Apache License
"""

import os,time,re,commands
import  psutil

def main():
    while(True):
        i_process = psutil.Process(os.getpid())
        print  'HI , this is from '+ i_process.name()
        time.sleep(1)



if __name__ == '__main__':
    main()
    pass
