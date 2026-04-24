from random import sample
from sqlalchemy.orm import Session
from data.words import Word


class Card:
    def __init__(self, word_kom: str,
                 word_rus: str,
                 suffix: tuple,
                 examples: tuple):
        self.word_kom = word_kom
        self.word_rus = word_rus
        self.suffix = suffix
        self.examples = examples

N_WORDS = 10000 # Предположительное число слов

def generate_card_test(n: int, db_sess: Session):
    unique_word_list = sample(range(1, N_WORDS + 1), n)

    cards_list = []

    for word_id in unique_word_list:
        parse = db_sess.query(Word).filter_by(id=word_id).first()

        card = ...

        yield card
