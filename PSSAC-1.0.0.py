# Python 简单频谱分析仪控制软件
# Python Simple Signal Analyzer Controller 1.0.0
import numpy as np
import time as Time
import pyvisa as visa
import matplotlib.pyplot as plt
import os
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import time
#导入所需库
plt.rcParams['font.sans-serif']=['Songti SC'] #macOS用来正常显示中文标签
#plt.rcParams['font.sans-serif']=['SimHei'] #Windows用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
main = tk.Tk()#窗体创建
main.minsize(350,250)#设置窗体大小
#main.resizable(False, False)
main.title("Python Simple Signal Analyzer Controller 1.0.0")#设置窗体名称


#函数定义区:
def lj():
    #定义连接命令
    getip = tk.Entry.get(set_ip)
    ljip = "TCPIP0::%s::inst0::INSTR"%(getip)
    rm = visa.ResourceManager()
    inst = rm.open_resource(ljip) #TCP/IP口连接设备
    name=inst.query("*IDN?") #读仪表名称
    print("已经连接的仪表名称："+name) #显示连接仪表名称
    inst.write("*CLS") #清理寄存器
    stopF = inst.query(":FREQ:STOP?")  # 读截止频率
    starF = inst.query(":FREQ:STARt?")  # 读起始频率
    centF = inst.query(":FREQ:CENT?")  # 读中心频率
    span = inst.query(":FREQ:SPAN?")  # 读SPAN
    reflevel = inst.query("DISP:WIND:TRAC:Y:RLEV?")  # 读参考电平
    reflevel = str(float(reflevel))
    rfatten = inst.query(":POW:ATT?")  # 读衰减值
    rfatten = str(float(rfatten))
    resBW = inst.query(":BAND:RES?")  # 读分辨率带宽
    vBW = inst.query(":BAND:VID?")  # 读视频带宽
    stime = inst.query(":SWEep:time?")  # 读取扫描时间
    stime = float(stime)
    point = inst.query(":SWEep:POINts?")  # 读取扫描点数
    main.minsize(650,350)#设置窗体大小
    # 仪器名称
    machine_name = "已连接:%s" % (name)
    machine_info = tk.Label(main, text=machine_name)
    machine_info.grid(column=0, row=0, columnspan=5)

    # 扫描时间
    # 扫描时间提示
    ts_swep_time = tk.Label(main, text='扫描时间:'+"%3.6f s"%(stime))
    ts_swep_time.grid(column=0, row=11)

    # 扫描点数
    # 扫描点数提示
    ts_swep_point = tk.Label(main, text='扫描点数:'+str(point[:-1]))
    ts_swep_point.grid(column=2, row=11)
    #刷新按钮
    rf = tk.Button(main, text="刷新数据", command=refresh)
    rf.grid(column=2, row=1)

    startF_input.delete(0, 'end')
    startF_input.insert(0, str(float(starF[:-1]) / 1000000) + "MHz")  # 填充起始频率
    stopF_input.delete(0, 'end')
    stopF_input.insert(0, str(float(stopF[:-1]) / 1000000) + "MHz")  # 填充终止频率
    centerF_input.delete(0, 'end')
    centerF_input.insert(0, str(float(centF[:-1]) / 1000000) + "MHz")  # 填充中心频率
    resBW_input.delete(0, 'end')
    resBW_input.insert(0, str(float(resBW[:-1]) / 1000) + "KHz")  # 分辨率带宽
    vBW_input.delete(0, 'end')
    vBW_input.insert(0, str(float(vBW[:-1]) / 1000) + "KHz")  # 分辨率带宽
    SPAN_input.delete(0, 'end')
    SPAN_input.insert(0, str(float(span[:-1]) / 1000000) + "MHz")  # 分辨率带宽
    reflevel_input.delete(0, 'end')
    reflevel_input.insert(0, reflevel[:-1] + "dBm")  # 参考电平
    rfatten_input.delete(0, 'end')
    rfatten_input.insert(0, rfatten + "dB")  # 衰减值
    pic()
    ts_ip.config(state="disabled")
    set_ip.config(state="disabled")
    ljb.config(state="disabled")
def refresh():
    #定义刷新函数
    #重新连接设备并读取数据
    getip = tk.Entry.get(set_ip)
    ljip = "TCPIP0::%s::inst0::INSTR" % (getip)
    rm = visa.ResourceManager()
    inst = rm.open_resource(ljip)  # TCP/IP口连接设备
    name = inst.query("*IDN?")  # 读仪表名称
    print("刷新成功")  # 显示连接仪表名称
    inst.write("*CLS")  # 清理寄存器
    stopF = inst.query(":FREQ:STOP?")  # 读截止频率
    starF = inst.query(":FREQ:STARt?")  # 读起始频率
    centF = inst.query(":FREQ:CENT?")  # 读中心频率
    span = inst.query(":FREQ:SPAN?")  # 读SPAN
    reflevel = inst.query("DISP:WIND:TRAC:Y:RLEV?")  # 读参考电平
    reflevel = str(float(reflevel))
    rfatten = inst.query(":POW:ATT?")  # 读衰减值
    rfatten = str(float(rfatten))
    resBW = inst.query(":BAND:RES?")  # 读分辨率带宽
    vBW = inst.query(":BAND:VID?")  # 读视频带宽
    stime = inst.query(":SWEep:time?")  # 读取扫描时间
    stime = float(stime)
    point = inst.query(":SWEep:POINts?")  # 读取扫描点数
    # 扫描时间
    # 扫描时间提示
    ts_swep_time = tk.Label(main, text='扫描时间:'+"%3.6f s"%(stime))
    ts_swep_time.grid(column=0, row=11)

    # 扫描点数
    # 扫描点数提示
    ts_swep_point = tk.Label(main, text='扫描点数:'+str(point[:-1]))
    ts_swep_point.grid(column=2, row=11)

    #清空Entry数据并写入新数据
    startF_input.delete(0, 'end')
    startF_input.insert(0, str(float(starF[:-1]) / 1000000) + "MHz")  # 填充起始频率
    stopF_input.delete(0, 'end')
    stopF_input.insert(0, str(float(stopF[:-1]) / 1000000) + "MHz")  # 填充终止频率
    centerF_input.delete(0, 'end')
    centerF_input.insert(0, str(float(centF[:-1]) / 1000000) + "MHz")  # 填充中心频率
    resBW_input.delete(0, 'end')
    resBW_input.insert(0, str(float(resBW[:-1]) / 1000) + "KHz")  # 分辨率带宽
    vBW_input.delete(0, 'end')
    vBW_input.insert(0, str(float(vBW[:-1]) / 1000) + "KHz")  # 分辨率带宽
    SPAN_input.delete(0, 'end')
    SPAN_input.insert(0, str(float(span[:-1]) / 1000000) + "MHz")  # 分辨率带宽
    reflevel_input.delete(0, 'end')
    reflevel_input.insert(0, reflevel[:-1] + "dBm")  # 参考电平
    rfatten_input.delete(0, 'end')
    rfatten_input.insert(0, rfatten + "dB")  # 衰减值
    pic()

def set_start():
    getip = tk.Entry.get(set_ip)
    ljip = "TCPIP0::%s::inst0::INSTR" % (getip)
    rm = visa.ResourceManager()
    inst = rm.open_resource(ljip)  # TCP/IP口连接设备
    name = inst.query("*IDN?")  # 读仪表名称
    inst.write("*CLS")  # 清理寄存器
    cmd_set_start=":FREQ:STARt %s"%(tk.Entry.get(startF_input))
    inst.write(cmd_set_start)  # 起始频率
    refresh()

def set_stop():
    getip = tk.Entry.get(set_ip)
    ljip = "TCPIP0::%s::inst0::INSTR" % (getip)
    rm = visa.ResourceManager()
    inst = rm.open_resource(ljip)  # TCP/IP口连接设备
    name = inst.query("*IDN?")  # 读仪表名称
    inst.write("*CLS")  # 清理寄存器
    cmd_set_stop=":FREQ:STOP %s"%(tk.Entry.get(stopF_input))
    inst.write(cmd_set_stop)  # 截止频率
    refresh()

def set_center():
    getip = tk.Entry.get(set_ip)
    ljip = "TCPIP0::%s::inst0::INSTR" % (getip)
    rm = visa.ResourceManager()
    inst = rm.open_resource(ljip)  # TCP/IP口连接设备
    name = inst.query("*IDN?")  # 读仪表名称
    inst.write("*CLS")  # 清理寄存器
    cmd_set_center="SENSe:FREQ:CENT %s"%(tk.Entry.get(centerF_input))
    inst.write(cmd_set_center)  # 中心频率
    refresh()

def set_resBW():
    getip = tk.Entry.get(set_ip)
    ljip = "TCPIP0::%s::inst0::INSTR" % (getip)
    rm = visa.ResourceManager()
    inst = rm.open_resource(ljip)  # TCP/IP口连接设备
    name = inst.query("*IDN?")  # 读仪表名称
    inst.write("*CLS")  # 清理寄存器
    cmd_set_resBW=":BAND:RES %s"%(tk.Entry.get(resBW_input))
    inst.write(cmd_set_resBW)  # 分辨率带宽
    refresh()

def set_vBW():
    getip = tk.Entry.get(set_ip)
    ljip = "TCPIP0::%s::inst0::INSTR" % (getip)
    rm = visa.ResourceManager()
    inst = rm.open_resource(ljip)  # TCP/IP口连接设备
    name = inst.query("*IDN?")  # 读仪表名称
    inst.write("*CLS")  # 清理寄存器
    cmd_set_vBW = ":BAND:VID %s" % (tk.Entry.get(vBW_input))
    inst.write(cmd_set_vBW)  # 分辨率带宽
    refresh()

def set_SPAN():
    getip = tk.Entry.get(set_ip)
    ljip = "TCPIP0::%s::inst0::INSTR" % (getip)
    rm = visa.ResourceManager()
    inst = rm.open_resource(ljip)  # TCP/IP口连接设备
    name = inst.query("*IDN?")  # 读仪表名称
    inst.write("*CLS")  # 清理寄存器
    cmd_set_SPAN = "FREQ:SPAN %s" % (tk.Entry.get(SPAN_input))
    inst.write(cmd_set_SPAN)  # 分辨率带宽
    refresh()

def set_reflevel():
    getip = tk.Entry.get(set_ip)
    ljip = "TCPIP0::%s::inst0::INSTR" % (getip)
    rm = visa.ResourceManager()
    inst = rm.open_resource(ljip)  # TCP/IP口连接设备
    name = inst.query("*IDN?")  # 读仪表名称
    inst.write("*CLS")  # 清理寄存器
    cmd_set_reflevel = "DISP:WIND:TRAC:Y:RLEV %s" % (tk.Entry.get(reflevel_input))
    inst.write(cmd_set_reflevel)  # 参考电平
    refresh()

def set_rfatten():
    getip = tk.Entry.get(set_ip)
    ljip = "TCPIP0::%s::inst0::INSTR" % (getip)
    rm = visa.ResourceManager()
    inst = rm.open_resource(ljip)  # TCP/IP口连接设备
    name = inst.query("*IDN?")  # 读仪表名称
    inst.write("*CLS")  # 清理寄存器
    cmd_set_rfatten = ":POW:ATT %s" % (tk.Entry.get(rfatten_input))
    inst.write(cmd_set_rfatten)  # 参考电平
    refresh()

def pic():

    plt.rcParams['font.sans-serif']=['Songti SC'] #用来正常显示中文标签
    plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
    data = []
    f = Figure(figsize=(12, 7), dpi=75)
    a = f.add_subplot(111)  # 添加子图:1行1列第1个
    a.patch.set_facecolor('black')

    # 打开相关端口 连接仪表相应地址———————————————————
    rm = visa.ResourceManager()
    inst = rm.open_resource('TCPIP0::192.168.0.118::inst0::INSTR') #TCP/IP口连接设备
    name=inst.query("*IDN?") #读仪表名称
    inst.write("*CLS") #清理寄存器
    #读取仪器测量参数—————————————————————————
    stopF=inst.query(":FREQ:STOP?") #读截止频率
    starF=inst.query(":FREQ:STARt?") #读起始频率
    point=inst.query(":SWEep:POINts?") #读取扫描点数
    #读取迹线数据并存储在TXT文件中 TRAC? TRACE1————————————

    for i in range(1):
        trac1data=inst.query("TRAC:DATA? TRACE1") #读出迹线1的每点数据
        print(trac1data) #列出每个点的值
        data.append([float(i) for i in trac1data.strip().split(',')])
    
    #绘制频谱图————————————————————————————
    #x=np.array(range(int(float(starF[:-1])/1000),int(float(stopF[:-1])/1000),20))
    #x=np.array(int(float(stopF[:-1])/1000))
    data = np.array(data)
    #x=range(int(float(starF[:-1])/1000000),int(float(stopF[:-1])/1000000),2)
    a.set_title("频谱图")
    #a.set_xticks(np.arange(88, 108, step=2))
    a.set_xlabel('点数') #设置X坐标名称（应当改为频率值）
    a.set_ylabel('电平:dBm') #设置Y坐标名称
    a.grid()
    a.plot(data.T, color="yellow", linewidth=0.8)
    #a.plot(x,data)

    # 在前面得到的子图上绘图
    #a.plot(x, y, color='blue')

    # 将绘制的图形显示到tkinter:创建属于main的canvas画布,并将图f置于画布上
    canvas = FigureCanvasTkAgg(f, master=main)
    canvas.draw()  # 注意show方法已经过时了,这里改用draw
    canvas.get_tk_widget().grid(column=4, row=1, rowspan=9)
    # matplotlib的导航工具栏显示上来(默认是不会显示它的)
    #toolbar = NavigationToolbar2Tk(canvas, main)
    #toolbar.update()
    #canvas._tkcanvas.grid(column=4, row=1, rowspan=9)


#频谱仪连接
#提示IP输入框
ts_ip=tk.Label(main, text='IP地址:')
ts_ip.grid(column=0, row=1)
#设置IP
set_ip = tk.Entry(main)
set_ip.grid(column=1, row=1)
#连接频谱仪并读取数据
ljb = tk.Button(main, text="连接仪器", command=lj)
ljb.grid(column=2, row=1)

#起始频率
#起始频率输入框提示
ts_startF=tk.Label(main, text='起始频率:')
ts_startF.grid(column=0, row=2)
#设置起始频率输入框
startF_input = tk.Entry(main)
startF_input.grid(column=1, row=2)
#设置起始频率按键
set_startF = tk.Button(main, text="更改数据", command=set_start)
set_startF.grid(column=2, row=2)

#终止频率
#终止频率输入框提示
ts_stopF=tk.Label(main, text='终止频率:')
ts_stopF.grid(column=0, row=3)
#终止终止频率输入框
stopF_input = tk.Entry(main)
stopF_input.grid(column=1, row=3)
#设置终止频率按键
set_stopF = tk.Button(main, text="更改数据", command=set_stop)
set_stopF.grid(column=2, row=3)

#中心频率
#中心频率输入框提示
ts_centerF=tk.Label(main, text='中心频率:')
ts_centerF.grid(column=0, row=4)
#中心终止频率输入框
centerF_input = tk.Entry(main)
centerF_input.grid(column=1, row=4)
#设置中心频率按键
set_centerF = tk.Button(main, text="更改数据", command=set_center)
set_centerF.grid(column=2, row=4)

#SPAN
#SPAN宽输入框提示
ts_resBW=tk.Label(main, text='SPAN:')
ts_resBW.grid(column=0, row=5)
#SPAN输入框
SPAN_input = tk.Entry(main)
SPAN_input.grid(column=1, row=5)
#设置SPAN按键
set_SPAN = tk.Button(main, text="更改数据", command=set_SPAN)
set_SPAN.grid(column=2, row=5)

#分辨率带宽
#分辨率带宽输入框提示
ts_resBW=tk.Label(main, text='分辨率带宽:')
ts_resBW.grid(column=0, row=6)
#分辨率带宽输入框
resBW_input = tk.Entry(main)
resBW_input.grid(column=1, row=6)
#设置分辨率带宽按键
Bset_resBW = tk.Button(main, text="更改数据", command=set_resBW)
Bset_resBW.grid(column=2, row=6)

#视频带宽
#视频带宽输入框提示
ts_vBW=tk.Label(main, text='视频带宽:')
ts_vBW.grid(column=0, row=7)
#视频带宽输入框
vBW_input = tk.Entry(main)
vBW_input.grid(column=1, row=7)
#设置视频带宽按键
Bset_vBW = tk.Button(main, text="更改数据", command=set_vBW)
Bset_vBW.grid(column=2, row=7)

#参考电平
#参考电平输入框提示
ts_reflevel=tk.Label(main, text='参考电平:')
ts_reflevel.grid(column=0, row=8)
#参考电平输入框
reflevel_input = tk.Entry(main)
reflevel_input.grid(column=1, row=8)
#设置参考电平按键
set_reflevel = tk.Button(main, text="更改数据", command=set_reflevel)
set_reflevel.grid(column=2, row=8)

#衰减值
#衰减值输入框提示
ts_rfatten=tk.Label(main, text='衰减值:')
ts_rfatten.grid(column=0, row=9)
#衰减值输入框
rfatten_input = tk.Entry(main)
rfatten_input.grid(column=1, row=9)
#设置衰减值按键
set_rfatten = tk.Button(main, text="更改数据", command=set_rfatten)
set_rfatten.grid(column=2, row=9)




# matplotlib的导航工具栏显示上来(默认是不会显示它的)
#toolbar = NavigationToolbar2Tk(canvas, main)
#toolbar.update()
#canvas._tkcanvas.grid(column=4, row=1, rowspan=9)


# #语法需要
main.mainloop()


