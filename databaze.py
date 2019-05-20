import db
import psycopg2
import psycopg2.extras
import datetime
import os
import hashlib, binascii
from flask import g, flash
from hashlib import sha512
from flask_login import UserMixin
from functools import lru_cache

def get_db():
    """ Spojeni s dtb. """
    if not hasattr(g, 'db') or g.db.closed == 1:
		# https://devcenter.heroku.com/articles/heroku-postgresql#connecting-in-python
        database_url = os.environ["DATABASE_URL"]
    #database_url = os.environ["DATABASE_URL"]
        con = psycopg2.connect(database_url, sslmode='require')
        g.db = con
    return g.db

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
 
def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def registrace_org(organizer_ico, organizer_dic, organizer_name, organizer_address, organizer_street_num,
    organizer_psc, organizer_city, organizer_phone, organizer_web, organizer_contact_person, organizer_description,
    organizer_username, organizer_password, organizer_password_confirmed, organizer_email):

    """ vlozi noveho oraganizatora do databaze """
    sql = """INSERT INTO public.databaze_org
        (organizer_ico, organizer_dic, organizer_name, organizer_address, organizer_street_num,
        organizer_psc, organizer_city, organizer_phone, organizer_web, organizer_contact_person, organizer_description,
        organizer_username, organizer_password, organizer_password_confirmed, organizer_email)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING organizer_id;"""
    conn = get_db()
    org_id = None
    #password = hash_password(password)     
    try:
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (organizer_ico, organizer_dic, organizer_name, organizer_address, organizer_street_num,
        organizer_psc, organizer_city, organizer_phone, organizer_web, organizer_contact_person, organizer_description,
        organizer_username, organizer_password, organizer_password_confirmed, organizer_email))
        # get the generated id back
        org_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        flash('Vaše emailová adresa už je v naší databázi.')
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return org_id

        

def registrace_uz(jmeno, prijmeni, email, password, password_confirmed):
    conn = db.get_db()
#sql dotaz na import registrace uzivatele
    sql = "INSERT INTO databaze_uz VALUES"+ ' '.join([jmeno, prijmeni, email, password, password_confirmed])
    print(sql)
    cur = conn.cursor()
#vykonej ten dotaz
    cur.execute(sql)

def registrace_camp(type_urban, type_nature, date, note, price, price_note, equipment, web_organizer,
    web_camp, camp_name, focus_classic, focus_language, focus_sport, focus_art, focus_christ, focus_science, focus_others,
    country_CR, country_int, who_girl, who_boy, who_girl_boy, who_mum_daughter, who_dad_son,who_parent_kid,                      
    who_senior, who_single, who_handicapped, accommodation_cabin, accommodation_tent, accommodation_house,
    accommodation_other, age_1, age_2, age_3, age_4, age_5, stay_day, stay_weekend, stay_week, stay_more, 
    stay_other, region_Praha, region_Jihocesky, region_Jihomoravsky, region_Karlovarsky, region_Vysocina,
    region_Kralovehradecky, region_Liberecky, region_Moravskoslezky, region_Olomoucky, region_Pardubicky,
    region_Plzensky, region_Stredocesky, region_Ustecky, region_Zlinsky):

#pripojeni k databazi a zavolam import db vkladani tabora
    conn = db.get_db()
#sql dotaz na import
    sql = "INSERT INTO databaze_camp VALUES " + ' '.join([type_urban, type_nature, date, note, price, price_note, equipment, web_organizer,
            web_camp, camp_name, focus_classic, focus_language, focus_sport, focus_art, focus_christ, focus_science, focus_others,
            country_CR, country_int, who_girl, who_boy, who_girl_boy, who_mum_daughter, who_dad_son,who_parent_kid,                      
            who_senior, who_single, who_handicapped, accommodation_cabin, accommodation_tent, accommodation_house,
            ccommodation_other, age_1, age_2, age_3, age_4, age_5, stay_day, stay_weekend, stay_week, stay_more, 
            stay_other, region_Praha, region_Jihocesky, region_Jihomoravsky, region_Karlovarsky, region_Vysocina,
            region_Kralovehradecky, region_Liberecky, region_Moravskoslezky, region_Olomoucky, region_Pardubicky,
            region_Plzensky, region_Stredocesky, region_Ustecky, region_Zlinsky])
    print(sql)
    cur = conn.cursor()
#vykonej ten dotaz
    cur.execute(sql)


def registrace_praha(Praha1, Praha2, Praha3, Praha4, Praha5, Praha6, Praha7, Praha8, Praha9, Praha10, Praha11,
    Praha12, Praha13, Praha14, Praha15, Praha16, Praha17, Praha18, Praha19, Praha20, Praha21, Praha22):

#pripojeni k databazi a zavolam import db vkladani tabora
    conn = db.get_db()
#sql dotaz na import
    sql = "INSERT INTO databaze_praha VALUES " + ' '.join([Praha1, Praha2, Praha3, Praha4, Praha5, Praha6, Praha7, Praha8, Praha9, Praha10, Praha11,
        Praha12, Praha13, Praha14, Praha15, Praha16, Praha17, Praha18, Praha19, Praha20, Praha21, Praha22])
    print(sql)
    cur = conn.cursor()
#vykonej ten dotaz
    cur.execute(sql)


    