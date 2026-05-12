from random import sample
from sqlalchemy.orm import Session
from app.models.words import Word
from app.services.generators.basic_classes import Card
import re

N_WORDS = 12460 # Предположительное число слов

def generate_trainer_test(db_sess: Session, n=20):
    unique_word_list = sample(range(1, N_WORDS + 1), n)

    for word_id in unique_word_list:
        parse = db_sess.query(Word).filter_by(id=word_id).first()

        list_kom_words = re.findall(r'[^\[\]\,\']+', parse.translate, re.IGNORECASE)

        card = Card(word_kom=list_kom_words[0],
                    word_rus=parse.value,
                    suffix=parse.suffix,
                    examples=parse.example,
                    id=word_id)

        yield card


