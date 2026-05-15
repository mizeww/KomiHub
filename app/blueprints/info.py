from flask import Blueprint, render_template

info_bp = Blueprint('info', __name__, template_folder='templates')

@info_bp.route('/conspect')
def notes():
    return render_template('info/conspect.html', title='Конспекты')

@info_bp.route('/about')
def about_language():
    return render_template('info/about.html', title='О коми языке')

@info_bp.route('/developers')
def developers():
    return render_template('info/developers.html', title='Разработчики')

@info_bp.route('/usefulinfo')
def useful_links():
    return render_template('info/usefulinfo.html', title='Полезная информация')
