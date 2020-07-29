# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 10:17:09 2020

@author: ataka
"""
#libraries
from sklearn.externals import joblib
import pandas as pd
import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import seaborn as sn
from tkinter import *
import os 
os.system("clear")
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer()
from sklearn.model_selection import train_test_split
import webbrowser

#loading models and countvectorizers
model = joblib.load("model.pkl")
cv2 = joblib.load("cv.pkl")
model_title = joblib.load("model_title.pkl")
cv_title = joblib.load("cv_title.pkl")

from PIL import Image, ImageTk



root = Tk()
root.title("Predicting Job Adverts-by Atakanoz")
root.geometry("400x500")

canvas = Canvas(root,width=400,height=500)
canvas.pack()
bgimage = ImageTk.PhotoImage(file="newspaper.jpg")
background_label = Label(root, image=bgimage, bg="grey")
background_label.place(relwidth=1, relheight=1)
root.wm_attributes("-transparentcolor", 'grey')

ICON = PhotoImage(file = "ao.png")
root.iconphoto(False, ICON)

root.resizable(width = False, height = False)

n_des = 1
def TitlePredict():  
    global n_des
    new_review = modelbox.get()
    massage_review = new_review
    modelbox.delete(0,"end")
    if massage_review == "":
        messagebox.showerror("Error","Please enter job advert description")
    else:
        new_review = re.sub('[^a-zA-Z]', ' ', new_review)
        new_review = new_review.lower()
        new_review = new_review.split()
        ps = PorterStemmer()
        all_stopwords = stopwords.words('english')
        all_stopwords.remove('not')
        new_review = [ps.stem(word) for word in new_review if not word in set(all_stopwords)]
        new_review = ' '.join(new_review)
        new_corpus = [new_review]
        new_X_test = cv2.transform(new_corpus).toarray()
        new_y_pred = model.predict(new_X_test)
        if new_y_pred == 1:
            messagebox.showerror("Description Hunter","Based on your job advert description, your job is Fraudulent!!!")
            massage_title = "{}) {} -->This description is Fraudulent!!!".format(n_des,massage_review)
            n_des += 1
            new_label = Label(new_window,text = massage_title, relief="solid")
            new_label.pack()
        else:
            messagebox.showinfo("Description Hunter","Based on your job advert description, your job is real and you can trust it :)")
            massage_title = "{}) {} -->This description is Real!".format(n_des,massage_review)
            n_des += 1
            new_label = Label(new_window,text = massage_title, relief="solid")
            new_label.pack()


n_title = 1
def Predict():   
    global n_title
    new_review = modelbox_title.get()
    modelbox_title.delete(0,"end")
    massage_review = new_review
    if massage_review == "":
        messagebox.showerror("Error","Please enter job advert title")
    else:
        new_review = re.sub('[^a-zA-Z]', ' ', new_review)
        new_review = new_review.lower()
        new_review = new_review.split()
        ps = PorterStemmer()
        all_stopwords = stopwords.words('english')
        all_stopwords.remove('not')
        new_review = [ps.stem(word) for word in new_review if not word in set(all_stopwords)]
        new_review = ' '.join(new_review)
        new_corpus = [new_review]
        new_X_test = cv_title.transform(new_corpus).toarray()
        new_y_pred = model_title.predict(new_X_test)
        if new_y_pred == 1:
            messagebox.showerror("Title Hunter","Based on your job advert title, your job is Fraudulent!!!")
            massage_title = "{}) {} -->This Title is Fraudulent!!!".format(n_title,massage_review)
            n_title +=1
            new_label = Label(new_window,text = massage_title,relief="solid")
            new_label.pack()
        else:
            messagebox.showinfo("Title Hunter","Based on your job advert title, your job is real and you can trust it")
            massage_title = "{}) {} -->This Title is Real!!!".format(n_title,massage_review)
            n_title +=1
            new_label = Label(new_window,text = massage_title, relief="solid")
            new_label.pack()

def button_hover(e):
    modelbutton["bg"] ="white"
def button_hover_leave(e):
    modelbutton["bg"] = "SystemButtonFace"
    
def button_hover2(e):
    Btn_google["bg"] ="white"
def button_hover_leave2(e):
    Btn_google["bg"] = "SystemButtonFace"
    
def button_hover3(e):
    modelbutton_title["bg"] ="white"
def button_hover_leave3(e):
    modelbutton_title["bg"] = "SystemButtonFace"

def openweb():
    new = 1
    new_review = modelbox_title.get()
    if new_review == "":
        messagebox.showerror("Error","Please enter job advert title")
    else:
        url = "https://www.google.com.tr/search?q={}".format(new_review)
        webbrowser.open(url,new=new)

Btn_google = Button(root, text = "Search this title in google", command=openweb, font="Helvetica 8 bold")
Btn_google.place(x=90,y=440)
Btn_google.bind("<Enter>", button_hover2)
Btn_google.bind("<Leave>", button_hover_leave2)

new_window = Toplevel(root)
new_window.title("Log")
new_window.geometry("200x300")           
def exit_function():
    warning = messagebox.askyesno("Close","Do you want to close Log? (You can not open it again)",icon="warning") 
    if warning == 1:
        new_window.destroy()        
new_window.protocol('WM_DELETE_WINDOW', exit_function)
new_window.iconphoto(False, ICON)


image = Image.open("besmart.jpg")
photo = image.resize((300,250),Image.ANTIALIAS)
photo = ImageTk.PhotoImage(photo)
label = Label(root, image=photo)
label.image = photo
label.place(x=55,y=1)

modelLabel = Label(root, text="Enter job description",font="Helvetica 8 bold")
modelLabel.place(x=145,y=270)

modelbox = Entry(root, width=20, bd=5, font=("Helvetica",18))
modelbox.place(x=65,y=295)

modelbutton = Button(root, text="Submit", command= TitlePredict, font="Helvetica 8 bold")
modelbutton.place(x=180,y=340)
modelbutton.bind("<Enter>", button_hover)
modelbutton.bind("<Leave>", button_hover_leave)

modelLabel_title = Label(root, text="Enter job Title",font="Helvetica 8 bold")
modelLabel_title.place(x=160,y=370)

modelbox_title = Entry(root, width=20, bd=5, font=("Helvetica",18))
modelbox_title.place(x=65,y=390)
#modelbox_title.place(relx=0.25,rely=0.65,relwidth=0.5,relheight=0.3)

modelbutton_title = Button(root, text="Submit", command= Predict, font="Helvetica 8 bold")
modelbutton_title.place(x=250,y=440)
modelbutton_title.bind("<Enter>", button_hover3)
modelbutton_title.bind("<Leave>", button_hover_leave3)

my_label = Label(root, text="This product is made by Atakan Özkan",font="Helvetica 6")
my_label.place(x=260,y=475)



root.mainloop()