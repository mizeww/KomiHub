from sqlalchemy.orm import Session
from app.models.nouns import Noun
from app.models.adjective import Adjective
from app.services.generators.basic_classes import Card

def first_100_nouns(db_sess: Session):
    parse = db_sess.query(Noun).filter(Noun.id.between(1, 100)).all()

    for word in parse:
        word_kom, word_rus = word.value, word.translate

        card = Card(word_kom=word_kom, word_rus=word_rus, suffix=(), examples=())

        yield card

def second_100_nouns(db_sess: Session):
    parse = db_sess.query(Noun).filter(Noun.id.between(101, 200)).all()

    for word in parse:
        word_kom, word_rus = word.value, word.translate

        card = Card(word_kom=word_kom, word_rus=word_rus, suffix=(), examples=())

        yield card

def third_100_nouns(db_sess: Session):
    parse = db_sess.query(Noun).filter(Noun.id.between(201, 300)).all()

    for word in parse:
        word_kom, word_rus = word.value, word.translate

        card = Card(word_kom=word_kom, word_rus=word_rus, suffix=(), examples=())

        yield card

def first_100_adj(db_sess: Session):
    parse = db_sess.query(Adjective).filter(Adjective.id.between(1, 100)).all()

    for word in parse:
        word_kom, word_rus = word.value, word.translate

        card = Card(word_kom=word_kom, word_rus=word_rus, suffix=(), examples=())

        yield card

def second_100_adj(db_sess: Session):
    parse = db_sess.query(Adjective).filter(Adjective.id.between(101, 200)).all()

    for word in parse:
        word_kom, word_rus = word.value, word.translate

        card = Card(word_kom=word_kom, word_rus=word_rus, suffix=(), examples=())

        yield card