import db

def registrace_org(organizer_ico, organizer_dic, organizer_name, organizer_address, organizer_street_num,
        organizer_psc, organizer_city, organizer_phone, organizer_web, organizer_contact_person, organizer_description,
        organizer_username, organizer_password, organizer_password_confirmed, organizer_email, organizer_gdpr):

#pripojeni k databazi a zavolam import db
    conn = db.get_db()
#sql dotaz na import
    sql = "INSERT INTO databaze_org VALUES " + ' '.join([organizer_ico, organizer_dic, organizer_name, organizer_address, organizer_street_num,
        organizer_psc, organizer_city, organizer_phone, organizer_web, organizer_contact_person, organizer_description,
        organizer_username, organizer_password, organizer_password_confirmed, organizer_email, organizer_gdpr])
    print(sql)
    cur = conn.cursor()
#vykonej ten dotaz
    cur.execute(sql)
    

def registrace_uz(jmeno, prijmeni, email, password, password_confirmed):
    conn = db.get_db()
#sql dotaz na import
    sql = "INSERT INTO databaze_uz VALUES"+ ' '.join([jmeno, prijmeni, email, password, password_confirmed])
    print(sql)
    cur = conn.cursor()
#vykonej ten dotaz
    cur.execute(sql)