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
from tkinter import ttk
from tkinter.ttk import Separator, Progressbar, Notebook
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

STATES = [
    'Reserved',
    'DC Motor Position (GUI)',
    'DC Motor Velocity (GUI)',
    'DC Motor Position (Sensor)',
    'DC Motor Velocity (Sensor)',
    'Stepper Motor (GUI)',
    'Stepper Motor (Sensor)',
    'Servo Motor (GUI)',
    'Servo Motor (Sensor)',
]


class SensorPanel:
    def __init__(self, name, min_val, max_val, parent, row, column, padx):
        # Sensor properties
        self.name = name
        self.min_val = min_val
        self.max_val = max_val

        # Append to Tk parent panel
        self.panel = Frame(parent, width=170, height=10, pady=3)
        if name:
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


class SectionTitle:
    def __init__(self, title, parent, row, column, width):
        Separator(parent, orient=HORIZONTAL).grid(row=row, column=column, sticky=(W, E))
        self.panel = Frame(parent, width=width, height=10, pady=10)
        self.panel.grid(row=row, column=column)
        self.label = Label(self.panel, text=" %s " % title)
        self.label.pack()


class StatePanel:
    def __init__(self, state, parent, row, column, width, padx):
        self.state_index = STATES.index(state)
        print('Create panel for state', self.state_index)

        self.panel = Frame(parent, width=width, pady=3)

        if self.state_index == 1:
            print('packing')
            SectionTitle('Sensor Data', self.panel, 0, 0, 170)
            self.sensor1 = SensorPanel(
                None, 0, 500, self.panel, row=1, column=0, padx=9
            )

            SectionTitle('Actuator Data', self.panel, 2, 0, 170)
            self.sensor2 = SensorPanel(None, 0, 50, self.panel, row=3, column=0, padx=9)

        elif self.state_index == 2:
            pass

        elif self.state_index == 3:
            pass

        elif self.state_index == 4:
            pass

        elif self.state_index == 5:
            pass

        elif self.state_index == 6:
            pass

        elif self.state_index == 7:
            pass

        elif self.state_index == 8:
            pass

        self.panel.grid(row=row, column=column, width=width, padx=padx)
        root.update()

    def destroy(self):
        print('Destroy panel for state', self.state_index)
        self.panel.destroy()


class GUI(object):
    def __init__(self, master):
        # Main Window
        master.title("Sensors and Motors Lab  |  Delta Autonomy")
        master.geometry('1100x800')
        master.resizable(width=False, height=False)

        self.ICON_PATH = PATH + 'images/da_icon.png'
        self.imgicon = PhotoImage(file=self.ICON_PATH)
        master.tk.call('wm', 'iconphoto', master._w, self.imgicon)

        #########################################################################################

        # Master Panel
        self.mpanel = Frame(master, width=1100, height=800, padx=5, pady=4)
        self.mpanel.pack()

        #########################################################################################

        # Left Panel
        self.lpanel = Frame(self.mpanel, width=170, height=800, pady=3)
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
        SectionTitle('Select COM Port', self.lpanel, 5, 0, 170)

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

        # State Select Panel
        SectionTitle('Select State', self.lpanel, 8, 0, 170)

        self.state = StringVar(master)
        self.states = STATES[1:]
        self.ddstate = OptionMenu(
            self.lpanel, self.state, *self.states, command=self.state_select
        )
        self.ddstate.config(width=22)
        self.ddstate.grid(row=9, column=0, padx=9)

        self.b2 = Button(
            self.lpanel, text="Start", width=22, command=self.b2_clicked, pady=4
        )
        self.b2.grid(row=10, column=0, padx=9, sticky=(W, E))
        self.b2.configure(state=DISABLED)

        #########################################################################################

        # Dynamic State Panel
        self.state_panel = Frame(self.lpanel, width=170, height=200, pady=3)
        self.dynamic_panel = None

        #########################################################################################

        # Seperator
        Separator(self.mpanel, orient=VERTICAL).grid(
            row=0, column=1, rowspan=20, sticky=(N, S), padx=6
        )

        #########################################################################################

        # Graph Panel
        Separator(self.mpanel, orient=HORIZONTAL).grid(row=0, column=4, sticky=(W, E))
        l3panel = Frame(self.mpanel, width=800, height=10, pady=3)
        l3panel.grid(row=0, column=4)
        tlabel = Label(l3panel, text=" Interactive Terminal ")
        tlabel.pack()

        tpanel = Frame(self.mpanel, bg='#AAAAAA', width=550, height=565, pady=3)
        tpanel.grid(row=1, column=2)

        # Insert Terminal
        # wid = tpanel.winfo_id()

    def get_com_ports(self):
        # Linux
        # TODO: update
        return glob.glob('tty[AU]*')  # return glob.glob('/dev/tty[AU]*')

    def comport_select(self, port):
        print('Port changed:', port)
        self.b1.configure(state=NORMAL)

    def state_select(self, state):
        print('State changed:', STATES.index(state), state)
        self.b2.configure(state=NORMAL)

        if self.dynamic_panel:
            self.dynamic_panel.destroy()

        self.dynamic_panel = StatePanel(
            state, self.state_panel, row=0, column=0, width=170, padx=3
        )

    def b1_clicked(self):
        print('B1 Clicked')
        if self.b1['text'] == 'Close Port':
            self.b1['text'] = 'Open Port'
            self.ddcom.configure(state=NORMAL)
        elif self.b1['text'] == 'Open Port':
            self.b1['text'] = 'Close Port'
            self.ddcom.configure(state=DISABLED)

    def b2_clicked(self):
        print('B2 Clicked')
        if self.b2['text'] == 'Stop':
            self.b2['text'] = 'Start'
            self.ddstate.configure(state=NORMAL)
        elif self.b2['text'] == 'Start':
            self.b2['text'] = 'Stop'
            self.ddstate.configure(state=DISABLED)

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
            try:
                app.sensor1.set_sensor_value(count)
                app.sensor2.set_sensor_value(count)
            except AttributeError:
                pass
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
