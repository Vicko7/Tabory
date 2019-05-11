from flask import Flask, render_template, request, g
import db

app= Flask("Tabory")

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        # Bezpečně ukončí spojení s naší databází
        g.db.close()

@app.route('/')
def index():
    return render_template ("index.html")

@app.route('/tabory', methods=["GET"])
def tabory():
    return render_template ("tabory.html")

@app.route('/tabory', methods=["POST"])
def tabory_hledani():
    print(request.form)

    kraje_sql = ["1=1"]
    if requests.form.get("kraj_karlovarsky") == 1:
        kraje_sql.append("kraj_karlovarsky = 1")
    if requests.form.get("kraj_ustecky") == 1:
        kraje_sql.append("kraj_ustecky = 1")
    kraje_sql_where = " OR ".join(kraje_sql)

    conn = db.get_db()
    sql = """SELECT * FROM camp WHERE  (""" + kraje_sql_where + ")"
    print(sql)
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    print(data)
    return render_template ("tabory_vysledky.html", tabory_z_db = data)

@app.route('/tabor/<id_taboru>')
def tabor_detail(id_taboru):

    conn = db.get_db()
    sql = """SELECT * FROM camp WHERE camp_id = %s"""
    cur = conn.cursor()
    cur.execute(sql, (id_taboru, ))
    data = cur.fetchall()

    return render_template("tabor_detail.html", tabor_z_db = data)

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



