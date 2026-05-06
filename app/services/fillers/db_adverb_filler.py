import requests
from bs4 import BeautifulSoup
from app.models import db_session
from app.models.most_used_words.adverbs import Adverb

"""
Создает словарь для карточек самых используемых наречий
Слово - перевод
Записывает перевод в базу данных для дальнейшего использования
"""

db_session.global_init('../../../instance/blogs.db')
url = 'http://komikyv.ru/node/347'
response = requests.get(url)

# Проверка успешности запроса
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    words_block = soup.find('ol')
    words_lines = soup.find_all('ol')

    if words_lines:

        db_sess = db_session.create_session()

        for line in words_lines:
            words = line.find_all('li')
            for word in words:
                value, translate = word.get_text().strip().split(' - ')
                adj = Adverb(value=value, translate=translate)

                db_sess.add(adj)


        db_sess.commit()