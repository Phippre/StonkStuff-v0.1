from yahoo_fin.stock_info import *
import tkinter as tk
from tkinter import *
import tkinter.font as font
from PIL import ImageTk, Image
import os
import time

isMonitoring = False

root = tk.Tk()
root.title('~Stonk Stuff v0.1')
root.geometry('400x400')
root.configure()
root.iconbitmap('StockInfo/rocket2.ico')

space_img = ImageTk.PhotoImage(Image.open("StockInfo/space_2.png"))
space_label = Label(image = space_img)
space_label.place(x=-2, y=-2)

moon_img = ImageTk.PhotoImage(Image.open("StockInfo/moon.png"))
moon_label = Label(image=moon_img, borderwidth=0)
moon_label.place(x=250)

courier_new = font.Font(family='Courier New', size=20)
font2 = font.Font(family='Comic Sans MS', size=8)

entry = Entry(root, width=25, borderwidth=1)
entry.place(x=125, y=5)

def enterStock():
    isMonitoring = True
    ticker = entry.get()
    livePrice = get_live_price(ticker.upper())
    myLabel = Label(root, text=livePrice, bg='#C09F52', foreground='#00FF21', font=courier_new, borderwidth=3, relief="ridge")
    myLabel.place(x=50, y=150)
    while isMonitoring:
        myLabel.configure(text=get_live_price(ticker.upper()))
        root.update()

def cancelProcess():
    isMonitoring = False
    print(isMonitoring)

button = Button(root, text="Enter", command=enterStock, width=21, borderwidth=1, background='green', relief='ridge', font=font2)
button.place(x=125, y=30)

cancelButton = Button(root, text="Stop", command=cancelProcess, width=21, borderwidth=1, background='maroon', relief='ridge', font=font2)
cancelButton.place(x=125, y=80)

doge_img = ImageTk.PhotoImage(Image.open("StockInfo/doge2.png"))
doge_label = Label(image = doge_img, background='#17211E')
doge_label.place(y = 220)

root.mainloop()


#ticker = input("Please enter a ticker symbol \n")

#while True:
    #print(get_live_price(ticker.upper()))