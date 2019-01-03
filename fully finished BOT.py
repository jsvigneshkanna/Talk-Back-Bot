#importing tkinter
#importing the wolframalpha API to access it's portal
#importing wikipedia API, MODULE to access it' portal
import wolframalpha
import wikipedia
import tkinter as tk
from tkinter import *
#importing browser module
import webbrowser
#importing text to speech module
from gtts import gTTS


#passing the question ang language in which answer to be seen
def search():

    q = inp_que.get()
    
#change lang string to standard of wikipedia
    langu = inp_lang.get()
    if(langu.lower() == 'english'):
            langu ='en'
    elif(lang.lower() == 'tamil'):
            langu = 'ta'
    
           
#try the wolframalpha search
    try:
        app_id = "APP ID FROM WOLFRAMALPHA WEBSITE"
        client = wolframalpha.Client(app_id)
        result = client.query(q)
        #answer = next(result.results).text
        ans = next(result.results).text
        message.delete('1.0', END)
        message.insert('1.0',ans)

        gTTS(text =ans,lang='en' )
#if above doesn't satisfy then try wikipedia search
    except:

        wikipedia.set_lang(langu)
        #answer = wikipedia.summary(q)
        ans = wikipedia.summary(q)
        message.delete('1.0', END)
        message.insert('1.0',ans)

        gTTS(text=ans, lang=langu)
def browser():
    
        browser = inp_browser.get()
        if(browser.lower()=='google'):
                   url = "https://www.google.com"
                   gTTS(text="opening google",lang='en')
                   webbrowser.open_new(url)
        elif(browser.lower()=='youtube'):
                   url= "https://www.youtube.com"
                   gTTS(text="opening youtube",lang='en')
                   webbrowser.open_new(url)
    


larger_font = ('bold',15)
medium_font = ('verdana',15)
#creating main window
window = tk.Tk()
window.title("personal Bot !!!")
#configuring the window's geometry


mainframe =Frame(window, bg='#ff0000',cursor='dot',height='1500',width='1000')
mainframe.pack()

label1 = tk.Label(mainframe, text='Enter the question :',bg='#99ff99',font=larger_font).pack()
inp_que = Entry(mainframe, bg='#b3ecff',font=medium_font,width='100')
inp_que.pack()
#creating language input box
label2 = tk.Label(mainframe, text= 'Enter the language :',bg='#99ff99',font=larger_font).pack()
inp_lang = Entry(mainframe, bg='#b3ecff',font=medium_font,width='100')
inp_lang.pack()
label2 = tk.Label(mainframe, text= 'Enter the website to be opened :',bg='#99ff99',font=larger_font).pack()
inp_browser = Entry(mainframe, bg='#b3ecff',font=medium_font,width='100')
inp_browser.pack()


#creating search button
searchButton = tk.Button(mainframe, text='search answer',command = search,bg='#800080',foreground='#ffff00').pack()
searchBrowser = tk.Button(mainframe, text='open website',command = browser,bg='#800080',foreground='#ffff00').pack()



#creating output box
label3 = tk.Label(mainframe, text ='The answer is !!! ',bg='#99ff99',font=larger_font).pack()


message = tk.Text(mainframe,bg='#b3ecff',width='200',height ='600',pady=5,padx=5)
message.pack()
window.mainloop()
