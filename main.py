from flask import Flask, render_template, redirect, request, make_response, session
from data import db_session
from data.users import User
from data.words import Word
from data.urls import Url
from forms.add_card_form import AddCardForm
from forms.change_card_form import ChangeCardForm
from forms.translate_form import TranslateForm
import datetime
from flask_login import LoginManager, login_user, login_required, logout_user
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from generators.basic_classes import Card
from generators.cards_test_generator import generate_card_test
from generators.cards_most_used_nouns import first_100, second_100, third_100

app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
app.config["SECRET_KEY"] = '6752691488291642133722832211molodoyadept6666767'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('register.html',
                           title='Регистрация',
                           form=form,
                           TranslateForm=TranslateForm())


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1

    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")

        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form, TranslateForm=TranslateForm())

    return render_template('login.html', title='Авторизация',
                           form=form,
                           TranslateForm=TranslateForm())


@app.route('/cards/add_card', methods=['GET', 'POST'])
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
        return redirect('/cards')
    return render_template('add_card.html',
                           title='Добавить карточку',
                           form=form,
                           TranslateForm=TranslateForm())

@app.route('/cards/change_card', methods=['GET', 'POST'])
def change_card():
    form = ChangeCardForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()


        db_sess.query(Url).filter(Url.name == form.name.data).update({'name': form.new_name.data,
                                                                      'preview_text': form.preview.data,
                                                                      'link': form.url.data,
                                                                      'img': form.img.data})
        db_sess.commit()
        return redirect('/cards')
    return render_template('change_card.html',
                           title='Изменить карточку',
                           form=form,
                           TranslateForm=TranslateForm())

@app.route("/")
def index():
    return render_template("index.html",
                           TranslateForm=TranslateForm(),
                           title='Komi Hub')

@app.route("/cards")
def cards():
    db_sess = db_session.create_session()

    cards_chooser = db_sess.query(Url).order_by(Url.id).all()
    return render_template("card_chooser.html",
                           TranslateForm=TranslateForm(),
                           items=cards_chooser)

@app.route("/cards/random100cards")
def random_100_cards():

    db_sess = db_session.create_session()
    word_cards = generate_card_test(100, db_sess)

    return render_template("cards.html",
                           TranslateForm=TranslateForm(),
                           word_cards=word_cards)

@app.route("/cards/most_used_nouns/<value>")
def most_used_nouns(value):

    functions = {'first100': first_100,
                 'second100': second_100,
                 'third100': third_100}

    db_sess = db_session.create_session()
    word_cards = functions[value](db_sess)

    return render_template("cards.html",
                           TranslateForm=TranslateForm(),
                           word_cards=word_cards)


@app.route("/user")
@login_required
def user():
    # db_sess = db_session.create_session()
    # news = db_sess.query(News).filter(News.is_private != True)
    return render_template("user.html", TranslateForm=TranslateForm())


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/translate/<word>')
def translate(word):
    db_sess = db_session.create_session()
    data1 = db_sess.query(Word).filter(Word.value == word.lower()).first()
    data2 = db_sess.query(Word).filter(Word.translate.like(f'%{word.lower()}%')).first()

    res = ''

    if data1:
        strdata = data1.translate
        for i in strdata:
            if i not in "['']":
                res += i
    elif data2:
        strdata = data2.value
        for i in strdata:
            if i not in "['']":
                res += i

    if not res:
        res = 'Слово не найдено'

    return render_template("translate.html",
                           word=word,
                           translate=res,
                           title="Komi Lang",
                           TranslateForm=TranslateForm())


if __name__ == '__main__':
    db_session.global_init('db/blogs.db')
    app.run(host="127.0.0.1", port=8081, debug=True)
