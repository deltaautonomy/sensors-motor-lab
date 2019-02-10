#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Python GUI for Sensors and Motors Lab
'''

__author__ = "Heethesh Vhavle"
__version__ = "1.0.0"

import os

try:
    from Tkinter import *
except ImportError:
    from tkinter import *
try:
    from ttk import Separator
except ImportError:
    from tkinter.ttk import Separator
from PIL import ImageTk, Image

PATH = os.path.dirname(os.path.abspath(__file__)) + '/'
HOME_PATH = os.path.expanduser('~') + '/'


def b1_clicked():
    # os.system("xterm -into %d -geometry 550x565 -fa 'Ubuntu Mono' -fs 13 -fg black -bg white -sb -rightbar -hold -e 'bash $HOME/AutoSetup/oneshot_customer_setup.sh' &" % wid)
    pass


def b2_clicked():
    # os.system("xterm -into %d -geometry 550x565 -fa 'Ubuntu Mono' -fs 13 -fg black -bg white -sb -rightbar -hold -e 'bash $HOME/AutoSetup/oneshot_setup.sh' &" % wid)
    pass


def b3_clicked():
    # os.system("xterm -into %d -geometry 550x565 -fa 'Ubuntu Mono' -fs 13 -fg black -bg white -sb -rightbar -hold -e 'bash /opt/godeep/crontab.sh' &" % wid)
    pass


def b4_clicked():
    # os.system("xterm -into %d -geometry 550x565 -fa 'Ubuntu Mono' -fs 13 -fg black -bg white -sb -rightbar -hold -e 'bash $HOME/AutoSetup/delete_customer.sh' &" % wid)
    pass


def b5_clicked():
    # os.system("xterm -into %d -geometry 550x565 -fa 'Ubuntu Mono' -fs 13 -fg black -bg white -sb -rightbar -hold -e 'bash $HOME/AutoSetup/generate_license.sh' &" % wid)
    pass


def b6_clicked():
    # os.system("xterm -into %d -geometry 550x565 -fa 'Ubuntu Mono' -fs 13 -fg black -bg white -sb -rightbar -hold -e 'bash $HOME/AutoSetup/generate_settings.sh' &" % wid)
    pass


def b7_clicked():
    # os.system("xterm -into %d -geometry 550x565 -fa 'Ubuntu Mono' -fs 13 -fg black -bg white -sb -rightbar -hold -e 'bash /opt/godeep/kill_crontab.sh %d' &" % (wid, os.getpid()))
    pass


# Main Window
root = Tk()
root.title("Sensors and Motors Lab  |  Delta Autonomy")
root.geometry('800x600')
root.resizable(width=False, height=False)

ICON_PATH = PATH + 'images/da_icon.png'
imgicon = PhotoImage(file=ICON_PATH)
root.tk.call('wm', 'iconphoto', root._w, imgicon)

#########################################################################################

# Master Panel
mpanel = Frame(root, width=800, height=600, padx=5, pady=4)
mpanel.pack()

#########################################################################################

# Left Panel
lpanel = Frame(mpanel, width=170, height=600, pady=3)
lpanel.grid(row=0, column=0, rowspan=4)

raisedFrame = Frame(lpanel, bd=3, relief=GROOVE)
raisedFrame.grid(row=0, column=0)

logo = ImageTk.PhotoImage(Image.open(PATH + 'images/da_logo_resize.png'))
logolabel = Label(raisedFrame, image=logo, width=205)
logolabel.grid(row=0, column=0)

infolabel3 = Label(raisedFrame, text=" ", font='"Consolas" 2')
infolabel3.grid(row=1, column=0)

infolabel = Label(raisedFrame, text="Sensors and Motors Lab", font='"Consolas" 12 bold')
infolabel.grid(row=2, column=0)

infolabel2 = Label(raisedFrame, text="Version %s" % __version__, font='"Consolas" 10')
infolabel2.grid(row=3, column=0)

infolabel5 = Label(raisedFrame, text=" ", font='"Consolas" 4')
infolabel5.grid(row=4, column=0)

infolabel6 = Label(lpanel, text="\nInstructions", font='"Consolas" 11 bold')
infolabel6.grid(row=3, column=0)

infotext = "Select COM Port"
infolabel4 = Label(lpanel, text=infotext, wraplength=205, font='"Consolas" 9')
infolabel4.grid(row=4, column=0)

# blank = Label(lpanel, height=1)
# blank.grid(row=4, column=0)

#########################################################################################

# Buttons Panel
Separator(lpanel, orient=HORIZONTAL).grid(row=5, column=0, sticky=(W, E))
l1panel = Frame(lpanel, width=170, height=10, pady=10)
l1panel.grid(row=5, column=0)
tlabel = Label(l1panel, text=" Select Mode ")
tlabel.pack()

b1 = Button(lpanel, text="Button 1", width=22, command=b1_clicked, pady=4)
b1.grid(row=6, column=0, padx=9)

b2 = Button(lpanel, text="Button 2", width=22, command=b2_clicked, pady=4)
b2.grid(row=7, column=0, padx=9)

Separator(lpanel, orient=HORIZONTAL).grid(row=8, column=0, sticky=(W, E))
l2panel = Frame(lpanel, width=170, height=10, pady=10)
l2panel.grid(row=8, column=0)
tlabel = Label(l2panel, text=" Select Sensor ")
tlabel.pack()

b3 = Button(lpanel, text="Button 3", width=22, command=b3_clicked, pady=4)
b3.grid(row=9, column=0, padx=9)

b7 = Button(lpanel, text="Button 4", width=22, command=b7_clicked, pady=4)
b7.grid(row=10, column=0, padx=9)

b4 = Button(lpanel, text="Button 5", width=22, command=b4_clicked, pady=4)
b4.grid(row=11, column=0, padx=9)

b5 = Button(lpanel, text="Button 6", width=22, command=b5_clicked, pady=4)
b5.grid(row=12, column=0, padx=9)
if not os.path.isfile(HOME_PATH + 'null'):
    b5.configure(state=DISABLED)

b6 = Button(lpanel, text="Button 7", width=22, command=b6_clicked, pady=4)
b6.grid(row=13, column=0, padx=9)
if not os.path.isfile(HOME_PATH + 'null'):
    b6.configure(state=DISABLED)

#########################################################################################

Separator(mpanel, orient=VERTICAL).grid(
    row=0, column=1, rowspan=20, sticky=(N, S), padx=6
)

#########################################################################################

# Terminal Panel
Separator(mpanel, orient=HORIZONTAL).grid(row=0, column=2, sticky=(W, E))
l3panel = Frame(mpanel, width=600, height=10, pady=3)
l3panel.grid(row=0, column=2)
tlabel = Label(l3panel, text=" Interactive Terminal ")
tlabel.pack()

tpanel = Frame(mpanel, bg='#AAAAAA', width=550, height=565, pady=3)
tpanel.grid(row=1, column=2)

# Insert Terminal
wid = tpanel.winfo_id()

# Run Main
root.mainloop()
