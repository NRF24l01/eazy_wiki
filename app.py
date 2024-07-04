from flask import Flask, render_template, request, redirect, session, abort, jsonify
from json import loads, dumps, JSONDecodeError
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import create_model

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
User, Wiki = create_model(db)
migrate = Migrate(app, db, compare_type=True)

app.secret_key = 'negrQWERTY123'


def get_user_type_by_code(code):
    print(User.query.filter_by(key=code).first())
    return None  # Return None if the code is not found


def article_edit():
    json_content = ""
    try:
        with open("articles.json", "r", encoding="utf-8") as f:
            json_content = loads(f.read())
    except JSONDecodeError:
        with open("articles.json", "w", encoding="utf-8") as f:
            f.write("{}")
        json_content = {}


def check_user(ses):
    code = ses.get("code", None)
    if not code: return None
    return get_user_type_by_code(code)


def remove_leading_hashtags(text):
    # Проверяем, начинается ли строка с '#'
    if text.startswith('#'):
        # Ищем первый символ, который не является '#'
        i = 0
        while i < len(text) and text[i] == '#':
            i += 1
        # Возвращаем строку без ведущих хештегов
        return text[i:]
    else:
        # Если строка не начинается с '#', возвращаем ее без изменений
        return text


def get_head(md):
    header = md.split("/n")[0].split("")
    header = remove_leading_hashtags(header)
    return header


@app.route('/')
def index():  # put application's code here
    if not check_user(session):
        return render_template("index.html", auth=False)
    else:
        return render_template("index.html", auth=True)


@app.route('/auth', methods=["GET"])
def send_auth():  # put application's code here
    if not check_user(session):
        return render_template("auth.html", error=None)
    else:
        return redirect("/")


@app.route('/logout')
def logout():  # put application's code here
    session.clear()
    return redirect("/")


@app.route('/auth', methods=["POST"])
def auth():  # put application's code here
    code = request.form.get("authCode")
    if not code:
        return redirect("/auth")
    user_type = get_user_type_by_code(code)
    if not user_type:
        return render_template("auth.html", error="Код не найден")
    session["code"] = code
    return redirect("/")


@app.route("/new_page", methods=["GET"])
def create_page():
    if not session.get("code", None):
        return redirect("/auth")
    else:
        return render_template("edit_wiki.html", auth=True)


@app.route("/subm_page", methods=["POST"])
def subm_page():
    if not session.get("code", None):
        return redirect("/auth")
    else:
        return render_template("submit_wiki.html", auth=True)


@app.route("/api/v1/send_md", methods=["POST"])
def recive_md():
    if not get_user_type_by_code(session.get("code", None)):
        return jsonify({"state": False, "err": "please auth"})
    else:
        markdown = request.get_json()["md"]
        print(markdown)
        if markdown:

            return jsonify({"state": True, "link": "/"})
        else:
            return jsonify({"state": False, "err": "Please enter markdown"})


@app.route("/mu")
def mu():
    return render_template("modal_test.html")


if __name__ == '__main__':
    app.run(debug=True)
