from flask import Flask, render_template, request, redirect, session, abort, jsonify
from json import loads, dumps
import os

app = Flask(__name__)
app.secret_key = 'negrQWERTY123'
docs_path = "docs.json"
users_path = "users.json"
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "/static/md_editor")


def get_user_type_by_code(code):
    with open(users_path, "r") as f:
        parsed_data = loads(f.read())
    for entry in parsed_data:
        if entry['code'] == code:
            return entry['type']
    return None  # Return None if the code is not found


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


def procces_md(md):
    header = md.split("/n")[0].split("")
    header = remove_leading_hashtags(header)



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
    else: return redirect("/")


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
        return render_template("new_wiki.html", auth=True)

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


if __name__ == '__main__':
    app.run(debug=True)
