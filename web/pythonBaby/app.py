# @author: ch3
# @date: 2024.04.03
import logging
import os
import re
import uuid
from flask import Flask, json, jsonify
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session

from Message import Message, MessageManager
from flask_session import Session

global app

app = Flask(__name__, static_folder=os.path.join(os.getcwd(), "static"),
            template_folder=os.path.join(os.getcwd(), "templates"))

app.config['SESSION_TYPE'] = "filesystem"
app.logger.setLevel(logging.DEBUG)

Session(app)

UserList = {}
MsgManager = MessageManager()


class User:

    def __init__(self):
        self.username = ""
        self.password = ""


admin = User()
admin.username = "admin"
admin.password = str(uuid.uuid4())
UserList["admin"] = admin


def CheckLogin(username: str, password: str):
    if username in UserList.keys() and (str(UserList.get(username, "").username) == username) and (
            str(UserList.get(username, "").password) == password):
        return True
    else:
        return False


def CheckCharAndLen(content: str):
    pattern = r'^[a-zA-Z0-9]+$'
    if re.match(pattern, content) and len(content) >= 5:
        return True
    else:
        return False


def CheckRegisterUser(username: str):
    user = UserList.get(username, None)
    if user:
        return True
    else:
        return False


def merge(src, dst):
    for k, v in src.items():
        if hasattr(dst, '__getitem__'):
            if dst.get(k) and type(v) == dict:
                merge(v, dst.get(k))
            else:
                dst[k] = v
        elif hasattr(dst, k) and type(v) == dict:
            merge(v, getattr(dst, k))
        else:
            setattr(dst, k, v)


@app.route('/')
def welcome():
    return redirect(url_for("index"))


@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/register', methods=['GET'])
def _register():
    return render_template("register.html")


@app.route('/register', methods=['POST'])
def register():
    if request.data:
        try:
            data = json.loads(request.data)
            if "username" not in data or "password" not in data:
                return jsonify({"redirect": "/error"}), 500

            username = data["username"]
            password = data["password"]
            if not (CheckCharAndLen(username) and CheckCharAndLen(password)):
                return jsonify({"redirect": "/error"}), 500

            if CheckRegisterUser(username):
                return jsonify({"redirect": "/error"}), 500

            user = User()
            merge(data, user)
            UserList[user.username] = user

        except Exception:
            return jsonify({"redirect": "/error"}), 500
        return jsonify({"redirect": "/login"}), 200
    else:
        return jsonify({"redirect": "/error"}), 500


@app.route('/login', methods=['GET'])
def _login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    if request.data:
        try:
            data = json.loads(request.data)
            if "username" not in data or "password" not in data:
                return jsonify({"redirect": "/error"}), 500

            username = data["username"]
            password = data["password"]

            if not CheckLogin(username, password):
                return jsonify({"redirect": "/error"}), 500

            session["username"] = username
            return jsonify({"redirect": f"/profile/{username}"}), 200
        except Exception:
            return jsonify({"redirect": "/error"}), 500
    return jsonify({"redirect": "/error"}), 500


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for("index"))


@app.route('/profile/<username>', methods=['POST', 'GET'])
def profile(username=None):
    if session.get("username", None) != username:
        return render_template("error.html"), 500
    if username == "admin":
        return render_template("admin.html", username=username)
    else:
        return render_template("normal.html", username=username)


@app.route('/profile/admin/edit/api', methods=['GET'])
def _edit():
    # check session
    if session.get("username", None) != "admin":
        return jsonify({"redirect": "/error"}), 500
    return jsonify({"redirect": "/profile/admin/edit"}), 200


@app.route('/profile/admin/edit', methods=['GET'])
def __edit():
    # check session
    if session.get("username", None) != "admin":
        return jsonify({"redirect": "/error"}), 500
    return render_template("create.html")


@app.route('/profile/admin/edit', methods=['POST'])
def edit():
    if session.get("username", None) != "admin":
        return jsonify({"redirect": "/error"}), 500
    if request.data:
        try:
            data = json.loads(request.data)
            if "message" not in data or "status" not in data:
                return jsonify({"redirect": "/error"}), 500

            message = data["message"]
            status = data["status"]

            Msg = Message(_message=message, _status=status)
            MsgManager.Store(message=Msg)

            return jsonify({"redirect": "1"}), 200
        except Exception:
            return jsonify({"redirect": "/error"}), 500
    else:
        return jsonify({"redirect": "/error"}), 500


@app.route('/profile/<username>/view/api', methods=['GET'])
def _view(username=None):
    if session.get("username", None) != username:
        return jsonify({"redirect": "/error"}), 500
    try:
        result = MsgManager.Show()

        return jsonify({"data": result}), 200
    except:
        return jsonify({"redirect": "/error"}), 500


@app.route('/profile/<username>/view', methods=['GET'])
def view(username=None):
    if session.get("username", None) != username:
        return jsonify({"redirect": "/error"}), 500
    try:
        return render_template("view.html", username=username)
    except:
        return jsonify({"redirect": "/error"}), 500


@app.route('/error')
def error():
    return render_template("error.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
