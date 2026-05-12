from random import choice

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, session

from app.models import db_session
from app.services.generators.generate_test import generate_trainer_test
from app.forms.choose_answer_form import TrueFalseForm
from app.models.url_trainers import UrlTrainers


trainers_bp = Blueprint('trainers', __name__, template_folder='../templates', static_folder='../static')


@trainers_bp.route("/")
def trainers():
    db_sess = db_session.create_session()

    trainers_chooser = db_sess.query(UrlTrainers).order_by(UrlTrainers.id).all()
    return render_template("trainers.html",
                           items=trainers_chooser)


@trainers_bp.route("/komi_to_rus_test", methods=['GET', 'POST'])
def komi_to_rus_test():
    db_sess = db_session.create_session()
    form = TrueFalseForm()

    if 'stats' not in session:
        session['stats'] = {'correct': 0, 'total': 0}

    if 'current_card' not in session:
        gen = generate_trainer_test(db_sess)
        card = next(gen)

        is_correct_pair = choice([True, False])
        display_rus = card.word_rus

        if not is_correct_pair:
            fake_card = next(generate_trainer_test(db_sess, n=1))
            display_rus = fake_card.word_rus

        session['current_card'] = {
            'word_kom': card.word_kom,
            'display_rus': display_rus,
            'is_real_match': is_correct_pair
        }

    if form.validate_on_submit():
        user_choice = form.answer.data == '1'
        correct_answer = session['current_card']['is_real_match']

        if 'stats' not in session: session['stats'] = {'correct': 0, 'total': 0}

        if user_choice == correct_answer:
            session['stats']['correct'] += 1
        session['stats']['total'] += 1

        step = session['stats']['total']
        if step >= 20:
            total = session['stats']['correct']
            # Сохраняем результат временно, чтобы показать на странице финала
            # прежде чем полностью очистить сессию
            keys_to_reset = ['stats', 'current_card']

            for key in keys_to_reset:
                session.pop(key, None)

            # Возвращаем красивый шаблон финала
            return render_template('result.html', total=total, max_questions=20)

        session.pop('current_card')
        return redirect('komi_to_rus_test')

    return render_template('quiz.html',
                           card=session['current_card'],
                           form=form,
                           stats=session.get('stats'),
                           step=session['stats']['total'])

@trainers_bp.route('/reset')
def reset_session():
    # Список ключей, которые мы использовали для теста
    keys_to_reset = ['quiz_ids', 'current_step', 'correct_count', 'current_task']

    for key in keys_to_reset:
        session.pop(key, None)  # Удаляет ключ, если он есть, не вызывая ошибки

    return redirect('trainers')
