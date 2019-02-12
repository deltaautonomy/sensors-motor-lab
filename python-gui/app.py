#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Python GUI for Sensors and Motors Lab
'''

__author__ = "Heethesh Vhavle"
__version__ = "1.0.0"
__email__ = "heethesh@cmu.edu"

# Built-in modules
import os
import glob
import time

# External modules
import numpy as np
from tkinter import *
from tkinter.ttk import Separator, Progressbar
from PIL import ImageTk, Image
import matplotlib

matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Local modules
from utils import *
from packet import Packet

PATH = os.path.dirname(os.path.abspath(__file__)) + '/'
HOME_PATH = os.path.expanduser('~') + '/'

app = None
GUI_CLOSED = False

# Arduino packet object
arduino = Packet()


class SensorPanel:
    def __init__(self, name, min_val, max_val, parent, row, column, padx):
        # Sensor properties
        self.name = name
        self.min_val = min_val
        self.max_val = max_val

        # Append to Tk parent panel
        self.panel = Frame(parent, width=170, height=10, pady=3)
        self.name_label = Label(self.panel, text=name)
        self.name_label.grid(row=0, column=0, columnspan=2, padx=9)
        self.pb = Progressbar(
            self.panel, orient="horizontal", mode="determinate", length=140
        )
        self.pb.grid(row=1, column=0, sticky=(W, E))
        self.value_label = Entry(self.panel, width=7, justify=RIGHT)
        self.value_label.grid(row=1, column=1, padx=5, sticky=(W, E))
        self.panel.grid(row=row, column=column, padx=padx)
        self.set_sensor_value(0)

    def set_sensor_value(self, value):
        self.pb['value'] = map_value(value, self.min_val, self.max_val)
        self.value_label.delete(0, END)
        self.value_label.insert(0, value)


class GUI(object):
    def __init__(self, master):
        # Main Window
        master.title("Sensors and Motors Lab  |  Delta Autonomy")
        master.geometry('1100x600')
        master.resizable(width=False, height=False)

        self.ICON_PATH = PATH + 'images/da_icon.png'
        self.imgicon = PhotoImage(file=self.ICON_PATH)
        master.tk.call('wm', 'iconphoto', master._w, self.imgicon)

        #########################################################################################

        # Master Panel
        self.mpanel = Frame(master, width=1100, height=600, padx=5, pady=4)
        self.mpanel.pack()

        #########################################################################################

        # Left Panel
        self.lpanel = Frame(self.mpanel, width=170, height=600, pady=3)
        self.lpanel.grid(row=0, column=0, rowspan=4)

        #########################################################################################

        # Info Panel
        self.raisedFrame = Frame(self.lpanel, bd=3, relief=GROOVE)
        self.raisedFrame.grid(row=0, column=0)

        self.logo = ImageTk.PhotoImage(Image.open(PATH + 'images/da_logo_resize.png'))
        self.logolabel = Label(self.raisedFrame, image=self.logo, width=205)
        self.logolabel.grid(row=0, column=0)

        self.infolabel3 = Label(self.raisedFrame, text=" ", font='"Consolas" 2')
        self.infolabel3.grid(row=1, column=0)

        self.infolabel = Label(
            self.raisedFrame, text="Delta Autonomy", font='"Consolas" 12 bold'
        )
        self.infolabel.grid(row=2, column=0)

        self.infolabel2 = Label(
            self.raisedFrame,
            text="Sensors and Motors Lab GUI\nVersion %s" % __version__,
            font='"Consolas" 10',
        )
        self.infolabel2.grid(row=3, column=0)

        self.infolabel5 = Label(self.raisedFrame, text=" ", font='"Consolas" 4')
        self.infolabel5.grid(row=4, column=0)

        self.infolabel6 = Label(
            self.lpanel, text="\nInstructions", font='"Consolas" 11 bold'
        )
        self.infolabel6.grid(row=3, column=0)

        self.infotext = "Lorem Ipsum"
        self.infolabel4 = Label(
            self.lpanel, text=self.infotext, wraplength=205, font='"Consolas" 9'
        )
        self.infolabel4.grid(row=4, column=0)

        #########################################################################################

        # COM Port Panel
        Separator(self.lpanel, orient=HORIZONTAL).grid(row=5, column=0, sticky=(W, E))
        self.l1panel = Frame(self.lpanel, width=170, height=10, pady=10)
        self.l1panel.grid(row=5, column=0)
        self.tlabel = Label(self.l1panel, text=" Select COM Port ")
        self.tlabel.pack()

        self.comport = StringVar(master)
        self.comports = self.get_com_ports()
        self.ddcom = OptionMenu(
            self.lpanel, self.comport, *self.comports, command=self.comport_select
        )
        self.ddcom.config(width=22)
        self.ddcom.grid(row=6, column=0, padx=9)

        self.b1 = Button(
            self.lpanel, text="Open Port", width=22, command=self.b1_clicked, pady=4
        )
        self.b1.grid(row=7, column=0, padx=9, sticky=(W, E))
        self.b1.configure(state=DISABLED)

        #########################################################################################

        Separator(self.lpanel, orient=HORIZONTAL).grid(row=8, column=0, sticky=(W, E))
        self.l2panel = Frame(self.lpanel, width=170, height=10, pady=10)
        self.l2panel.grid(row=8, column=0)
        self.tlabel = Label(self.l2panel, text=" Select Sensor ")
        self.tlabel.pack()

        self.sensor1 = SensorPanel(
            'Sensor1', 0, 500, self.lpanel, row=9, column=0, padx=9
        )
        self.sensor2 = SensorPanel(
            'Sensor2', 0, 50, self.lpanel, row=10, column=0, padx=9
        )

        # self.b2 = Button(self.lpanel, text="Button 2", width=22, command=self.b2_clicked, pady=4)
        # self.b2.grid(row=7, column=0, padx=9)

        # self.b3 = Button(self.lpanel, text="Button 3", width=22, command=self.b3_clicked, pady=4)
        # self.b3.grid(row=9, column=0, padx=9)

        # self.b7 = Button(self.lpanel, text="Button 4", width=22, command=self.b7_clicked, pady=4)
        # self.b7.grid(row=10, column=0, padx=9)

        # self.b4 = Button(self.lpanel, text="Button 5", width=22, command=self.b4_clicked, pady=4)
        # self.b4.grid(row=11, column=0, padx=9)

        # self.b5 = Button(self.lpanel, text="Button 6", width=22, command=self.b5_clicked, pady=4)
        # self.b5.grid(row=12, column=0, padx=9)

        # self.b6 = Button(self.lpanel, text="Button 7", width=22, command=self.b6_clicked, pady=4)
        # self.b6.grid(row=13, column=0, padx=9)

        #########################################################################################

        # Seperator
        Separator(self.mpanel, orient=VERTICAL).grid(
            row=0, column=1, rowspan=20, sticky=(N, S), padx=6
        )

        #########################################################################################

        # Right Panel
        self.rpanel = Frame(self.mpanel, width=170, height=600, pady=3)
        self.rpanel.grid(row=0, column=2, rowspan=4)

        #########################################################################################

        # Seperator
        Separator(self.mpanel, orient=VERTICAL).grid(
            row=0, column=3, rowspan=20, sticky=(N, S), padx=6
        )

        #########################################################################################

        # Graph Panel
        # Separator(self.mpanel, orient=HORIZONTAL).grid(row=0, column=4, sticky=(W, E))
        # l3panel = Frame(self.mpanel, width=600, height=10, pady=3)
        # l3panel.grid(row=0, column=4)
        # tlabel = Label(l3panel, text=" Interactive Terminal ")
        # tlabel.pack()

        # tpanel = Frame(self.mpanel, bg='#AAAAAA', width=550, height=565, pady=3)
        # tpanel.grid(row=1, column=2)

        # Insert Terminal
        # wid = tpanel.winfo_id()

    def get_com_ports(self):
        # Linux
        # TODO: update
        return glob.glob('tty[AU]*')  # return glob.glob('/dev/tty[AU]*')

    def comport_select(self, port):
        print('Port changed:', port)
        self.b1.configure(state=NORMAL)

    def b1_clicked(self):
        print('B1 Clicked')
        if self.b1['text'] == 'Close Port':
            self.b1['text'] = 'Open Port'
            self.ddcom.configure(state=NORMAL)
        elif self.b1['text'] == 'Open Port':
            self.b1['text'] = 'Close Port'
            self.ddcom.configure(state=DISABLED)

    def b2_clicked(self):
        pass

    def b3_clicked(self):
        pass

    def b4_clicked(self):
        pass

    def b5_clicked(self):

        pass

    def b6_clicked(self):
        pass

    def b7_clicked(self):
        pass


def packet_listener():
    count = 0
    while not GUI_CLOSED:
        if app:
            app.sensor1.set_sensor_value(count)
            app.sensor2.set_sensor_value(count)
            count += 1
        time.sleep(0.1)


if __name__ == '__main__':
    packet_listener_t = StoppableThread(target=packet_listener)
    packet_listener_t.start()

    root = Tk()
    app = GUI(root)
    root.mainloop()

    GUI_CLOSED = True
    packet_listener_t.stop()
