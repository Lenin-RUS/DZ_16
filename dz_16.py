from flask import Flask, render_template, request
import requests, pprint

app = Flask(__name__)
domain='https://api.hh.ru/'
url=f'{domain}vacancies'

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/contact/")
def contact():
    my_data={
        'name':'Lenin',
        'mail':'S.lanin@gmail.com',
        'tel':'+7 916 99 371 22'
    }
    return render_template('contact.html', **my_data)

@app.route("/search_form/", methods=['GET'])
def search_form_get():
    if request.method=='POST':
        print('POST')
    return render_template('search_form.html')


@app.route('/search_form/', methods=['POST'])
def result():
    params={}
    params['text']=request.form['vac_text']
    params['employment']=request.form['schedule_query']
    params['education_level']=request.form['education_level_query']
    params['business_trip_readiness']=request.form['business_trip_readiness_query']
    params['area'] = request.form['area_query']

    result=requests.get(url, params = params).json()
    all_found_vac=result['found']
    all_pages=result['found']//100+1 if result['found']//100 <=20 else 20
    print('----------------------------------------------')
    print(f'по запросу: {params}, найдено {all_found_vac} вакансий')


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

    for i in all_skills:
        all_skills[i] = [all_skills[i], str(round(all_skills[i]/all_keys*100,2))+'%']

    print('----------------------------------------------')
    print(f'необходимые скилы для запроса {params}: ')
    pprint.pprint(all_skills)
    print('----------------------------------------------')

    return render_template('result.html', all_found_vac=all_found_vac, skills=all_skills, **params)


if __name__ == "__main__":
    app.run(debug=True)
