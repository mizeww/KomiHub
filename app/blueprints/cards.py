from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify

from app.forms.add_card_form import AddCardForm
from app.forms.change_card_form import ChangeCardForm
from app.models.urls import Url
from app.models import db_session
from app.forms.translate_form import TranslateForm
from app.services.generators.cards_most_used import first_100_nouns, second_100_nouns, third_100_nouns, first_100_adj, \
    second_100_adj

from app.services.generators.cards_test_generator import generate_card_test


cards_bp = Blueprint('cards', __name__, template_folder='../templates', static_folder='../static')


@cards_bp.route('/add_card', methods=['GET', 'POST'])
def add_card():
    form = AddCardForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        url_card = Url(
            name=form.name.data,
            preview_text=form.preview.data,
            link=form.url.data,
            img=form.img.data,
        )

        db_sess.add(url_card)
        db_sess.commit()
        return redirect('/')
    return render_template('add_card.html',
                           title='Добавить карточку',
                           form=form,
                           TranslateForm=TranslateForm())


@cards_bp.route('/change_card', methods=['GET', 'POST'])
def change_card():
    form = ChangeCardForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        db_sess.query(Url).filter(Url.name == form.name.data).update({'name': form.new_name.data,
                                                                      'preview_text': form.preview.data,
                                                                      'link': form.url.data,
                                                                      'img': form.img.data})
        db_sess.commit()
        return redirect('/')
    return render_template('change_card.html',
                           title='Изменить карточку',
                           form=form,
                           TranslateForm=TranslateForm())


@cards_bp.route("/")
def cards():
    db_sess = db_session.create_session()

    cards_chooser = db_sess.query(Url).order_by(Url.id).all()
    return render_template("card_chooser.html",
                           TranslateForm=TranslateForm(),
                           items=cards_chooser)


@cards_bp.route("/random100cards")
def random_100_cards():
    db_sess = db_session.create_session()
    word_cards = generate_card_test(100, db_sess)

    return render_template("cards.html",
                           TranslateForm=TranslateForm(),
                           word_cards=word_cards)


@cards_bp.route("/most_used_nouns/<value>")
def most_used_nouns(value):
    functions = {'first100': first_100_nouns,
                 'second100': second_100_nouns,
                 'third100': third_100_nouns}

    db_sess = db_session.create_session()
    word_cards = functions[value](db_sess)

    return render_template("cards.html",
                           TranslateForm=TranslateForm(),
                           word_cards=word_cards)

@cards_bp.route("/most_used_adjectives/<value>")
def most_used_adjectives(value):

    functions = {'first100': first_100_adj,
                 'second100': second_100_adj}

    db_sess = db_session.create_session()
    word_cards = functions[value](db_sess)

    return render_template("cards.html",
                           TranslateForm=TranslateForm(),
                           word_cards=word_cards)
