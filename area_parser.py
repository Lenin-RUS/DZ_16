import requests
domain='https://api.hh.ru/'
url=f'{domain}areas'
result=requests.get(url).json()

print(result[0]['areas'][0]['areas'][0]['areas'])

