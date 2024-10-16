import os
import sqlite3



from flask import Flask, flash, jsonify, redirect, render_template, request, session

app = Flask(__name__)












FOODS = [
    "koshary",
    "Mulukhiyah",
    "kofta",
]


@app.route("/")
def index():
    return render_template ("index.html")

@app.route("/food")
def food():
    connection = sqlite3.connect("mydata.db")
    cursor = connection.cursor()
    cursor.execute("SELECT AVG(rate) FROM datas WHERE nam = ?", ('TAMIYA',))
    TAMIYA = cursor.fetchone()[0] or 0
    cursor.execute("SELECT AVG(rate) FROM datas WHERE nam = ?", ('KOSHARI',))
    KOSHARI = cursor.fetchone()[0] or 0

    cursor.execute("SELECT AVG(rate) FROM datas WHERE nam = ?", ('Mulukhiyah',))
    Mulukhiyah = cursor.fetchone()[0] or 0
    cursor.close()
    connection.close()
    return render_template ("food.html",TAMIYA=TAMIYA,KOSHARI=KOSHARI,Mulukhiyah=Mulukhiyah)

@app.route("/history")
def history():
    return render_template ("history.html")

@app.route("/tourism")
def tourism():
    connection = sqlite3.connect("mydata.db")
    cursor = connection.cursor()
    cursor.execute("SELECT AVG(rate) FROM datas WHERE nam = ?", ('Pyramids of Giza',))
    Pyramids = cursor.fetchone()[0] or 0
    cursor.execute("SELECT AVG(rate) FROM datas WHERE nam = ?", ('Luxors Temples & Tombs',))
    Temples = cursor.fetchone()[0] or 0

    cursor.execute("SELECT AVG(rate) FROM datas WHERE nam = ?", ('Cruising the Nile',))
    Nile = cursor.fetchone()[0] or 0
    cursor.close()
    connection.close()
    return render_template ("tourism.html",Nile=Nile,Temples=Temples,Pyramids=Pyramids)

@app.route("/votes", methods=['GET', 'POST'])
def votes():
    if request.method == 'POST':
        category = request.form.get('category')
        options = get_options_by_category(category)
        selection = request.form.get('selection')
        rating = int(request.form.get('rating'))
        if not selection :
            return render_template('votes.html', options=options)
        

        connection = sqlite3.connect("mydata.db")
        cursor = connection.cursor()
        
        cursor.execute("INSERT INTO datas (nam, rate) VALUES (?, ?)", (selection, rating))
        
        connection.commit()
        
        cursor.close()
        connection.close()
        

        return render_template('votes.html', options=options)
    
    return render_template('votes.html', options=[])

def get_options_by_category(category):
    options_by_category = {
        'food': ["TAMIYA", "KOSHARI", "Mulukhiyah"],
        'places': ["Pyramids of Giza", "Luxors Temples & Tombs", "Cruising the Nile"]
    }
    return options_by_category.get(category, [])
