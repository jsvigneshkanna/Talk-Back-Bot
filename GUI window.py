#importing tkinter
import tkinter as tk
from tkinter import *

larger_font = ('verdana',20)
medium_font = ('verdana',10)
#creating main window
window = tk.Tk()
window.title("personal Bot !!!")
#configuring the window's geometry

window.geometry("1500x1500")
label1 = tk.Label(window, text =' Ask me anything: ').grid(row=0,column=0)
inp = Entry(window, bg='grey',width="75", font=larger_font)
inp.grid(row=1)

#creating search button
searchButton = tk.Button(window, text='search').grid(row=3,column=0)

#creating output box
label2 = tk.Label(window, text ='The answer is !!! ').grid(row=5,column=0)
message = tk.Canvas(window,bg='grey',width='1000',height ='600')
message.grid(row=6)
