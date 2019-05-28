from flask import Flask, render_template, request, g
import db
import functools
import databaze
import logging
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

@app.route('/tabory', methods=["GET"])
def tabory():
    camp_table = databaze.tabulka_vypis()
    return render_template ("tabory.html",
    camp_table=camp_table
    )

@app.route('/tabory', methods=["POST"])
def tabory_hledani():
    print(request.form)

    podminky = []
    kraje_sql = ["1=1"]
    kraje = request.form.getlist("kraje")
    if "všechny" not in kraje:
        if "region_Praha" in kraje:
            kraje_sql.append("region_Praha = TRUE")
        if "region_jihocesky" in kraje:
            kraje_sql.append("region_jihocesky = TRUE")
        if "region_jihomoravsky" in kraje:
            kraje_sql.append("region_jihomoravsky = TRUE")
        if "region_karlovarsky" in kraje:
            kraje_sql.append("region_karlovarsky = TRUE")
        if "region_vysocina" in kraje:
            kraje_sql.append("region_vysocina = TRUE")
        if "region_kralovehradecky" in kraje:
            kraje_sql.append("region_kralovehradecky = TRUE")
        if "region_moravskoslezky" in kraje:
            kraje_sql.append("region_moravskoslezky = TRUE")
        if "region_olomoucky" in kraje:
            kraje_sql.append("region_olomoucky = TRUE")
        if "region_pardubicky" in kraje:
            kraje_sql.append("region_pardubicky = TRUE")
        if "region_plzensky" in kraje:
            kraje_sql.append("region_plzensky = TRUE")
        if "region_stredocesky" in kraje:
            kraje_sql.append("region_stredocesky = TRUE")
        if "region_ustecky" in kraje:
            kraje_sql.append("region_ustecky = TRUE")
        if "region_zlinsky" in kraje:
            kraje_sql.append("region_zlinsky = TRUE")
        podminky.append(" OR ".join(kraje_sql))

    koho_sql = ["1=1"]
    if request.form.get("camp_girl") == "1":
        koho_sql.append("camp_girl = TRUE")
    if request.form.get("camp_boy") == "1":
        koho_sql.append("camp_boy = TRUE")
    if request.form.get("camp_girl_boy") == "1":
        koho_sql.append("camp_girl_boy = TRUE")
    if request.form.get("camp_mum_daughter") == "1":
        koho_sql.append("camp_mum_daughter = TRUE")
    if request.form.get("camp_dad_son") == "1":
        koho_sql.append("camp_dad_son = TRUE")
    if request.form.get("camp_parent_kid") == "1":
        koho_sql.append("camp_parent_kid = TRUE")
    if request.form.get("camp_senior") == "1":
        koho_sql.append("camp_senior = TRUE")
    if request.form.get("camp_single") == "1":
        koho_sql.append("camp_single = TRUE")
    if request.form.get("camp_handicapped") == "1":
        koho_sql.append("camp_handicapped = TRUE")
    podminky.append(" OR ".join(koho_sql))

    zajmy_sql = ["1=1"]
    if request.form.get("camp_focus_classic") == "1":
        zajmy_sql.append("camp_focus_classic = TRUE")
    if request.form.get("camp_focus_language") == "1":
        zajmy_sql.append("camp_focus_language = TRUE")
    if request.form.get("camp_focus_sport") == "1":
        zajmy_sql.append("camp_focus_sport = TRUE")
    if request.form.get("camp_focus_art") == "1":
       zajmy_sql.append("camp_focus_art = TRUE")
    if request.form.get("camp_focus_christ") == "1":
        zajmy_sql.append("camp_focus_christ = TRUE")
    if request.form.get("camp_focus_science") == "1":
        zajmy_sql.append("camp_focus_science = TRUE")
    if request.form.get("camp_focus_others") == "1":
        zajmy_sql.append("camp_focus_others = TRUE")
    podminky.append(" OR ".join(zajmy_sql))

    misto_sql = ["1=1"]
    if request.form.get("camp_international") == "1":
        misto_sql.append("camp_international = TRUE")
    if request.form.get("camp_CR") == "1":
        misto_sql.append("camp_CR = TRUE")
    podminky.append(" OR ".join(misto_sql))

    typ_sql = ["1=1"]
    if request.form.get("camp_type_urban") == "1":
        typ_sql.append("camp_type_urban = TRUE")
    if request.form.get("camp_type_nature") == "1":
        typ_sql.append("camp_type_nature = TRUE")
    podminky.append(" OR ".join(typ_sql))
    #typ_sql_where = " OR ".join(typ_sql)

    vek_sql = ["1=1"]
    vek = request.form.getlist("vek")
    if "Nerozhoduje" not in vek:
        if "age1" in vek:
            vek_sql.append("age1 = 1")
        if "age2" in vek:
            vek_sql.append("age2 = 1")
        if "age3" in vek:
            vek_sql.append("age3 = 1")
        if "age4" in vek:
            vek_sql.append("age4 = 1")
        if "age5" in vek:
            vek_sql.append("age5 = 1")
    podminky.append(" OR ".join(vek_sql))
    
    delka_sql = ["1=1"]
    delka = request.form.getlist("delka_pobytu")
    if "nerozhoduje" not in delka:
        if "stay_day" in delka:
            delka_sql.append("stay_day = TRUE")
        if "stay_weekend" in delka:
            delka_sql.append("stay_weekend = TRUE")
        if "stay_week" in delka:
            delka_sql.append("stay_week = TRUE")
        if "stay_more" in delka:
            delka_sql.append("stay_more = TRUE")
        if "stay_2weeks" in delka:
            delka_sql.append("stay_2weeks = TRUE")
    podminky.append(" OR ".join(delka_sql))
   

    cena = request.form.get("camp_price")
    if cena == "price_to":
        cena_sql = "camp_price <= 2000"
    else:
        cena_sql = "camp_price > 2000"
    podminky.append(cena_sql)

    
    termin_start = request.form.get("date_from")
    termin_finish = request.form.get("date_to")
    termin_sql = ["1=1"]
    if termin_start:
        termin_sql.append("camp_date_start >= '" + termin_start + "'")
    if termin_finish:
        termin_sql.append("camp_date_finish <= '" + termin_finish + "'")
    termin_sql_where = " AND ".join(termin_sql)
    podminky.append(termin_sql_where)


    where = "(" + ") AND (".join(podminky) + ")"

    sql = """SELECT * FROM camp WHERE  (""" + where + ")"
    print(sql)
    
    conn = db.get_db()
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

@app.route('/prace', methods=("GET", "POST"))
def vloz_praci():
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

@app.route('/registrace_org', methods=["GET"])
def registrace_org():
    return render_template("registrace_org.html")
    

@app.route('/registrace_org', methods=["POST"]) 
def registrace_org_post():
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
        databaze.registrace_org(organizer_ico, organizer_dic, organizer_name, organizer_address, organizer_street_num,
        organizer_psc, organizer_city, organizer_phone, organizer_web, organizer_contact_person, organizer_description,
        organizer_username, organizer_password, organizer_password_confirmed, organizer_email)
    return render_template("success.html", organizer_z_db = data)

@app.route('/registrace_uz', methods=["GET"])
def registrace_uz():
    return render_template("registrace_uz.html")

@app.route('/registrace_uz', methods=["POST"])
def registrace_uz_post():
    if request.method == 'POST':
        jmeno = request.form['jmeno']
        prijmeni = request.form['prijmeni']
        email = request.form['email']
        password = request.form['password']
        password_confirmed = request.form['password_confirmed']
        databaze.registrace_uz(jmeno, prijmeni, email, password, password_confirmed)
    return render_template("success.html")


@app.route('/success')
def success():
    return render_template("success.html")


if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

