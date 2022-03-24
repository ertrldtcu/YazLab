from app.models import *
from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit

# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config["SECRET_KEY"] = "thiskeyissosecret"
socketio = SocketIO(app)


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login_page():
    if "username" in session:
        return redirect(url_for("main_page"))

    if "trycounter" in session and session["trycounter"] >= 3:
        return render_template("login.html", alertmsg="3 defa başarısız giriş yapmışsınız!")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if login(username, password):
            session["username"] = username
            set_logged_in(username)
            return redirect(url_for("main_page"))
        else:
            session["trycounter"] = session["trycounter"] + 1 if "trycounter" in session else 1
            return render_template("login.html", alertmsg="Girdiğiniz bilgiler hatalı!")

    session.permanent = False

    return render_template("login.html", alertmsg="false")


@app.route("/main", methods=["GET", "POST"])
def main_page():

    if "username" not in session:
        return redirect(url_for("login_page"))

    if request.method == 'POST':
        if "logout" in request.form:
            set_logged_out(session["username"])
            if "username" in session:
                del session["username"]
            if "trycounter" in session:
                del session["trycounter"]
            return redirect(url_for("login_page"))

    return render_template("main.html", cars=get_user_cars(session["username"]), username=session["username"])


app.run(debug=True)
socketio.run(app)


@socketio.on("get_car_dates")
def get_car_dates(carid):
    emit("send_car_dates", {
        "id": carid,
        "date_start": get_car_first_date(carid),
        "date_end": get_car_last_date(carid)
    })


@socketio.on("get_car_rotate")
def get_car_dates(datas):
    emit("send_car_rotate",
         {"carid": datas["carid"], "locs": get_car_data(datas["carid"], datas["date_start"], datas["date_end"])})
