# -*- coding: utf-8 -*-
# ----------------------------
# @File    : es_insert.py
# @Date    : 2021-03-24
# @Author  : jf.l
# ----------------------------


from faker import Faker
import requests, json

fk = Faker('zh_cn')
index = 'book'
type = 'novel'
url = 'http://localhost:9200/{index}/{type}/{id}'

headers = {'Content-Type': 'application/json'}

data = lambda: {
    "user": fk.name(),
    "title": fk.job(),
    "desc": fk.text()
}

for i in range(1, 200):
    res = requests.put(url.format(index=index, type=type, id=i), data=json.dumps(data()), headers=headers)
    print(res.status_code, res.text)
