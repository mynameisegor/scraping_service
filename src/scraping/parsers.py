import requests
import codecs
from random import randint
from bs4 import BeautifulSoup as BS

__all__ = ('hhru', 'rabota66')

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
]


def hhru(url, city=None, language=None):
    jobs = []
    errors = []
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div = soup.find('div', id='a11y-main-content')
            if main_div:
                div_lst = main_div.find_all('div', attrs={'class': 'serp-item'})
                for div in div_lst:
                    title = div.find('h3')
                    href = title.a['href']
                    content = div.find('div', attrs={'class': 'g-user-content'}).get_text() + \
                              div.find('div', attrs={'class': 'bloko-text'}).get_text()
                    company = div.find('div', attrs={'class': 'vacancy-serp-item-company'}).a.get_text()

                    jobs.append({'title': title.text, 'url': href, 'description': content, 'company': company,
                                  'city_id': city, 'language_id': language})
            else:
                errors.append({'url': url, 'title': 'Div hhru does not exists', })

        else:
            errors.append({'url': url, 'title': 'Page hhru do not response', })

    return jobs, errors


def rabota66(url, city=None, language=None):
    jobs = []
    errors = []
    domain = 'https://www.rabota66.ru'
    if url:
        resp = requests.get(url, headers=headers[randint(0, 2)])
        if resp.status_code == 200:
            soup = BS(resp.content, 'html.parser')
            main_div_habr = soup.find("div", attrs={'id': "vacancy-list"})
            if main_div_habr:
                li_lst = main_div_habr.find_all('li', attrs={'class': "vvl-one vvl-ord- vvl-detaled- show- "
                                                                       "hide-note-comment clearfix"})
                if li_lst:
                    for li in li_lst:
                        link = li.find('div', attrs={'class': "pad- pb5"})
                        title = link.find('a', attrs={'id': True}).text
                        href = li.a['href']
                        company = link.find('div', attrs={'class': "employer- clearfix"}).a.text
                        jobs.append({'title': title, 'url': domain + href, 'company': company,
                                  'city_id': city, 'language_id': language})
                else:
                    errors.append(2)
            else:

                errors.append({'url': url, 'title': 'Div rabota66 does not exists', })

        else:
            errors.append({'url': url, 'title': 'Page rabota66 do not response', })

    return jobs, errors


if __name__ == '__main__':
    url = 'https://www.rabota66.ru/vacancy/search?&limit=30&target=vacancy&q=python&geo_id=3'
    jobs, errors = rabota66(url)
    with codecs.open('../work.txt', 'w', encoding='utf-8') as h:
        h.write(f'{(str(jobs))}, {str(errors)}')
