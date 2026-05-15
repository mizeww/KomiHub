import sqlalchemy
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_required

from app.forms.add_card_form import AddCardForm
from app.forms.change_card_form import ChangeCardForm
from app.models.card_views import CardView
from app.models.urls import Url
from app.models import db_session
from app.services.generators.cards_most_used import first_100_nouns, second_100_nouns, third_100_nouns, first_100_adj, \
    second_100_adj, first_100_verbs, first_50_adv

from app.services.generators.cards_test_generator import generate_card_test

from flask import render_template, abort, session, jsonify
from app.models.most_used_words.nouns import Noun
from app.models.most_used_words.adjective import Adjective
from app.models.most_used_words.verbs import Verb
from app.models.most_used_words.adverbs import Adverb

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
                           form=form)


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
                           form=form)


@cards_bp.route("/")
def cards():
    db_sess = db_session.create_session()

    cards_chooser = db_sess.query(Url).order_by(Url.id).all()
    return render_template("card_chooser.html",
                           items=cards_chooser)


@cards_bp.route("/random/<int:value>")
def random_value_cards(value):
    db_sess = db_session.create_session()
    word_cards = generate_card_test(value, db_sess)

    return render_template("cards.html",
                           word_cards=word_cards)


@cards_bp.route("/most_used_nouns/<value>")
def most_used_nouns(value):
    functions = {'first100': first_100_nouns,
                 'second100': second_100_nouns,
                 'third100': third_100_nouns}

    db_sess = db_session.create_session()
    word_cards = functions[value](db_sess)

    return render_template("cards.html",
                           word_cards=word_cards,
                           folder='nouns')

@cards_bp.route("/most_used_adjectives/<value>")
def most_used_adjectives(value):

    functions = {'first100': first_100_adj,
                 'second100': second_100_adj}

    db_sess = db_session.create_session()
    word_cards = functions[value](db_sess)

    return render_template("cards.html",
                           word_cards=word_cards,
                           folder='adjectives')

@cards_bp.route("/most_used_verbs/<value>")
def most_used_verbs(value):

    functions = {'first100': first_100_verbs}

    db_sess = db_session.create_session()
    word_cards = functions[value](db_sess)

    return render_template("cards.html",
                           word_cards=word_cards,
                           folder='verbs')

@cards_bp.route("/most_used_adverbs/<value>")
def most_used_adverbs(value):

    functions = {'first50': first_50_adv}

    db_sess = db_session.create_session()
    word_cards = functions[value](db_sess)

    return render_template("cards.html",
                           word_cards=word_cards,
                           folder='adverbs')


from flask import render_template, abort
from flask_login import current_user
from app.models import db_session
from app.models.card_views import CardView
from app.models.most_used_words.nouns import Noun
from app.models.most_used_words.adjective import Adjective
from app.models.most_used_words.verbs import Verb
from app.models.most_used_words.adverbs import Adverb
import sqlalchemy


@cards_bp.route("/view/<folder>/<int:card_id>")
def view_single_card(folder, card_id):
    db_sess = db_session.create_session()
    models = {'nouns': Noun, 'adjectives': Adjective, 'verbs': Verb, 'adverbs': Adverb}

    if folder not in models:
        abort(404)

    card = db_sess.query(models[folder]).get(card_id)
    if not card:
        abort(404)

    # НАДЁЖНЫЙ ТРЕКИНГ: Если пользователь авторизован, записываем просмотр прямо здесь
    if current_user.is_authenticated:
        exists = db_sess.query(CardView).filter(
            CardView.user_id == current_user.id,
            CardView.folder == folder,
            CardView.card_id == card_id
        ).first()

        if not exists:
            try:
                new_view = CardView(
                    user_id=current_user.id,
                    folder=folder,
                    card_id=card_id
                )
                db_sess.add(new_view)
                db_sess.commit()
            except sqlalchemy.exc.IntegrityError:
                db_sess.rollback()  # Защита от случайных дубликатов при обновлении страницы
    html_content = render_template("single_card.html", card=card, folder=folder)

    db_sess.close()

    return html_content


@cards_bp.route("/track_view/<folder>/<int:card_id>", methods=['POST'])
@login_required
def track_view(folder, card_id):
    db_sess = db_session.create_session()

    # Проверяем, не смотрел ли пользователь эту карточку ранее
    exists = db_sess.query(CardView).filter(
        CardView.user_id == current_user.id,
        CardView.folder == folder,
        CardView.card_id == card_id
    ).first()

    if not exists:
        try:
            new_view = CardView(
                user_id=current_user.id,
                folder=folder,
                card_id=card_id
            )
            db_sess.add(new_view)
            db_sess.commit()
        except sqlalchemy.exc.IntegrityError:
            db_sess.rollback()  # Защита от гонки условий при быстром двойном клике

    return jsonify({'success': True})

