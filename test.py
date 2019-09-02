import time
import os
import sys
import h5py
import visa
import numpy as np
import matplotlib.pyplot as plt
from ctypes import *
from sympy import *
from threading import Thread
from scipy import ndimage
from matplotlib.widgets import Button
from random import *

class Test:
    """测试"""
    def __init__(self):
        self.volt = visa.ResourceManager().open_resource('TCPIP0::192.168.3.10::inst0::INSTR')
        self.cur = visa.ResourceManager().open_resource('TCPIP0::192.168.3.102::inst0::INSTR')
        self.cur.write("*RST")
        self.cur.write('SOUR:FUNC CURR;:SOUR:RANG MAX;:OUTP ON')
        self.cur_data = 0.012

    def read_volt(self):
        t1 = time.time()
        i = 1
        for i  in range(10000):
            self.volt.query('MEAS?')
            i =+ 1
        t2 = time.time()
        print(t2-t1)

    '''
    def output_cur(self):
        t1 = time.time()
        i = 1
        for i in range(10000):
            self.cur_data = uniform(0,0.1)
            self.cur.write(':SOUR:LEV '+str(self.cur_data))
            i += 1
        t2 = time.time()
        print(t2-t1)
    '''

    def run(self):

        self.read_volt()
        #self.updata_array()
        #self.line.set_ydata(self.array)
        #self.updata_lim()
        #self.output_cur()
        #plt.draw()

if __name__ == '__main__':
    test = Test()
    test.run()

    #plt.show()