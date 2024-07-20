from flask import Flask, render_template, request, redirect, session, abort, jsonify
from json import loads, dumps, JSONDecodeError
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import create_model
from os import makedirs, path
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
User, Wiki = create_model(db)
migrate = Migrate(app, db, compare_type=True)

app.secret_key = 'negrQWERTY123'
makedirs("instance/files/images", exist_ok=True)
makedirs("instance/files/wikis", exist_ok=True)

def article_edit():
    json_content = ""
    try:
        with open("articles.json", "r", encoding="utf-8") as f:
            json_content = loads(f.read())
    except JSONDecodeError:
        with open("articles.json", "w", encoding="utf-8") as f:
            f.write("{}")
        json_content = {}


def check_user_by_code(code):
    if not User.query.filter_by(key=code).first(): return None
    return User.query.filter_by(key=code).first()


def check_user(ses) -> None:
    code = ses.get("code", None)
    if not User.query.filter_by(key=code).first(): return None
    return User.query.filter_by(key=code).first()


def can_write(ses):
    if not check_user(ses): return None
    if check_user(ses).can_write:
        return True
    return False


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
    user_type = check_user_by_code(code)
    if not user_type:
        return render_template("auth.html", error="Код не найден")
    session["code"] = code
    return redirect("/")


@app.route("/new_page", methods=["GET"])
def create_page():
    if not can_write(session):
        abort(403)
    else:
        return render_template("edit_wiki.html", auth=True)


@app.route("/api/v1/send_md", methods=["POST"])
def recive_md():
    if not can_write(session):
        abort(403)
    else:
        markdown = request.get_json()["md"]
        print(markdown)
        session["md"] = markdown
        if markdown:
            return jsonify({"state": True, "link": "/final_config_docs"})
        else:
            return jsonify({"state": False, "err": "Please enter markdown"})


@app.route("/final_config_docs", methods=["GET"])
def final_config_docs():
    if not can_write(session):
        abort(403)
    else:
        return render_template("final_config.html", auth=True, md=session.get("md", None))


@app.route("/final_config_docs", methods=["POST"])
def save_docs():
    if not can_write(session):
        abort(403)
    else:
        uploaded_file = request.files['cover']
        filename = secure_filename(uploaded_file.filename)
        wiki_title, desc = request.form.get("title"), request.form.get("desc")

        with open(path.join("instance/files/wikis", wiki_title+".md"), "w", encoding="UTF-8") as f: f.write(session.get("md", ""))
        uploaded_file.save(path.join("instance/files/images", filename))

        new_wiki = Wiki(title=wiki_title, desc=desc, path_to_md=path.join("instance/files/wikis", wiki_title+".md"), path_to_logo=path.join("instance/files/images", filename))
        db.session.add(new_wiki)
        db.session.commit()

        return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
