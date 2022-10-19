import codecs
import os
import sys
from django.db import DatabaseError
from django.contrib.auth import get_user_model

proj = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "scraping_service.settings"

import django

django.setup()

from scraping.parsers import *
from scraping.models import City, Vacancy, Language

user = get_user_model()

parsers = ((hhru, 'https://ekaterinburg.hh.ru/search/vacancy?area=3&clusters=true&enable_snippets=true&ored_clusters'
                  '=true&text=python&order_by=publication_time&hhtmFrom=vacancy_search_list'),
           (rabota66, 'https://www.rabota66.ru/vacancy/search?&limit=30&target=vacancy&q=python&geo_id=3'))


def get_settings():
    qs = user.objects.filter(send_email=True).values()
    settings_lst = set((q['sity_id'], q['language_id']) for q in qs)
    return settings_lst


city = City.objects.filter(slug='ekaterinburg').first()
language = Language.objects.filter(slug='python').first()
jobs, errors = [], []
for func, url in parsers:
    j, e = func(url)
    jobs += j
    errors += e

for job in jobs:
    v = Vacancy(**job, city=city, language=language)
    try:
        v.save()
    except DatabaseError:
        pass

# with codecs.open('../work.txt', 'w', encoding='utf-8') as h:
#     h.write(f'{(str(jobs))}, {str(errors)}')
