# -*- coding: utf-8 -*-
"""
@author: HeSY
Date:  2016/4/29
Email:	lion_117@126.com
All Rights Reserved Licensed under the Apache License
"""

import os
from multiprocessing import  Process
import subprocess


def main():
     p = subprocess.Popen("test_recover.py", stdin=subprocess.PIPE,
        stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell = False)



if __name__ == '__main__':
    main()
    pass
