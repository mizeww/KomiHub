import requests
from bs4 import BeautifulSoup
from data import db_session
from data.nouns import Noun

"""
Создает словарь для карточек самых используемых существительных
Слово - перевод
Записывает перевод в базу данных для дальнейшего использования
"""

db_session.global_init('../db/blogs.db')
url = 'http://komikyv.ru/node/341'
response = requests.get(url)

# Проверка успешности запроса
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    words_block = soup.find('div', 'row row-1')
    words_lines = words_block.find_all('ol')

    if words_lines:

        db_sess = db_session.create_session()

        for line in words_lines:
            words = line.find_all('li')
            for word in words:
                value, translate = word.get_text().strip().split(' – ')
                noun = Noun(value=value, translate=translate)

                db_sess.add(noun)


        db_sess.commit()





