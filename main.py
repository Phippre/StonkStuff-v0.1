import matplotlib

matplotlib.use("TkAgg")
import datetime as dt
import os
import tkinter as tk
import tkinter.font as font
from threading import Thread
from tkinter import *

import matplotlib.dates as mdates
import pandas_datareader
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import DateFormatter
from matplotlib.figure import Figure
from mpl_finance import candlestick_ohlc
from PIL import Image, ImageTk
from yahoo_fin.stock_info import *

#Change Directory
os.chdir('C:/Users/parke/Documents/GitHub/StonkStuff')

#SETTING UP ROOT WINDOW~~~~~~~~
root = tk.Tk()
root.title('~Stonk Stuff v0.3')
root.geometry('1000x400')
root.configure()
root.iconbitmap('StonkStuff/res/rocket2.ico')
root.resizable(False, False)
root.attributes('-topmost', True)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Declaring dates for graph~~~~~
end = dt.datetime.now()
start = end - dt.timedelta(weeks=7)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#Declaring global variables~~~~
isMonitoring = False
stopThread = False
tickerLabel = NONE
priceLabel = NONE
ticker = NONE
canvas = NONE
entry = NONE
data = NONE
t1 = NONE
f = NONE
a = NONE
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#IMAGES AND FONTS~~~~~~~~~~~~~~
#Here we are making images and font using the Tkinter functions
space_img = ImageTk.PhotoImage(Image.open("StonkStuff/res/space_2.png"))
doge_img = ImageTk.PhotoImage(Image.open("StonkStuff/res/doge3.png"))
moon_img = ImageTk.PhotoImage(Image.open("StonkStuff/res/moon.png"))

courier_new = font.Font(family='Courier New', size=20)

font3 = font.Font(family='Comic Sans MS', size=20)
font2 = font.Font(family='Comic Sans MS', size=8)
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#METHODS~~~~~~~~~~~~~~~~~~~~~~~
def renderAssets():
    #In this function we create assets and place them onto the GUI
    global entry

    space_label = Label(image = space_img, borderwidth=0)
    space_label.place(width=400, height=400)

    space_label2 = Label(image = space_img, borderwidth=0)
    space_label2.place(x=395)

    space_label3 = Label(image = space_img, borderwidth=0)
    space_label3.place(x=600)

    moon_label = Label(image=moon_img, borderwidth=0)
    moon_label.place(x=248)

    doge_label = Label(image = doge_img, background='#17211E')
    doge_label.place(x = -6, y = 220)
    
    startButton = Button(root, text="Much Start", command=startThread, width=21, borderwidth=1, background='green', relief='ridge', font=font2)
    startButton.place(x=50, y=55)

    cancelButton = Button(root, text="Such Stop", command=cancelProcess, width=21, borderwidth=1, background='maroon', relief='ridge', font=font2)
    cancelButton.place(x=50, y=85)
    
    entry = Entry(root, width=25, borderwidth=1)
    entry.place(x=50, y=25)

def startThread():
    #Starting a thread in the function that calls the "enterStock" function and sets off the chain reaction to call other functions
    #This function is called when clicking the start button. 
    global isMonitoring, t1

    #Set isMonitoring to true because once we start this thread the code for refreshing the stock kicks off
    isMonitoring = True
    #Create and start the thread here so it doesnt bogg down the main loop of the GUI. USE THREAD.RUN(). threading.Thread() function in the python threading library uses thread.run() so it doesnt crash
    t1 = Thread(target=enterStock)
    t1.run()

def enterStock(event=None):
    #This function is called by the Thread function. A lot here so I will explain line by line of my shitty organization and thought processes. 
    global priceLabel, tickerLabel, ticker

    #Getting ticker from input
    ticker = entry.get()
    #setting a variable for the live price. Making sure its in caps
    livePrice = get_live_price(ticker.upper())
    #Rendering these labels outside the render function because we only want to see them when the start button is pressed.
    priceLabel = Label(root, text=livePrice, bg='#C09F52', foreground='#00FF21', font=courier_new, borderwidth=3, relief="ridge", width=20)
    priceLabel.place(x=50, y=170)
    tickerLabel = Label(root, text=ticker.upper(), bg='#C09F52', foreground='black', font=courier_new, borderwidth=3, relief='ridge', width=9)
    tickerLabel.place(x=50, y=130)

    #Making the graph visible and constantly updating the stock price
    renderGraph()
    updatePrice()

def updatePrice():
    #A loop that is long that "isMonitoring" is true, it will ask the Yahoo API for the price and update the GUI
    while isMonitoring == True: #Dont call a refernece of the global variable "isMonitoring" here because im not changing the variable locally in the funtion
        global stopThread
        priceLabel.configure(text=get_live_price(ticker.upper()))
        root.update()
        #By default I set a stopThread boolean to detect if the cancel button was pressed. This if statement will check if the stopThread variable was changed to True. If it was then we reset stopThread to false and break the loop
        if stopThread == True:
            stopThread = False
            break

def renderGraph():
    global canvas, ticker, data

    #Grabbing data from the Yahoo finance API and stripping the data we need from it
    data = pandas_datareader.DataReader(ticker, 'yahoo', start, end)
    data = data[['Open', 'High', 'Low', 'Close']]
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].map(mdates.date2num)

    f = Figure(figsize=(1, 1), dpi=65)
    a = f.add_subplot(111)
    a.set_facecolor('#17211E')
    a.figure.set_facecolor('#17211E')
    a.grid(True)
    a.set_axisbelow(True)
    a.set_title(ticker + ' Price', color='white')
    a.tick_params(axis='x', colors='white')
    a.tick_params(axis='y', colors='white')
    myFmt = DateFormatter("%m / %d")
    a.xaxis.set_major_formatter(myFmt)
    #Converting data to a candlestick graph
    candlestick_ohlc(a, data.values, width=.25, colorup='#00ff00')
    #Drawing the canvas on the Figure
    canvas = FigureCanvasTkAgg(f, root)
    canvas.draw()
    canvas.get_tk_widget().place(x=400, y=0, width=600, height=400)

def cancelProcess():
    global tickerLabel, priceLabel, canvas, stopThread
    #stopThread is set to True here to kick off the deletion of the thread.
    stopThread = True
    #Destroying assets here. We destroy the canvas and not the actual Figure for multiple reasons. 1: It will crash, 2: Once we create the Figure it is blank and cached in ram. So, deleting it and recreating it every time would effect performance and load times. 
    tickerLabel.destroy()
    priceLabel.destroy()
    canvas.get_tk_widget().destroy()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

renderAssets()

root.bind('<Return>', enterStock)
root.mainloop()