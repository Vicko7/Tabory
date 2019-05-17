from flask import Flask, render_template, request, g
import db
import functools
import databaze
#import main
#import gunicorn
app = Flask("WEB_TABORY")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



# Zaregistruje funkci close_db() do naší aplikace jako funkci, která se má spustit,
# když se ukončuje naše aplikace

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        # Bezpečně ukončí spojení s naší databází
        g.db.close()

@app.route('/')
def index():
    return render_template ("index.html")

@app.route('/tabory', methods=['GET'])
def tabory():
    return render_template ("tabory.html")

@app.route('/tabory', methods=['POST'])
def tabory_hledani():
    print(request.form)

    kraje_sql = ["1=1"]
    if requests.form.get("region_Praha") == 1:
        kraje_sql.append("region_Praha = 1")
    if requests.form.get("region_jihocesky") == 1:
        kraje_sql.append("region_jihocesky = 1")
    if requests.form.get("region_jihomoravsky") == 1:
        kraje_sql.append("region_jihomoravsky = 1")
    if requests.form.get("region_karlovarsky") == 1:
        kraje_sql.append("region_karlovarsky = 1")
    if requests.form.get("region_vysocina") == 1:
        kraje_sql.append("region_vysocina = 1")
    if requests.form.get("region_kralovehradecky") == 1:
        kraje_sql.append("region_kralovehradecky = 1")
    if requests.form.get("region_moravskoslezky") == 1:
        kraje_sql.append("region_moravskoslezky = 1")
    if requests.form.get("region_olomoucky") == 1:
        kraje_sql.append("region_olomoucky = 1")
    if requests.form.get("region_pardubicky") == 1:
        kraje_sql.append("region_pardubicky = 1")
    if requests.form.get("region_plzensky") == 1:
        kraje_sql.append("region_plzensky = 1")
    if requests.form.get("region_stredocesky") == 1:
        kraje_sql.append("region_stredocesky = 1")
    if requests.form.get("region_ustecky") == 1:
        kraje_sql.append("region_ustecky = 1")
    if requests.form.get("region_zlinsky") == 1:
        kraje_sql.append("region_zlinsky = 1")
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

@app.route('/prace', methods=('GET', 'POST'))
def vloz_praci ():
    if request.method == 'POST':
        datum = request.form['datum']
        typ = request.form['typ']
        text = request.form['text']
        databaze.registrace_prace(datum, typ, text)
    return render_template("success.html")

@app.route('/onas')
def onas():
    return render_template ("onas.html")

@app.route('/mapa')
def mapa():
    return render_template ("mapa.html")

    
@app.route('/prihlaseni')
def prihlaseni():
    return render_template ("prihlaseni.html")

@app.route('/registrace_org', methods=['GET'])
def registrace_org ():
    return render_template("registrace_org.html")
    

@app.route('/registrace_org', methods=['POST']) 
def registrace_org():
    if request.method == 'POST':
        organizer_ico = request.form['organizer_ico']
        organizer_dic = request.form['organizer_dic']
        organizer_name = request.form['organizer_name']
        organizer_address = request.form['organizer_address']
        organizer_street_num = request.form['organizer_street_num']
        organizer_psc = request.form['organizer_psc']
        organizer_city = request.form['organizer_city']
        organizer_phone = request.form['organizer_phone']
        organizer_web = request.form['organizer_web']
        organizer_contact_person = request.form['organizer_contact_person']
        organizer_description = request.form['organizer_description']
        organizer_username = request.form['organizer_username']
        organizer_password = request.form['organizer_password']
        organizer_password_confirmed = request.form['organizer_password_confirmed']
        organizer_email = request.form['organizer_email']
        organizer_gdpr = request.form['organizer_gdpr']
        databaze.registrace_org(organizer_ico, organizer_dic, organizer_name, organizer_address, organizer_street_num,
        organizer_psc, organizer_city, organizer_phone, organizer_web, organizer_contact_person, organizer_description,
        organizer_username, organizer_password, organizer_password_confirmed, organizer_email, organizer_gdpr)
    return render_template('/success.html')

@app.route('/registrace_uz', methods=['GET'])
def registrace_uz ():
    return render_template("registrace_uz.html")

@app.route('/registrace_uz', methods=('POST'))
def registrace_uz ():
    if request.method == 'POST':
        jmeno = request.form['jmeno']
        prijmeni = request.form['prijmeni']
        email = request.form['email']
        password = request.form['password']
        password_confirmed = request.form['password_confirmed']
        databaze.registrace_uz(jmeno, prijmeni, email, password, password_confirmed)
    return render_template("success.html")


@app.route('/success')
def success ():
    return render_template("success.html")

