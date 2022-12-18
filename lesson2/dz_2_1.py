import requests
from pprint import pprint
from lxml import html
import chardet

res_dict = {}
headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           # 'Accept-Encoding':'gzip, deflate, br',
           'Accept-Language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'}
# Сайт Екатеринбургских новостей е1
url = 'https://www.e1.ru'
news_url = url + '/text/'
res = requests.get(url=news_url, headers=headers)
dom = html.fromstring(res.content)
news = dom.xpath("//article[@data-test='archive-record-item']/div/div/h2/a")
for el in news:
    news_href = url + el.attrib['href']
    news_text = el.attrib['title']
    res_dict[news_text] = {
        'url': url,
        'href': news_href,
        'title': news_text,
    }
# Сайт  новостей lenta.ru
url = 'https://lenta.ru'
res = requests.get(url=url, headers=headers)
dom = html.fromstring(res.content)
news = dom.xpath("//a[@class='card-mini _topnews']")
for el in news:
    news_href = el.xpath("./@href")[0]
    news_text = el.xpath("./div/span[@class='card-mini__title']")[0].text
    # news_time = el.xpath("./div/div/time")[0].text
    res_dict[news_text] = {
        'url': url,
        'href': url + news_href,
        'title': news_text,
    }
# news = dom.xpath("//div[@class='last24']/a/div[@class='card-mini__text']/span")
# for el in news:
    # news_text = el.text.encode('utf-16')
    # suffix = chardet.detect(news_text)['encoding']
    # print(news_text.decode(suffix).encode('utf-8').decode('utf-8') )
pprint(res_dict)