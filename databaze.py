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

def registrace_camp(camp_type_urban, camp_type_nature, camp_date_start, camp_date_finish, camp_price, camp_price_remark, camp_remark,
            camp_equipment, camp_address, camp_web, camp_name, camp_programm, camp_focus_classic, camp_focus_language, camp_focus_sport,
            camp_focus_art, camp_focus_christ, camp_focus_science, camp_focus_others, camp_CR, camp_international, camp_girl, camp_boy,
            camp_girl_boy, camp_mum_daughter, camp_dad_son, camp_parent_kid, camp_senior, camp_single, camp_handicapped, accommodation_cabin,
            accommodation_tent, accommodation_house, accommodation_other, age1, age2, age3, age4, age5, camp_capacity, stay_day, stay_weekend,
            stay_week, stay_more, stay_2weeks, region_Praha, region_jihocesky, region_jihomoravsky, region_karlovarsky, region_vysocina,
            region_kralovehradecky, region_liberecky, region_moravskoslezky, region_olomoucky, region_pardubicky,
            region_plzensky, region_stredocesky, region_ustecky, region_zlinsky):
#sql dotaz na import
    sql = """INSERT INTO camp (camp_type_urban, camp_type_nature, camp_date_start, camp_date_finish, camp_price, camp_price_remark, camp_remark,
            camp_equipment, camp_address, camp_web, camp_name, camp_programm, camp_focus_classic, camp_focus_language, camp_focus_sport,
            camp_focus_art, camp_focus_christ, camp_focus_science, camp_focus_others, camp_CR, camp_international, camp_girl, camp_boy,
            camp_girl_boy, camp_mum_daughter, camp_dad_son, camp_parent_kid, camp_senior, camp_single, camp_handicapped, accommodation_cabin,
            accommodation_tent, accommodation_house, accommodation_other, age1, age2, age3, age4, age5, camp_capacity, stay_day, stay_weekend,
            stay_week, stay_more, stay_2weeks, region_Praha, region_jihocesky, region_jihomoravsky, region_karlovarsky, region_vysocina,
            region_kralovehradecky, region_liberecky, region_moravskoslezky, region_olomoucky, region_pardubicky,
            region_plzensky, region_stredocesky, region_ustecky, region_zlinsky)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s%s, %s, %s, %s, %s, %s, %s, %s, %s, %s%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING camp_id;"""
    #pripojeni k databazi a zavolam import db vkladani tabora
    c_id = None
    try:
        cur = conn.cursor()
        cur.execute(sql, (camp_type_urban, camp_type_nature, camp_date_start, camp_date_finish, camp_price, camp_price_remark, camp_remark,
            camp_equipment, camp_address, camp_web, camp_name, camp_programm, camp_focus_classic, camp_focus_language, camp_focus_sport, camp_focus_art, camp_focus_christ, camp_focus_science, camp_focus_others, camp_CR, camp_international, camp_girl, camp_boy, camp_girl_boy, camp_mum_daughter, camp_dad_son, camp_parent_kid,                      
            camp_senior, camp_single, camp_handicapped, accommodation_cabin, accommodation_tent, accommodation_house,
            accommodation_other, age1, age2, age3, age4, age5, camp_capacity, stay_day, stay_weekend, stay_week, stay_more, stay_2weeks,
            region_Praha, region_jihocesky, region_jihomoravsky, region_karlovarsky, region_vysocina,
            region_kralovehradecky, region_liberecky, region_moravskoslezky, region_olomoucky, region_pardubicky,
            region_plzensky, region_stredocesky, region_ustecky, region_zlinsky))
        c_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return c_id

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

def tabulka_vypis():
    sql = """SELECT c.camp_id
                    , c.camp_name 
                    , c.camp_date_start
                    , c.camp_date_finish
                    , c.camp_programm
                    , c.camp_focus_classic
                    , c.camp_focus_language
                    , c.camp_focus_sport
                    , c.camp_focus_art
                    , c.camp_focus_christ
                    , c.camp_focus_science
                    , c.camp_focus_others
                    , c.camp_price
                    , c.region_Praha
                    , c.region_jihocesky
                    , c.region_jihomoravsky
                    , c.region_karlovarsky
                    , c.region_vysocina
                    , c.region_kralovehradecky
                    , c.region_liberecky
                    , c.region_moravskoslezky
                    , c.region_olomoucky
                    , c.region_pardubicky
                    , c.region_plzensky
                    , c.region_stredocesky
                    , c.region_ustecky
                    , c.region_zlinsky
                    , org.organizer_name
                    FROM camp as c
                    LEFT JOIN  databaze_org AS org ON c.camp_id = org.camp_id
                    ORDER BY c.camp_date_start DESC"""
    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute(sql)
        camp_table = cur.fetchall()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
           conn.close()
    return camp_table

def registrace_job (typ_nabidka, typ_poptavka, date_start, date_finish, text):
    conn = db.get_db()
    #sql dotaz na import
    sql = """INSERT INTO JOB (typ_nabidka, typ_poptavka, date_start, date_finish, text)
            VALUES(%s, %s, %s, %s, %s) RETURNING job_id;"""
    #pripojeni k databazi a zavolam import db vkladani job(prace)
    j_id = None
    try:
        cur = conn.cursor()
        cur.execute(sql, (typ_nabidka, typ_poptavka, date_start, date_finish, text))
        j_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return j_id

def tabulka_vypis_job():
    sql = """SELECT job_id
                    , typ_nabidka
                    , typ_poptavka
                    , date_start
                    , date_finish
                    , text
                    FROM JOB
                    """
    conn = get_db()
    try:
        cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        cur.execute(sql)
        job_table = cur.fetchall()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
           conn.close()
    return job_table
    