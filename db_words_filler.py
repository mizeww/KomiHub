import requests
from bs4 import BeautifulSoup
from data import db_session
from data.words import Word

"""
Создает словарь для карточек слов
Слово - его суффиксы - перевод - примеры
Записывает перевод в базу данных для дальнейшего использования
"""

db_session.global_init('db/blogs.db')
url = 'http://dict.komikyv.ru/poisk?name=%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%BE-%D0%BA%D0%BE%D0%BC%D0%B8'
response = requests.get(url)


def get_translate(word: str) -> tuple:
    url = f'http://dict.komikyv.ru/post_query?lang=rus-kpv&word={word}'
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    dict = soup.find('tt')

    suffixes = []
    translations = []
    examples_rus = []

    if dict:

        exapmle_all = dict.find_all('example')

        ex = span = []

        suf = dict.find_all('suf')
        t = dict.find_all('t')
        if exapmle_all:
            for exapmle in exapmle_all:
                ex.extend(exapmle.find_all('ex'))
                span.extend(exapmle.find_all('span'))

        if suf:
            for x in suf:
                suffixes.append(x.get_text())

        if t:
            for x in t:
                translations.append(x.get_text())

        if ex:
            for x in ex:
                examples_rus.append(x.get_text())
    else:
        print('None')

    data = (response.status_code, suffixes, translations, examples_rus)

    return data


# Проверка успешности запроса
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    words_block = soup.find('div', 'view-content')
    words = soup.find_all('span', 'field-content')

    if words:
        db_sess = db_session.create_session()

        for word in words[1:]:
            print(word.get_text())
            try:
                response_translate = get_translate(str(word.get_text()))
            except Exception as e:
                print(e)
                response_translate = (0, 0, 0, 0, 0)
            while response_translate[0] != 200:
                try:
                    response_translate = get_translate(...)
                except Exception as e:
                    print(e)
                    continue

            suffixes, translations, examples = response_translate[1:]

            db_word = Word(value=word.get_text(), translate=f'{translations}', suffix=f'{suffixes}',
                           example=f'{examples}')

            db_sess.add(db_word)
            db_sess.commit()

