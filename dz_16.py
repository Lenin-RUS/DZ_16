from flask import Flask, render_template, request
from rest import  parser
from rest_orm import  parser_orm
app = Flask(__name__)

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
    #
    all_found_vac, all_skills = parser_orm(params)                    # <-------------- парсер с базой SQL вынесен в отдельный файл.
    print(all_skills)
    return render_template('result.html', all_found_vac=all_found_vac, skills=all_skills, **params)


if __name__ == "__main__":
    app.run(debug=True)
