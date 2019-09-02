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


class BfieldViewer:
    '''利用万用表进行磁场观测，并利用电流源反馈进行磁场补偿'''
    def __init__(self): 
        #初始化，通过visa地址连接仪器
        self.file = self.create_file('Bfield')
        self.init_current()
        self.init_voltage()
        self.init_pic()
        
    def init_voltage(self):
        #连接万用表并创建数据列表
        self.volt_x = visa.ResourceManager().open_resource('TCPIP0::192.168.3.10::inst0::INSTR')
        self.volt_y = visa.ResourceManager().open_resource('TCPIP0::192.168.3.11::inst0::INSTR')
        self.volt_z = visa.ResourceManager().open_resource('TCPIP0::192.168.3.12::inst0::INSTR')
        self.volt_data = [0.0]*3
        
        self.read_volt()

    def read_volt(self):
        self.read_volt_x()
        self.read_volt_y()
        self.read_volt_z()
        
    def read_volt_x(self):
        #读取万用表的电压读数
        self.volt_x.write('MEAS?')
        self.volt_data[0] = self.convert(self.volt_x.read())
    def read_volt_y(self):
        self.volt_y.write('MEAS?')
        self.volt_data[1] = self.convert(self.volt_y.read())
    def read_volt_z(self):
        self.volt_z.write('MEAS?')
        self.volt_data[2] = self.convert(self.volt_z.read())
        
    def convert(self, str_data):
        #将万用表返回的电压字符串转换为浮点数
        n = str_data.split("\n")
        fn = float(n[0])
        #print(fn)
        return fn
        
    def create_file(self,file_name='Bfield'):
        #依据当前时间创建文件夹和txt文件
        year = time.strftime("%Y", time.localtime())
        month = time.strftime("%m", time.localtime())
        date = time.strftime("%d", time.localtime())
        name_time = time.strftime('%Hh-%Mm-%Ss', time.localtime())
        file_name = name_time + '_'+ file_name
        path = 'E:/ChenZ/Bfield/'+ year +'/'+ month +'/'+ date +'/'
        if not os.path.exists(path):
            os.makedirs(path)
        file = open(path + file_name +'.txt', 'w+')
        return file
        
    def write_file(self):
        #写入文件
        self.file.write( time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime()) )
        self.file.write('\t')
        self.file.write(str(time.time()))
        self.file.write('\t')
        for i in range(3):
            self.file.write(str(self.volt_data[i]))
            if i != 2:
                self.file.write('\t')
        self.file.write('\n')
        #self.file.flush()

    def write_file_i(self,i):
        #写入文件
        self.file.write( time.strftime('%Y-%m-%d_%H:%M:%S', time.localtime()) )
        self.file.write('\t')
        self.file.write(str(time.time()))
        self.file.write('\t')
        self.file.write(str(self.volt_data[i]))
        self.file.write('\t')
        self.file.write('\n')
        
    def init_pic(self):
        #创建并初始化显示图表
        
        plt.subplots_adjust(bottom=0.2)#底部空余大小，用来后续设置Start和Stop按钮
        
        #设置三组空的数组
        self.array1 = np.full(500,np.nan)
        self.array2 = np.full(500,np.nan)
        self.array3 = np.full(500,np.nan)
        
        #读取第一个数据，为解决数组全部为nan时plt总是失败的bug
        self.read_volt()
        self.updata_array()
        
        #设置子图参数
        self.ax1 = plt.subplot(311)
        self.line1, = plt.plot(self.array1)
        #print(self.line1)，测试代码
        self.ax2 = plt.subplot(312)
        self.line2, = plt.plot(self.array2)
        self.ax3 = plt.subplot(313)
        self.line3, = plt.plot(self.array3)
        
        #设置横轴坐标
        self.ax1.set_xlim(0,500)
        self.ax2.set_xlim(0,500)
        self.ax3.set_xlim(0,500)
        
    def clear_pic(self,event):
        #清除图标
        self.array1 = np.full(500,np.nan)
        self.array2 = np.full(500,np.nan)
        self.array3 = np.full(500,np.nan)
    
    def updata_array(self):
        self.updata_array_x()
        self.updata_array_y()
        self.updata_array_z()

    def updata_array_x(self):
        #更新数据数组
        self.array1 = np.delete(self.array1,0)
        self.array1 = np.append(self.array1,self.volt_data[0])
        #print(self.array1)，测试代码
    def updata_array_y(self):
        self.array2 = np.delete(self.array2,0)
        self.array2 = np.append(self.array2,self.volt_data[1])
    def updata_array_z(self):
        self.array3 = np.delete(self.array3,0)
        self.array3 = np.append(self.array3,self.volt_data[2])
        
        self.write_file()
        
    def updata_lim(self):
        #刷新图像纵轴坐标
        self.updata_array_x()
        self.updata_array_y()
        self.updata_array_z()
    def updata_lim_x(self): 
        max1 = np.nanmax(self.array1)
        min1 = np.nanmin(self.array1)
        lim1_min = min1 - 0.1*(max1-min1)
        lim1_max = max1 + 0.1*(max1-min1)
        if lim1_max > lim1_min:
            self.ax1.set_ylim(lim1_min,lim1_max)
        else:
            pass
        
    def updata_lim_y(self): 
        max2 = np.nanmax(self.array2)
        min2 = np.nanmin(self.array2)
        lim2_min = min2 - 0.1*(max2-min2)
        lim2_max = max2 + 0.1*(max2-min2)
        if lim2_max > lim2_min:
            self.ax2.set_ylim(lim2_min,lim2_max)
        else:
            pass
        
    def updata_lim_z(self): 
        max3 = np.nanmax(self.array3)
        min3 = np.nanmin(self.array3)
        lim3_min = min3 - 0.1*(max3-min3)
        lim3_max = max3 + 0.1*(max3-min3)
        if lim3_max > lim3_min:
            self.ax3.set_ylim(lim3_min,lim3_max)
        else:
            pass
        


    def init_current(self):
        #连接电流源并创建数据列表
        self.cur1 = visa.ResourceManager().open_resource('TCPIP0::192.168.3.101::9221::SOCKET')
        self.cur2 = visa.ResourceManager().open_resource('TCPIP0::192.168.3.102::inst0::INSTR')
        self.cur_data = [0.0]*3
        self.cur_data[0] = 0.274
        self.cur_data[1] = 0.316
        self.cur_data[2] = 0.1645
        #电流源1参数初始化
        self.cur1.write("*RST")
        time.sleep(0.5)
        self.cur1.write('V1 12;I1 0.1;OP1 1')
        self.cur1.write('V2 12;I2 0.1;OP2 1')
        #self.cur1.write("OVP1 12;OVP2 12")        #设置过压保护
        #电流源1参数初始化
        self.cur2.write("*RST")
        self.cur2.write('SOUR:FUNC CURR;:SOUR:RANG MAX;:OUTP ON')
        
    def gain(self):
        #设置增益系数,可选
        pass

    def curNum(self,volt_data):
        #确定补偿电流大小

        cur_x = 0.01
        cur_y = 0.02
        cur_z = 0.03
        return cur_x,cur_y,cur_z
    
    def output_cur(self):
        self.output_cur_x()
        time.sleep(0.4)
        self.output_cur_y()
        self.output_cur_z()
        #输出电流以补偿磁场
    def output_cur_x(self):
        if abs(self.cur_data[0]) > 0.0001:
            self.cur_data[0] += self.volt_data[0]/6
        self.cur1.write('I1 '+str(self.cur_data[0]))

    def output_cur_y(self):
        #time.sleep(0.4)
        if abs(self.cur_data[1]) > 0.0001:
            self.cur_data[1] += self.volt_data[1]/4.64
        self.cur1.write('I2 '+str(self.cur_data[1]))
    def output_cur_z(self):
        if abs(self.cur_data[2]) > 0.000001:
            self.cur_data[2] -= self.volt_data[2]/500
        self.cur2.write(':SOUR:LEV '+str(self.cur_data[2]))

        #cur = self.curNum()
        #self.cur1.write('OP1 1')
        #time.sleep(0.1)
        #self.cur1.write('I2 '+str(cur[1]))
        #self.cur1.write('OP2 1')
        #time.sleep(0.1)
        #self.cur2.write('I3 '+str(cur[2]))
        #self.cur2.write('OP3 1')

    def run_x(self):
        while self.trig_x:
            self.read_volt_x()
            self.updata_array_x()
            self.line1.set_ydata(self.array1)
            self.updata_lim_x()
            plt.draw()
            self.output_cur_x()

    #def run_y(self):
        #while self.trig_y:
            self.read_volt_y()
            self.updata_array_y()
            self.line2.set_ydata(self.array2)
            self.updata_lim_y()
            plt.draw()
            time.sleep(0.4)
            self.output_cur_y()

    def run_z(self):
        while self.trig_z:
            self.read_volt_z()
            self.updata_array_z()
            self.line3.set_ydata(self.array3)
            self.updata_lim_z()
            plt.draw()
            self.output_cur_z()

            
            #time.sleep(0.2)

    def Start(self, event):
        self.trig_x =True
        t_x =Thread(target=self.run_x)
        t_x.start()
        '''
        self.trig_y =True
        t_y =Thread(target=self.run_y)
        t_y.start()
        '''
        self.trig_z =True
        t_z =Thread(target=self.run_z)
        t_z.start()
        
    def Stop(self, event):
        self.trig_x =False
        self.trig_y =False
        self.trig_z =False


if __name__ == '__main__':
    control = BfieldViewer()
    
    #创建按钮并设置单击事件处理函数
    axprev = plt.axes([0.81,0.05,0.1,0.075])
    bprev = Button(axprev,'Stop')
    bprev.on_clicked(control.Stop)
    
    axnext = plt.axes([0.7,0.05,0.1,0.075])
    bnext = Button(axnext,'Start')
    bnext.on_clicked(control.Start)
    
    axnext1 = plt.axes([0.1,0.05,0.1,0.075])
    bnext1 = Button(axnext1,'clear_pic')
    bnext1.on_clicked(control.clear_pic)

    plt.show()