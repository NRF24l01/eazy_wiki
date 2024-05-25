from flask import Flask, render_template, request, redirect, session, abort
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


@app.route('/')
def index():  # put application's code here
    if not session.get("code", None):
        return render_template("index.html", auth=False)
    else:
        return render_template("index.html", auth=True)


@app.route('/auth', methods=["GET"])
def send_auth():  # put application's code here
    return render_template("auth.html", error=None)


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


@app.route('/editor.md/<path:filepath>', methods=['GET'])
def get_file(filepath):
    return redirect("/static/md_editor/"+filepath)


if __name__ == '__main__':
    app.run(debug=True)
