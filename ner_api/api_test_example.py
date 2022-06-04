import requests
import json


URL = "http://0.0.0.0:30005/ner"
datas = {'text':
        ['김민수 삼성전자 tom 서울특별시 박민수 영등포구 123-45 010-1234-5687', '경기도 수원시 장안구 010-5456-5654 이지연 LG전자']
}

response = requests.post(URL, data=json.dumps(datas)).json()

print(response)
# result
## [{'PER': [' 김민수', ' 박민수'], 'ORG': [' 삼성전자']}, {'PER': [' 이지연'], 'ORG': [' LG전자']}]