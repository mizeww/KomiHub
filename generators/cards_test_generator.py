from random import sample
from sqlalchemy.orm import Session
from data.words import Word
from generators.basic_classes import Card

N_WORDS = 10000 # Предположительное число слов

def generate_card_test(n: int, db_sess: Session):
    unique_word_list = sample(range(1, N_WORDS + 1), n)

    cards_list = []

    for word_id in unique_word_list:
        parse = db_sess.query(Word).filter_by(id=word_id).first()

        card = Card(word_kom=parse.translate,
                    word_rus=parse.value,
                    suffix=parse.suffix,
                    examples=parse.example)

        yield card
