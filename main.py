from flask import Flask, render_template

app= Flask("Tabory")

@app.route('/')
def index ():
    return render_template ("index.html")

    @app.route('/tabory')
def index ():
    return render_template ("tabory.html")

@app.route('/dobrovolnicti')
def index ():
    return render_template ("dobrovolnictvi.html")

@app.route('/prace')
def index ():
    return render_template ("prace.html")

@app.route('/onas')
def index ():
    return render_template ("onas.html")

    @app.route('/registrace')
def index ():
    return render_template ("registrace.html")
    
    @app.route('/prihlaseni')
def index ():
    return render_template ("prihlaseni.html")



