import matplotlib

matplotlib.use("TkAgg")
import datetime as dt
import os
import tkinter as tk
import tkinter.font as font
from threading import *
from tkinter import *

import matplotlib.dates as mdates
import pandas_datareader
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import DateFormatter
from matplotlib.figure import Figure
from mpl_finance import candlestick_ohlc
from PIL import Image, ImageTk
from yahoo_fin.stock_info import *

isMonitoring = False

#Change Directory
os.chdir('C:/Users/parke/Documents/GitHub/StonkStuff')

#SETTING UP ROOT WINDOW~~~~~~~~
root = tk.Tk()
root.title('~Stonk Stuff v0.2')
root.geometry('1000x400')
root.configure()
root.iconbitmap('StonkStuff/res/rocket2.ico')
root.resizable(False, False)
root.attributes('-topmost', True)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#IMAGES AND FONTS~~~~~~~~~~~~~~
space_img = ImageTk.PhotoImage(Image.open("StonkStuff/res/space_2.png"))
space_label = Label(image = space_img, borderwidth=0)
space_label.place(width=400, height=400)

moon_img = ImageTk.PhotoImage(Image.open("StonkStuff/res/moon.png"))
moon_label = Label(image=moon_img, borderwidth=0)
moon_label.place(x=248)

doge_img = ImageTk.PhotoImage(Image.open("StonkStuff/res/doge3.png"))
doge_label = Label(image = doge_img, background='#17211E')
doge_label.place(x = -6, y = 220)

space_img2 = ImageTk.PhotoImage(Image.open("StonkStuff/res/space_3.png"))
space_label2 = Label(image = space_img, borderwidth=0)
space_label2.place(x=395)

space_img3 = ImageTk.PhotoImage(Image.open("StonkStuff/res/space_2.png"))
space_label3 = Label(image = space_img, borderwidth=0)
space_label3.place(x=600)

courier_new = font.Font(family='Courier New', size=20)
font2 = font.Font(family='Comic Sans MS', size=8)
font3 = font.Font(family='Comic Sans MS', size=20)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#METHODS~~~~~~~~~~~~~~~~~~~~~~~
def startThread():
    global t1

    t1 = Thread(target=enterStock)
    t1.start()

def updatePrice():
    global isMonitoring
    global ticker

    while isMonitoring == True:
        priceLabel.configure(text=get_live_price(ticker.upper()))
        root.update()
    else:
        return

def enterStock(event=None):
    global isMonitoring
    global priceLabel
    global tickerLabel
    global ticker

    isMonitoring = True
    ticker = entry.get()
    livePrice = get_live_price(ticker.upper())
    priceLabel = Label(root, text=livePrice, bg='#C09F52', foreground='#00FF21', font=courier_new, borderwidth=3, relief="ridge", width=20)
    priceLabel.place(x=45, y=150)
    tickerLabel = Label(root, text=ticker.upper(), bg='#C09F52', foreground='black', font=courier_new, borderwidth=3, relief='ridge', width=9)
    tickerLabel.place(relx=.125, y=110)
    processGraph()
    updatePrice()

def processGraph():
    global canvas
    #Start and end dates for graph
    start = dt.datetime(2021, 3, 1)
    end = dt.datetime.now()

    #Data
    data = pandas_datareader.DataReader('DOGE-USD', 'yahoo', start, end)
    data = data[['Open', 'High', 'Low', 'Close']]
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].map(mdates.date2num)

    #Graphics
    f = Figure(figsize=(1, 1), dpi=65)
    a = f.add_subplot(111)
    a.set_facecolor('#17211E')
    a.figure.set_facecolor('#17211E')
    a.grid(True)
    a.set_axisbelow(True)
    a.set_title('DOGE Price', color='white')
    a.tick_params(axis='x', colors='white')
    a.tick_params(axis='y', colors='white')
    myFmt = DateFormatter("%m / %d")
    a.xaxis.set_major_formatter(myFmt)
    candlestick_ohlc(a, data.values, width=.25, colorup='#00ff00')
    canvas = FigureCanvasTkAgg(f, root)
    canvas.draw()
    canvas.get_tk_widget().place(x=400, y=0, width=600, height=400)

def cancelProcess():
    global isMonitoring
    global t1
    global canvas

    isMonitoring = False
    tickerLabel.destroy()
    priceLabel.destroy()
    canvas.get_tk_widget().destroy()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#TEXT ENTRY FIELD~~~~~~~~~~~~~~
entry = Entry(root, width=25, borderwidth=1)
entry.place(x=125, y=5)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
#BUTTONS~~~~~~~~~~~~~~~~~~~~~~~
startButton = Button(root, text="Much Start", command=startThread, width=21, borderwidth=1, background='green', relief='ridge', font=font2)
startButton.place(x=125, y=35)

cancelButton = Button(root, text="Such Stop", command=cancelProcess, width=21, borderwidth=1, background='maroon', relief='ridge', font=font2)
cancelButton.place(x=125, y=65)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

root.bind('<Return>', enterStock)
root.mainloop()
