import requests
import sqlite3

def parser(params):
    conn = sqlite3.connect('dz_17.sqlite')
    cursor = conn.cursor()
    print(params)
    domain='https://api.hh.ru/'
    url=f'{domain}vacancies'

    result=requests.get(url, params = params).json()
    all_found_vac=result['found']
    all_pages=result['found']//100+1 if result['found']//100 <=20 else 20

    # Подсчет скилов
    all_skills={}
    for i in range(all_pages):
        params['page']=i
        result=requests.get(url, params = params).json()
        for j in result['items']:
            rez_tmp=requests.get(j['url']).json()
            for i in rez_tmp['key_skills']:
                if i['name'] in all_skills:
                    all_skills[i['name']]+=1
                else:
                    all_skills.setdefault(i['name'], 1)

    all_keys=0
    for i in all_skills:
        all_keys += all_skills[i]



    cursor.execute('SELECT * from schedule_query where schedule = ?', (params['employment'],))
    if not cursor.fetchall():
        cursor.execute("insert into schedule_query (schedule) VALUES (?)", (params['employment'],))
    schedule=cursor.execute('SELECT shed_id from schedule_query where schedule=?',(params['employment'],)).fetchall()[0][0]   #<---- Хрень какая-то.....

    cursor.execute('SELECT * from education where education_level = ?', (params['education_level'],))
    if not cursor.fetchall():
        cursor.execute("insert into education (education_level) VALUES (?)", (params['education_level'],))
    education_level=cursor.execute('SELECT educ_id from education where education_level=?',(params['education_level'],)).fetchall()[0][0]

    cursor.execute('SELECT * from business_trip_readiness where business_trip_readiness = ?', (params['business_trip_readiness'],))
    if not cursor.fetchall():
        cursor.execute("insert into business_trip_readiness (business_trip_readiness) VALUES (?)", (params['business_trip_readiness'],))
    business=cursor.execute('SELECT trip_readiness_id from business_trip_readiness where business_trip_readiness=?',(params['business_trip_readiness'],)).fetchall()[0][0]

    cursor.execute('SELECT * from area where name = ?', (params['area'],))    #<---------- пока сделано криво, имя региона - просто номер
    if not cursor.fetchall():
        cursor.execute("insert into area (name) VALUES (?)", (params['area'],))
    area=cursor.execute('SELECT area_id from area where name=?',(params['area'],)).fetchall()[0][0]

    cursor.execute("insert into main_table (shedule_id, education_id, trip_id, area_id, querry_text, num_of_vac) VALUES (?,?,?,?,?,?)", (schedule,education_level, business, area,params['text'],all_keys,  ))

    mt_last_id=cursor.execute("SELECT max(querry_id) FROM main_table").fetchall()[0][0]
    for i in all_skills:
        cursor.execute('SELECT * from skills where skill_name = ?', (i,))
        if not cursor.fetchall():
            cursor.execute("insert into skills (skill_name) VALUES (?)", (i,))
        skill_id=cursor.execute('SELECT skill_id from skills where skill_name=?',(i,)).fetchall()[0][0]
        skill_num=all_skills[i]
        skill_percent=round(all_skills[i]/all_keys*100,2)
        all_skills[i] = [all_skills[i], str(round(all_skills[i]/all_keys*100,2))+'%']
        cursor.execute("insert into skill_req (skill_id, request_id, skill_num, skill_percent) VALUES (?,?,?,?)", (skill_id,mt_last_id, skill_num, skill_percent,))

    # Запрос к базе
    cursor.execute("select sk.skill_name, sr.skill_num, sr.skill_percent from skill_req sr, skills sk where sr.skill_id=sk.skill_id and sr.request_id=?", (mt_last_id,))

    all_skills_from_sql=cursor.fetchall()
    conn.commit()
    return all_found_vac, all_skills_from_sql