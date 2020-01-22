import requests
import json
import pprint

domain='https://api.hh.ru/'
url=f'{domain}vacancies'
params={}

text_query=input('Введите текст вакансии: ')
params['text'] = text_query

# Блок формирования запроса
schedule_query=int(input('Введите график работы (1-Полная занятость, 2-Частичная занятость, 3-Стажировка): '))
if schedule_query==1: params['employment'] = 'full'
if schedule_query==2: params['employment'] = 'part'
if schedule_query==3: params['employment'] = 'probation'

education_level_query=int(input('Введите образование (1-Среднее, 2-Высшее, 3-Магистр): '))
if education_level_query==1: params['education_level'] = 'secondary'
if education_level_query==2: params['education_level'] = 'higher'
if education_level_query==3: params['education_level'] = 'master'

business_trip_readiness_query=int(input('Командировки (1-готов, 2-редкие, 3-не готов): '))
if business_trip_readiness_query==1: params['business_trip_readiness'] = 'ready'
if business_trip_readiness_query==2: params['business_trip_readiness'] = 'sometimes'
if business_trip_readiness_query==3: params['business_trip_readiness'] = 'never'

area_query=int(input('Регион (113-Россия, 1-Москва, 1890-Липецкая область, 43-Калуга): '))
params['area'] = str(area_query)
# Конец блока формирования запроса

result=requests.get(url, params = params).json()
all_found_vac=result['found']
all_pages=result['found']//100+1 if result['found']//100 <=20 else 20
print('----------------------------------------------')
print(f'по запросу: {params}, найдено {all_found_vac} вакансий')

# Подсчет скилов
all_skills={}
for i in range(all_pages):
    # print(f'страница {i}')
    params['page']=i
    result=requests.get(url, params = params).json()
    for j in result['items']:
        rez_tmp=requests.get(j['url']).json()
        # print(rez_tmp)
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
print(f'необходимые скилы для запроса {text_query}: ')
pprint.pprint(all_skills)
print('----------------------------------------------')
if input('Сохранить файл (y/n)? ') !='n':
    file_name=str(input('Имя файла: '))+'.json'
    with open(file_name, 'w') as f:
        json.dump({'params':params}, f)
        json.dump({'count':all_found_vac}, f)
        json.dump({'skills':all_skills}, f)