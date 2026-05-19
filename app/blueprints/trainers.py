from random import choice, shuffle

from flask import Blueprint

from app.forms.trainers.input_form import InputTrainerForm
from app.forms.trainers.multiple_choose_form import ChoiceTrainerForm
from app.models import db_session
from app.services.generators.generate_test import generate_trainer_test, generate_trainer_test_nouns
from app.forms.trainers.choose_answer_form import TrueFalseForm
from app.models.url_trainers import UrlTrainers

trainers_bp = Blueprint('trainers', __name__, template_folder='../templates/trainers', static_folder='../static')


@trainers_bp.route("/")
def trainers():
    db_sess = db_session.create_session()

    trainers_chooser = db_sess.query(UrlTrainers).order_by(UrlTrainers.id).all()
    return render_template("trainers.html",
                           items=trainers_chooser)


from flask import session, render_template, redirect, url_for


@trainers_bp.route("/komi_to_rus_test", methods=['GET', 'POST'])
def komi_to_rus_test():
    db_sess = db_session.create_session()
    form = TrueFalseForm()

    # Сброс и чистая инициализация при первом GET-заходе
    if session.get('quiz_active') != 'komi_to_rus_test':
        session.pop('stats', None)
        session.pop('current_card', None)
        session['stats'] = {'correct': 0, 'total': 0}
        session['quiz_active'] = True  # Активируем маркер теста

    # Подстраховка на случай непредвиденного сброса
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

        if user_choice == correct_answer:
            session['stats']['correct'] += 1
        session['stats']['total'] += 1

        step = session['stats']['total']
        if step >= 20:
            total = session['stats']['correct']
            # Полностью вычищаем всё, включая маркер активности
            keys_to_reset = ['stats', 'current_card', 'quiz_active']
            for key in keys_to_reset:
                session.pop(key, None)
            return render_template('result.html', total=total, max_questions=20, test_name='komi_to_rus_test')

        session.pop('current_card', None)
        return redirect('komi_to_rus_test')

    return render_template('quiz_true_false.html',
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


@trainers_bp.route("/choice_test", methods=['GET', 'POST'])
def choice_test():
    db_sess = db_session.create_session()
    form = ChoiceTrainerForm()

    # ИСПРАВЛЕНО: Теперь записывается ИМЯ ТЕСТА, а не True
    if session.get('quiz_active') != 'choice_test':
        session.pop('stats', None)
        session.pop('current_card', None)
        session['stats'] = {'correct': 0, 'total': 0}
        session['quiz_active'] = 'choice_test'  # <--- Здесь должна быть строка!

    if 'stats' not in session:
        session['stats'] = {'correct': 0, 'total': 0}

    # 1. Проверяем наличие карточки
    if 'current_card' not in session:
        gen = generate_trainer_test(db_sess)
        card = next(gen)

        fake_gen = generate_trainer_test(db_sess, n=3)
        options = [f_card.word_rus for f_card in fake_gen]
        options.append(card.word_rus)
        shuffle(options)

        session['current_card'] = {
            'word_kom': card.word_kom,
            'correct_answer': card.word_rus,
            'options': options
        }

    # 2. Наполняем форму
    form.answer.choices = [(opt, opt) for opt in session['current_card']['options']]

    # 3. Валидация формы
    if form.validate_on_submit():
        user_choice = form.answer.data
        correct_answer = session['current_card']['correct_answer']

        if user_choice == correct_answer:
            session['stats']['correct'] += 1
        session['stats']['total'] += 1

        step = session['stats']['total']
        if step >= 20:
            total = session['stats']['correct']
            keys_to_reset = ['stats', 'current_card', 'quiz_active']
            for key in keys_to_reset:
                session.pop(key, None)
            return render_template('result.html', total=total, max_questions=20, test_name='choice_test')

        session.pop('current_card', None)

        # ИСПРАВЛЕНО: Используем url_for для Blueprint
        return redirect(url_for('trainers.choice_test'))

    return render_template('quiz_choice.html',
                           card=session['current_card'],
                           form=form,
                           stats=session.get('stats'),
                           step=session['stats']['total'])


@trainers_bp.route("/input_test", methods=['GET', 'POST'])
def input_test():
    db_sess = db_session.create_session()
    form = InputTrainerForm()

    if session.get('quiz_active') != 'input_test':
        session.pop('stats', None)
        session.pop('current_card', None)
        session['stats'] = {'correct': 0, 'total': 0}
        session['quiz_active'] = 'input_test'

    if 'stats' not in session:
        session['stats'] = {'correct': 0, 'total': 0}

    if 'current_card' not in session:
        gen = generate_trainer_test(db_sess)
        card = next(gen)

        session['current_card'] = {
            'word_kom': card.word_kom,
            'correct_answer': card.word_rus
        }

    if form.validate_on_submit():
        user_choice = form.answer.data.strip().lower()
        correct_answer = session['current_card']['correct_answer'].strip().lower()

        if user_choice == correct_answer:
            session['stats']['correct'] += 1
        session['stats']['total'] += 1

        step = session['stats']['total']
        if step >= 20:
            total = session['stats']['correct']
            keys_to_reset = ['stats', 'current_card', 'quiz_active']
            for key in keys_to_reset:
                session.pop(key, None)
            return render_template('result.html', total=total, max_questions=20, test_name='input_test')

        session.pop('current_card', None)
        return redirect(url_for('trainers.input_test'))

    return render_template('quiz_input.html',
                           card=session['current_card'],
                           form=form,
                           stats=session.get('stats'),
                           step=session['stats']['total'])


@trainers_bp.route("/scramble_test", methods=['GET', 'POST'])
def scramble_test():
    db_sess = db_session.create_session()
    form = InputTrainerForm()

    if session.get('quiz_active') != 'scramble_test':
        session.pop('stats', None)
        session.pop('current_card', None)
        session['stats'] = {'correct': 0, 'total': 0}
        session['quiz_active'] = 'scramble_test'

    if 'stats' not in session:
        session['stats'] = {'correct': 0, 'total': 0}

    if 'current_card' not in session:
        gen = generate_trainer_test(db_sess)
        card = next(gen)

        letters = list(card.word_kom)
        if len(letters) > 1:
            original = list(letters)
            while letters == original:
                shuffle(letters)
        scrambled_word = "".join(letters)

        session['current_card'] = {
            'word_rus': card.word_rus,
            'scrambled_word': scrambled_word,
            'correct_answer': card.word_kom
        }

    if form.validate_on_submit():
        user_choice = form.answer.data.strip().lower()
        correct_answer = session['current_card']['correct_answer'].strip().lower()

        if user_choice == correct_answer:
            session['stats']['correct'] += 1
        session['stats']['total'] += 1

        step = session['stats']['total']
        if step >= 20:
            total = session['stats']['correct']
            keys_to_reset = ['stats', 'current_card', 'quiz_active']
            for key in keys_to_reset:
                session.pop(key, None)
            return render_template('result.html', total=total, max_questions=20, test_name='scramble_test')

        session.pop('current_card', None)
        return redirect(url_for('trainers.scramble_test'))

    return render_template('quiz_scramble.html',
                           card=session['current_card'],
                           form=form,
                           stats=session.get('stats'),
                           step=session['stats']['total'])


@trainers_bp.route("/komi_to_rus_test_nouns", methods=['GET', 'POST'])
def komi_to_rus_test_nouns():
    db_sess = db_session.create_session()
    form = TrueFalseForm()

    # Сброс и чистая инициализация при первом GET-заходе
    if session.get('quiz_active') != 'komi_to_rus_test':
        session.pop('stats', None)
        session.pop('current_card', None)
        session['stats'] = {'correct': 0, 'total': 0}
        session['quiz_active'] = True  # Активируем маркер теста

    # Подстраховка на случай непредвиденного сброса
    if 'stats' not in session:
        session['stats'] = {'correct': 0, 'total': 0}

    if 'current_card' not in session:
        gen = generate_trainer_test_nouns(db_sess)
        card = next(gen)

        is_correct_pair = choice([True, False])
        display_rus = card.word_rus

        if not is_correct_pair:
            fake_card = next(generate_trainer_test_nouns(db_sess, n=1))
            display_rus = fake_card.word_rus

        session['current_card'] = {
            'word_kom': card.word_kom,
            'display_rus': display_rus,
            'is_real_match': is_correct_pair
        }

    if form.validate_on_submit():
        user_choice = form.answer.data == '1'
        correct_answer = session['current_card']['is_real_match']

        if user_choice == correct_answer:
            session['stats']['correct'] += 1
        session['stats']['total'] += 1

        step = session['stats']['total']
        if step >= 20:
            total = session['stats']['correct']
            # Полностью вычищаем всё, включая маркер активности
            keys_to_reset = ['stats', 'current_card', 'quiz_active']
            for key in keys_to_reset:
                session.pop(key, None)
            return render_template('result.html', total=total, max_questions=20, test_name='komi_to_rus_test')

        session.pop('current_card', None)
        return redirect(url_for('trainers.komi_to_rus_test_nouns'))

    return render_template('quiz_true_false.html',
                           card=session['current_card'],
                           form=form,
                           stats=session.get('stats'),
                           step=session['stats']['total'])


@trainers_bp.route("/choice_test_nouns", methods=['GET', 'POST'])
def choice_test_nouns():
    db_sess = db_session.create_session()
    form = ChoiceTrainerForm()

    # ИСПРАВЛЕНО: Теперь записывается ИМЯ ТЕСТА, а не True
    if session.get('quiz_active') != 'choice_test':
        session.pop('stats', None)
        session.pop('current_card', None)
        session['stats'] = {'correct': 0, 'total': 0}
        session['quiz_active'] = 'choice_test'  # <--- Здесь должна быть строка!

    if 'stats' not in session:
        session['stats'] = {'correct': 0, 'total': 0}

    # 1. Проверяем наличие карточки
    if 'current_card' not in session:
        gen = generate_trainer_test_nouns(db_sess)
        card = next(gen)

        fake_gen = generate_trainer_test_nouns(db_sess, n=3)
        options = [f_card.word_rus for f_card in fake_gen]
        options.append(card.word_rus)
        shuffle(options)

        session['current_card'] = {
            'word_kom': card.word_kom,
            'correct_answer': card.word_rus,
            'options': options
        }

    # 2. Наполняем форму
    form.answer.choices = [(opt, opt) for opt in session['current_card']['options']]

    # 3. Валидация формы
    if form.validate_on_submit():
        user_choice = form.answer.data
        correct_answer = session['current_card']['correct_answer']

        if user_choice == correct_answer:
            session['stats']['correct'] += 1
        session['stats']['total'] += 1

        step = session['stats']['total']
        if step >= 20:
            total = session['stats']['correct']
            keys_to_reset = ['stats', 'current_card', 'quiz_active']
            for key in keys_to_reset:
                session.pop(key, None)
            return render_template('result.html', total=total, max_questions=20, test_name='choice_test')

        session.pop('current_card', None)

        # ИСПРАВЛЕНО: Используем url_for для Blueprint
        return redirect(url_for('trainers.choice_test_nouns'))

    return render_template('quiz_choice.html',
                           card=session['current_card'],
                           form=form,
                           stats=session.get('stats'),
                           step=session['stats']['total'])


@trainers_bp.route("/input_test_nouns", methods=['GET', 'POST'])
def input_test_nouns():
    db_sess = db_session.create_session()
    form = InputTrainerForm()

    if session.get('quiz_active') != 'input_test':
        session.pop('stats', None)
        session.pop('current_card', None)
        session['stats'] = {'correct': 0, 'total': 0}
        session['quiz_active'] = 'input_test'

    if 'stats' not in session:
        session['stats'] = {'correct': 0, 'total': 0}

    if 'current_card' not in session:
        gen = generate_trainer_test_nouns(db_sess)
        card = next(gen)

        session['current_card'] = {
            'word_kom': card.word_kom,
            'correct_answer': card.word_rus
        }

    if form.validate_on_submit():
        user_choice = form.answer.data.strip().lower()
        correct_answer = session['current_card']['correct_answer'].strip().lower()

        if user_choice == correct_answer:
            session['stats']['correct'] += 1
        session['stats']['total'] += 1

        step = session['stats']['total']
        if step >= 20:
            total = session['stats']['correct']
            keys_to_reset = ['stats', 'current_card', 'quiz_active']
            for key in keys_to_reset:
                session.pop(key, None)
            return render_template('result.html', total=total, max_questions=20, test_name='input_test')

        session.pop('current_card', None)
        return redirect(url_for('trainers.input_test_nouns'))

    return render_template('quiz_input.html',
                           card=session['current_card'],
                           form=form,
                           stats=session.get('stats'),
                           step=session['stats']['total'])


@trainers_bp.route("/scramble_test_nouns", methods=['GET', 'POST'])
def scramble_test_nouns():
    db_sess = db_session.create_session()
    form = InputTrainerForm()

    if session.get('quiz_active') != 'scramble_test':
        session.pop('stats', None)
        session.pop('current_card', None)
        session['stats'] = {'correct': 0, 'total': 0}
        session['quiz_active'] = 'scramble_test'

    if 'stats' not in session:
        session['stats'] = {'correct': 0, 'total': 0}

    if 'current_card' not in session:
        gen = generate_trainer_test_nouns(db_sess)
        card = next(gen)

        letters = list(card.word_kom)
        if len(letters) > 1:
            original = list(letters)
            while letters == original:
                shuffle(letters)
        scrambled_word = "".join(letters)

        session['current_card'] = {
            'word_rus': card.word_rus,
            'scrambled_word': scrambled_word,
            'correct_answer': card.word_kom
        }

    if form.validate_on_submit():
        user_choice = form.answer.data.strip().lower()
        correct_answer = session['current_card']['correct_answer'].strip().lower()

        if user_choice == correct_answer:
            session['stats']['correct'] += 1
        session['stats']['total'] += 1

        step = session['stats']['total']
        if step >= 20:
            total = session['stats']['correct']
            keys_to_reset = ['stats', 'current_card', 'quiz_active']
            for key in keys_to_reset:
                session.pop(key, None)
            return render_template('result.html', total=total, max_questions=20, test_name='scramble_test')

        session.pop('current_card', None)
        return redirect(url_for('trainers.scramble_test_nouns'))

    return render_template('quiz_scramble.html',
                           card=session['current_card'],
                           form=form,
                           stats=session.get('stats'),
                           step=session['stats']['total'])
