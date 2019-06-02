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
    
@app.route('/tabory', methods=['POST'])
def tabory_hledani():
    print(request.form)

    podminky = []
    kraje_sql = []
    kraje = request.form.getlist("kraje")
    if "všechny" not in kraje:
        for kraj in kraje:
            if kraj == "region_Praha":
                kraje_sql.append("region_praha IS NOT NULL")
            elif kraj.startswith("region_"):
                kraje_sql.append(kraj + " = TRUE")
            else: # cislo casti prahy
                kraje_sql.append("region_praha = " + kraj)

        podminky.append(" OR ".join(kraje_sql))

    koho_sql = []
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
    if koho_sql:
        podminky.append(" OR ".join(koho_sql))

    zajmy_sql = []
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
    if zajmy_sql:
        podminky.append(" OR ".join(zajmy_sql))

    misto_sql = []
    if request.form.get("camp_international") == "1":
        misto_sql.append("camp_international = TRUE")
    if request.form.get("camp_CR") == "1":
        misto_sql.append("camp_CR = TRUE")
    if misto_sql:
        podminky.append(" OR ".join(misto_sql))

    typ_sql = []
    if request.form.get("camp_type_urban") == "1":
        typ_sql.append("camp_type_urban = TRUE")
    if request.form.get("camp_type_nature") == "1":
        typ_sql.append("camp_type_nature = TRUE")
    if typ_sql:
        podminky.append(" OR ".join(typ_sql))
  

    vek_sql = []
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
    
    delka_sql = []
    delka = request.form.getlist("delka_pobytu")
    if "Nerozhoduje" not in delka:
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
   

    cena = request.form.get("cena")
    if cena != "Nerozhoduje":
        if cena == "price_to":
            cena_sql = "camp_price <= 2000"
        else:
            cena_sql = "camp_price > 2000"
        podminky.append(cena_sql)

    
    termin_start = request.form.get("date_from")
    termin_finish = request.form.get("date_to")
    termin_sql = []
    if termin_start:
        termin_sql.append("camp_date_start >= '" + termin_start + "'")
    if termin_finish:
        termin_sql.append("camp_date_finish <= '" + termin_finish + "'")
    if termin_sql:
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


@app.route('/tabory', methods=["GET"])
def tabory():
    return render_template ("tabory.html")


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

@app.route('/prace', methods=["GET", "POST"])
def vloz_praci():
    if request.method == 'POST':
        
        typN = request.form['typ_nabidka']
        typP = request.form['typ_poptavka']
        text = request.form['text']
        dateStart = request.form['date_start']
        dateFinish = request.form['date_finish']
        databaze.registrace_prace(typ_nabidka, typ_poptavka, text, date_start, date_finish )
    return render_template("success.html")

    
@app.route('/onas')
def onas():
    return render_template ("onas.html")

@app.route('/mapa')
def mapa():
    return render_template ("mapa.html")

@app.route('/zkouska_mapa')
def zkouska_mapa():
    return render_template ("zkouska_mapa.html")

    
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

@app.route('/registrace_camp' , methods = ["GET"])
def registrace_camp():
    return render_template("registrace_camp.html")

@app.route('/registrace_camp' , methods = ["POST"])
def registrace_camp_post():
    if request.method == 'POST':
        nazev= request.form['camp_name']
        web= request.form['camp_web']
        camp_address= request.form['camp_address']
        camp_girl= request.form['camp_girl']
        camp_boy= request.form['camp_boy']
        camp_girl_boy= request.form['camp_girl_boy']
        camp_mum_daughter= request.form['camp_mum_daughter']
        camp_dad_son= request.form['camp_dad_son']
        camp_parent_kid= request.form['camp_parent_kid']
        camp_senior= request.form['camp_senior']
        camp_single= request.form['camp_single']
        camp_handicapped= request.form['camp_handicapped']
        camp_focus_language= request.form['camp_focus_language']
        camp_focus_classic= request.form['camp_focus_classic']
        camp_focus_sport= request.form['camp_focus_sport']
        camp_focus_art= request.form['camp_focus_art']
        camp_focus_christ= request.form['camp_focus_christ']
        camp_focus_science= request.form['camp_focus_science']
        camp_focus_others= request.form['camp_focus_others']
        camp_type_urban= request.form['camp_type_urban']
        camp_type_nature= request.form['camp_type_nature']
        camp_CR= request.form['camp_CR']
        camp_international= request.form['camp_international']
        accommodation_cabin= request.form['accommodation_cabin']
        accommodation_camp= request.form['accommodation_camp']
        accommodation_house= request.form['accommodation_house']
        accommodation_other= request.form['accommodation_other']
        age1= request.form['age1']
        age2= request.form['age2']
        age3= request.form['age3']
        age4= request.form['age4']
        age5= request.form['age5']
        stay_day= request.form['stay_day']
        stay_weekend= request.form['stay_weekend']
        stay_week= request.form['stay_week']
        stay_more= request.form['stay_more']
        stay_2weeks= request.form['stay_2weeks']
        region_Praha= request.form['region_Praha']
        region_jihoceskya= request.form['region_jihocesky']
        region_jihomoravsky= request.form['region_jihomoravsky']
        region_karlovarsky= request.form['region_karlovarsky']
        region_vysocina= request.form['region_vysocina']
        region_kralovehradecky= request.form['region_kralovehradecky']
        region_moravskoslezky= request.form['region_moravskoslezky']
        region_olomoucky= request.form['region_olomouckyy']
        region_pardubicky= request.form['region_pardubicky']
        region_plzensky= request.form['region_plzensky']
        region_ustecky= request.form['region_ustecky']
        region_zlinsky= request.form['region_zlinsky']
        date_start= request.form['date_start']
        date_finish= request.form['date_finish']
        camp_price= request.form['camp_price']
        databaze.registrace_uz(nazev, web, camp_address, camp_girl, camp_boy, camp_girl_boy, camp_mum_daughter,
camp_dad_son, camp_parent_kid, camp_senior, camp_single, camp_handicapped, camp_focus_language, camp_focus_classic, camp_focus_sport, camp_focus_art, camp_focus_christ, camp_focus_science, camp_focus_others, camp_type_urban, camp_type_nature,
camp_CR, camp_international, accommodation_cabin, accommodation_camp, accommodation_house, accommodation_other, age1,
age2, age3, age4, age5, stay_day, stay_weekend, stay_week, stay_more, stay_2weeks, region_Praha, region_jihocesky, region_jihomoravsky,
region_karlovarsky, region_vysocina, region_kralovehradecky, region_moravskoslezky, region_olomoucky, region_pardubicky, region_plzensky.
region_ustecky, region_zlinsky, date_start, date_finish, camp_price)
    return render_template("success.html")

   

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

