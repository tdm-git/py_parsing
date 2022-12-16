# 2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis). Найти среди них любое,
# требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
# возьмите API вконтакте (https://vk.com/dev/first_guide). Сделайте запрос, чтобы получить список всех сообществ
# на которые вы подписаны.
import os
from  dotenv import load_dotenv
import requests
from pprint import pprint

load_dotenv('.env')
vk_token = os.getenv('VK_TOKEN')
user_id = os.getenv('USER_ID')
# print(vk_token)
params = vk_token + '&user_id=' + user_id + '&extended=1&count=10&v=5.131' # count - количество групп за запрос
url = 'https://api.vk.com/method/groups.get?' + params
#
res = requests.get(url=url)
pprint(res.json())
# print(res['response']['count'])  # общее количество групп
# for str in res['response']['items']:  # перебор и вывод id и наименований групп
#     print(str['id'],str['name'])
