from flask import Flask, render_template

app= Flask("Tabory")

@app.route('/')
def index():
    return render_template ("index.html")

@app.route('/tabory')
def tabory():
    return render_template ("tabory.html")

@app.route('/dobrovolnictvi')
def dobrovolnictvi():
    return render_template ("dobrovolnictvi.html")

@app.route('/prace')
def prace():
    return render_template ("prace.html")

@app.route('/onas')
def onas():
    return render_template ("onas.html")

@app.route('/registrace')
def registrace():
    return render_template ("registrace.html")
    
@app.route('/prihlaseni')
def prihlaseni():
    return render_template ("prihlaseni.html")



