import requests
from bs4 import BeautifulSoup
from data import db_session
from data.urls import Url

"""
Создает дб для для перехода по карточкам
название - описание - ссылка - фото
Записывает в базу данных для дальнейшего использования
"""

db_session.global_init('../db/blogs.db')

db_sess = db_session.create_session()

name = input()
preview_text = input()
link = input()
img = input()

url = Url(name=name, preview_text=preview_text, link=link, img=img)

db_sess.add(url)
db_sess.commit()


'''
вторые 100 самых используемых слов
набор из 100 слов
/cards/most_used_nouns/second100
None
'''