from flask import Flask, render_template, request, jsonify, send_file, session
from flask_sqlalchemy import SQLAlchemy
import os
import logging
from textprocessing import *

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

DB_NAME = "database.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = "thiskeyissosecret"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    is_admin = db.Column(db.Integer)


class files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(255), nullable=False)
    file = db.Column(db.LargeBinary(), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    students = db.Column(db.String(255))
    date = db.Column(db.String(255))
    period = db.Column(db.String(255))
    keywords = db.Column(db.String(255))
    lesson = db.Column(db.String(255))
    title = db.Column(db.String(255))
    teachers = db.Column(db.String(255))
    juries = db.Column(db.String(255))
    summary = db.Column(db.String(255))


def downloadFile ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    path = "/Examples.pdf"
    return send_file(path, as_attachment=True)

@app.route("/")
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        search = users.query.filter_by(username=username, password=password).first()

        if search == None:
            return jsonify({"message":"Hesap bulunamadı!"})
        else:
            session.permanent = False
            session["id"] = search.id
            session["is_admin"] = search.is_admin or 0
            session["username"] = username
            if search.is_admin == 1:
                return jsonify({"redirect":"admin"})
            else:
                return jsonify({"redirect":"home"})

    return render_template("login.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == 'POST':
        print(request.form)
        if "adduserbutton" in request.form:
            username = request.form.get("username")
            password = request.form.get("password")
            newuser = users(username=username, password=password)
            db.session.add(newuser)
            db.session.commit()
        elif "file_id" in request.form:
            file = files.query.filter_by(id=int(request.form.get("file_id"))).first()
            print(file)
            if file is not None:
                f = open(file.name, "wb")
                f.write(file.file)
                f.close()            
            return send_file(file.name, as_attachment=True)
        elif "remove_user_id" in request.form:
            deluser = users.query.filter_by(id=request.form.get("remove_user_id")).first()
            user_files = files.query.filter_by(user_name=deluser.username)
            for file in user_files:
                db.session.delete(file)
            db.session.delete(deluser)
            db.session.commit()


    allusers = users.query.all()
    allfiles = files.query.all()
    return render_template("admin.html", users=allusers, files=allfiles)

@app.route("/home", methods=["GET", "POST"])
def userpage():
    if "id" not in session:
        return render_template("login.html")
    else:
        if session["is_admin"]:
            return render_template("admin.html", users=users.query.all(), files=files.query.all())
    if request.method == "POST":
        if request.files.get("file"):
            print(request.files.get("file").filename)
            if request.files.get("file").filename == '':
                return "Dosya seçiniz."
            file = request.files.get('file')
            data = file.read()

            f = open(file.filename, "wb")
            f.write(data)
            f.close()
            pdfstr = read_pdf(file.filename)
            os.remove(file.filename)

            student = ""
            numbers = find_students_number(pdfstr)
            for i,s in enumerate(find_students_name(pdfstr)):
                student += s + " " + numbers[i] + " " + ("1" if numbers[i][5] == "1" else "2") + ". Öğretim\n"

            delivery_date = find_date(pdfstr)
            period = find_period(delivery_date)
            keywords = find_keywords(pdfstr)
            lesson = find_lesson(pdfstr)
            title = find_title(pdfstr, lesson)
            teachers = find_teachers(pdfstr)
            juries = find_juries(pdfstr)
            summary  = find_summary(pdfstr)

            newfile = files(
                user_name = session["username"],
                file = data,
                name = file.filename,
                students = student,
                date = delivery_date,
                period = period,
                keywords = keywords,
                lesson = lesson,
                title = title,
                teachers = teachers,
                juries = juries,
                summary = summary
            )
            db.session.add(newfile) 
            db.session.commit()
        elif "file_id" in request.form:
            file = files.query.filter_by(id=int(request.form.get("file_id"))).first()
            print(file)
            if file is not None:
                f = open(file.name, "wb")
                f.write(file.file)
                f.close()            
            return send_file(file.name, as_attachment=True)
        

    allfiles = files.query.filter_by(user_name=session["username"])
    return render_template("user.html", files=allfiles)


if __name__ == "__main__":

    if not os.path.exists(DB_NAME):
        db.create_all()

    app.run(debug=True)
