# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.
import requests
import json
from pprint import pprint

user_name = 'tdm-git'
headers = {'Accept': 'application/vnd.github+json',
           'X-GitHub-Api-Version': '2022-11-28'}
url = 'https://api.github.com/users/' + user_name + '/repos'
response = requests.get(url=url, headers=headers)
# выводим
pprint(response.json())
# сохраняем в файл
with open(user_name + "_repo.json", "w") as f:
    json.dump(response.json(), f)
