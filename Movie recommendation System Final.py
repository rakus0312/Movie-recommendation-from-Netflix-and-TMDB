# import important libraries
from concurrent.futures import thread
from tkinter import messagebox
import pandas as pd
from pyparsing import col
import requests
from IPython.display import Image, display
import json
from rapidfuzz import fuzz,process

# read required datasets
ndata=pd.read_csv("./netflix_titles.csv")
tmdbmain=pd.read_csv('./tmdb_5000_movies.csv')
tmdbcred=pd.read_csv('./tmdb_5000_credits.csv')

# Merge datasets 
tdf=pd.DataFrame()
ndf=pd.DataFrame()

tdf['title'],tdf['description']=tmdbmain.original_title,tmdbmain.overview
ndf['title'],ndf['description']=ndata.title,ndata.description

merge=pd.concat((tdf,ndf),ignore_index=True)
merge=merge.fillna('')

df=merge

df.columns=['title','words']

# finding similarities between descriptions

from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer(stop_words='english',strip_accents='unicode',analyzer='word')
tfidf_matrix = tfidf.fit_transform(df['words'])  

from sklearn.metrics.pairwise import sigmoid_kernel
cosine_sim=sigmoid_kernel(tfidf_matrix, tfidf_matrix)

global images

#function to get similar movies using cosine similarity(Top and Sorted) as list
def fpred(event):

    # movie=input("Give name.")  
    movie=movieName.get()
    slist=pd.Series(dtype='object')
    idx=pd.Series(dtype='object')
    t=process.extract(movie, merge.title,limit=1)

    for i in t:
        similar=pd.Series(cosine_sim[i[2]]).sort_values(ascending=False)
        idx=idx.append(similar.iloc[0:6])
    idx=idx.sort_values(ascending=False)
    for j in range(len(idx)):
        smovies=merge['title'].iloc[idx.index[j]]
        slist=slist.append(pd.Series(smovies))
        slist=slist.drop_duplicates()
        list1=list(slist)
    print(slist.to_string(index=False))
    label3 = Label(root,text='Searching Please wait.....')
    label3.grid(row=4,column=2,sticky=N)
    root.update()
    disp_poster(list(slist))
    return 

global disp_poster

#function to get movie's name from TMDB database using TMDB API

def disp_poster(plist):
    images=[]
    for s in plist:
        url='https://api.themoviedb.org/3/search/multi?api_key=61bcd21296810ac31ae3f0607a117b59&language=en-US&query='+s+'&page=1&include_adult=false'
            
        data=requests.get(url,timeout=2).json()
        
        if not data['results']: break
        
        ppath=data['results'][0]['poster_path']
        
        url='https://image.tmdb.org/t/p/original'+ppath
        
        img=requests.get(url,timeout=2)
        if not img: continue
        images.append(img)
        #for img,i in zip(images,range(len(images))):
        i=len(images)-1
        displayImg(images[i],i,s)
    return

#Function to display image 
def displayImg(img,i,n):
    root.geometry("900x900")
    label4 = Label(root,text='Showing you top 5 results')
    label4.grid(row=4,column=2,sticky=N)
    img = Image.open(BytesIO(img.content))
    photo = ImageTk.PhotoImage(img.resize((100,200),Image.ANTIALIAS))
    photos.append(photo)#keep references!
    newPhoto_label = Label(image=photo).grid(row=5,column=1*i,sticky=W)
    new_label=Label(text=n).grid(row=6,column=1*i,sticky=W)
    root.update()
    return

# Tkinter implementation

from tkinter import *
from PIL import Image, ImageTk
import glob, os
from io import BytesIO


root = Tk()
root.geometry("600x600")
photos = []

img=ImageTk.PhotoImage(file="bazaart-edit-app.jpg",size=50)
        
global movieName

movieName=StringVar()    

label = Label(
    root,
    image=img
)
label.place(x=0, y=0)

label2 = Label(
    root,
    text='Enter Movie Name Here'
)
label2.grid(row=0,column=2,sticky=N)

text = Entry(
    root,
    textvariable=movieName,
)
text.grid(row=2,column=2,sticky="E")
text.bind('<Return>',fpred)

def onClick():
    messagebox.showinfo("Searching",  "Please wait for some time. Don't close the window. It may hang")
    fpred(movieName)
    return
  
# Create a Button
button = Button(root, text="Search", command=onClick, height=1, width=10,)
button.grid(row=2,column=3,sticky='E')

root.mainloop()
