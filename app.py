from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route('/')
def index():  # put application's code here
    return render_template("index.html")


@app.route('/auth', method=["GET"])
def send_auth():  # put application's code here
    return render_template("auth.html")

@app.route('/auth', method=["POST"])
def auth():  # put application's code here
    code = request.form.get("authCode")
    if not code:
        return redirect("/auth")



if __name__ == '__main__':
    app.run(debug=True)
