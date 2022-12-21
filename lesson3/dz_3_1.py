# Собрать информацию о вакансиях на вводимую должность с сайтов hh.ru и/или Superjob и/или работа.ру.
# Приложение должно анализировать несколько страниц сайта. Получившийся список должен содержать в себе
# минимум:
# 1. Наименование вакансии.
# 2. Предлагаемую зарплату (дополнительно: разносим в три поля: минимальная и максимальная и валюта, цифры
# преобразуем к цифрам).
# 3. Ссылку на саму вакансию.
# 4. Сайт, откуда собрана вакансия.
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение). Структурадолжна быть
# одинаковая для вакансий с всех сайтов. Общий результат можно вывести с помощью dataFrame через pandas, cохранить в json,
# либо csv.
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
from time import sleep
import json


result_dict = {}
seek_vacancy = 'Python'
start_page = 0
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'}
# url = 'https://ekaterinburg.hh.ru/search/vacancy?text=Python&from=suggest_post&area=3'
url = 'https://ekaterinburg.hh.ru/search/vacancy?text=Python&from=suggest_post&area=3&page=0&hhtmFrom=vacancy_search_list'

while True:
    if start_page == 1:  # отладочная отсечка
        break
    response = requests.get(url=url, headers=headers)
    if not response.ok:
        break
    soup = bs(response.content, 'html.parser')
    vacancy_list = soup.find_all('div', attrs={'class':['vacancy-serp-item__layout']})

    for el in vacancy_list:
      tag_title = el.find('a', attrs={'class': ['serp-item__title']})
      tag_salary = el.find('span', attrs={'class': ['bloko-header-section-3']})
      tag_employer = el.find('a', attrs={'data-qa': ['vacancy-serp__vacancy-employer']})
      tag_responsibility = el.find('div', attrs={'data-qa': ['vacancy-serp__vacancy_snippet_responsibility']})
      tag_requirement = el.find('div', attrs={'data-qa': ['vacancy-serp__vacancy_snippet_requirement']})

      if tag_title:
        title_text = tag_title.text
        title_href = tag_title['href']
        title_id = re.search(r'\d{6,10}', title_href)[0]
      else:
        title_text, title_href, title_id = '', '', 0
      salary_text = tag_salary.text if tag_salary else 'None'
      employer_text = tag_employer.text if tag_employer else 'None'
      responsibility_text = tag_responsibility.text if tag_responsibility else 'None'
      requirement_text = tag_requirement.text if tag_requirement else 'None'

      result_dict[title_id] = {'title': title_text,
                          'id': title_id,
                          'href': title_href,
                          'salary': salary_text,
                          'employer': employer_text,
                          'responsibility': responsibility_text,
                          'requirement': requirement_text, }
    sleep(5)
    start_page+=1
    print('обработана страница - ', url)
    url = 'https://ekaterinburg.hh.ru/search/vacancy?text=Python&from=suggest_post&area=3&page='+str(start_page)+'&hhtmFrom=vacancy_search_list'
###
with open(seek_vacancy + "_hh.json", "w", encoding='utf-8') as f:
    json.dump(result_dict, f)
###
df = pd.DataFrame(result_dict)
df.to_csv(seek_vacancy + '_hh.csv', sep='\t', encoding='utf-8')
