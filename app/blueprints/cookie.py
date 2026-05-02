from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, make_response, session

cookie_bp = Blueprint('cookie', __name__, template_folder='../templates', static_folder='../static')

@cookie_bp.route("/cookie_test")
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


@cookie_bp.route("/session_test")
def session_test():
    visits_count = session.get('visits_count', 0)
    session['visits_count'] = visits_count + 1

    return make_response(
        f"Вы пришли на эту страницу {visits_count + 1} раз")