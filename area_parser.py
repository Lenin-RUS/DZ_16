import requests
import pprint
domain='https://api.hh.ru/'
url='https://transparency.entsog.eu/api/v1/operationaldatas?pointDirection=RU-TSO-0001ITP-00184exit,UA-TSO-0001ITP-00184entry&from=2019-12-27&to=2020-01-26&indicator=Physical%20Flow&periodType=day&timezone=CET'
result=requests.get(url).json()

pprint.pprint(result)

