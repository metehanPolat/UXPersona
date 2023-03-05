import datetime
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import sqlite3
from tkinter import messagebox

con = sqlite3.connect("C:/Users/mete/Desktop/proje3 veritabanı/dataFrame.db")

df = pd.read_sql_query("SELECT * FROM People", con)
df['image_path'] = '/static/' + df['image_path'].astype(str)
app = Flask(__name__)

def myFilter(gender,ageSmall,ageBig,count):

    df_filter = df
    if(ageSmall != ''):
        df_filter = df[df["Age"] >= int(ageSmall)]
    if(ageBig !=''):
        df_filter = df_filter[df_filter["Age"] <= int(ageBig)]
    if(gender != "both"):
        df_filter = df_filter[df_filter["Gender"] == gender]
    if(count !='' and int(count) <= len(df_filter["Age"])):
        df_filter = df_filter.sample(n=int(count))


    return df_filter

@app.route('/', methods =["GET", "POST"])
def gfg():
    return render_template("StartPage.html")

@app.route('/home', methods=("POST", "GET"))
def hello():

    if request.method == "POST":
       humanCount = request.form.get("eCount")
       Gender = request.form.get("comp_select")
       age1 = request.form.get("aAroundSmall")
       age2 = request.form.get("aAroundBig")

       if (age1 != '' and age2 != '' and int(age1) > int(age2)):
           error = "YAŞ ARALIĞI HATALI!!!"
           return render_template("StartPage.html", error=error)
       elif((age1 != '' and int(age1) < 0) or (age2 != '' and int(age2) < 0)):
           error = "YAŞ ARALIĞI HATALI!!!"
           return render_template("StartPage.html", error=error)
       elif (humanCount != ''  and (int(humanCount) < 1 or int(humanCount) > 6 )):
           error = "İSTENİLEN KİŞİ SAYISI 1-6 ARASI OLMALIDIR!!!"
           return render_template("StartPage.html", error=error)
       else:

           price = request.args.get('income', 12000.00, type=float)

           df1 = myFilter(Gender, age1, age2, humanCount)

           items = df1.to_dict(orient='records')

           return render_template('index.html', items=items, humanCount=humanCount, gender=Gender, age1=age1, age2=age2, income=price)



app.run()