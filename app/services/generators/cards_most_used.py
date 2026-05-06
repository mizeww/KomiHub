from sqlalchemy.orm import Session
from app.models.most_used_words.nouns import Noun
from app.models.most_used_words.adjective import Adjective
from app.models.most_used_words.verbs import Verb
from app.models.most_used_words.adverbs import Adverb
from app.services.generators.basic_classes import Card

def first_100_nouns(db_sess: Session):
    parse = db_sess.query(Noun).filter(Noun.id.between(1, 100)).all()

    for word in parse:
        word_kom, word_rus = word.value, word.translate

        card = Card(word_kom=word_kom, word_rus=word_rus, suffix=(), examples=(), id=word.id)

        yield card

def second_100_nouns(db_sess: Session):
    parse = db_sess.query(Noun).filter(Noun.id.between(101, 200)).all()

    for word in parse:
        word_kom, word_rus = word.value, word.translate

        card = Card(word_kom=word_kom, word_rus=word_rus, suffix=(), examples=(), id=word.id)

        yield card

def third_100_nouns(db_sess: Session):
    parse = db_sess.query(Noun).filter(Noun.id.between(201, 300)).all()

    for word in parse:
        word_kom, word_rus = word.value, word.translate

        card = Card(word_kom=word_kom, word_rus=word_rus, suffix=(), examples=(), id=word.id)

        yield card

def first_100_adj(db_sess: Session):
    parse = db_sess.query(Adjective).filter(Adjective.id.between(1, 100)).all()

    for word in parse:
        word_kom, word_rus = word.value, word.translate

        card = Card(word_kom=word_kom, word_rus=word_rus, suffix=(), examples=(), id=word.id)

        yield card

def second_100_adj(db_sess: Session):
    parse = db_sess.query(Adjective).filter(Adjective.id.between(101, 200)).all()

    for word in parse:
        word_kom, word_rus = word.value, word.translate

        card = Card(word_kom=word_kom, word_rus=word_rus, suffix=(), examples=(), id=word.id)

        yield card

def first_100_verbs(db_sess: Session):
    parse = db_sess.query(Verb).filter(Verb.id.between(1, 100)).all()

    for word in parse:
        word_kom, word_rus = word.value, word.translate

        card = Card(word_kom=word_kom, word_rus=word_rus, suffix=(), examples=(), id=word.id)

        yield card

def first_50_adv(db_sess: Session):
    parse = db_sess.query(Adverb).filter(Adverb.id.between(1, 50)).all()

    for word in parse:
        word_kom, word_rus = word.value, word.translate

        card = Card(word_kom=word_kom, word_rus=word_rus, suffix=(), examples=(), id=word.id)

        yield card