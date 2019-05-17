import db

def registrace_org(organizer_ico, organizer_dic, organizer_name, organizer_address, organizer_street_num,
    organizer_psc, organizer_city, organizer_phone, organizer_web, organizer_contact_person, organizer_description,
    organizer_username, organizer_password, organizer_password_confirmed, organizer_email, organizer_gdpr):

#pripojeni k databazi a zavolam import db
    conn = db.get_db()
#sql dotaz na import registrace organizatora
    sql = "INSERT INTO databaze_org VALUES " + ' '.join([organizer_ico, organizer_dic, organizer_name, organizer_address, organizer_street_num,
        organizer_psc, organizer_city, organizer_phone, organizer_web, organizer_contact_person, organizer_description,
        organizer_username, organizer_password, organizer_password_confirmed, organizer_email, organizer_gdpr])
    print(sql)
    cur = conn.cursor()
#vykonej ten dotaz
    cur.execute(sql)
    

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


    