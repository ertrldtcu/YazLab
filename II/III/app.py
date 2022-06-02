import os
import webbrowser

from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from neo4j import GraphDatabase, basic_auth
from xml.etree.ElementTree import parse

DATABASE_USERNAME = 'neo4j'
DATABASE_PASSWORD = 'leap-tunnels-basins'
DATABASE_URL = 'bolt://54.147.6.54:7687'

driver = GraphDatabase.driver(DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, DATABASE_PASSWORD))
sessionx = driver.session()

DB_NAME = "database.db"

app = Flask(__name__)
app.config["SECRET_KEY"] = "thiskeyissosecret"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
socketio = SocketIO(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)


@app.route("/", methods=["GET", "POST"])
@app.route("/main", methods=["GET", "POST"])
def main_page():
    q = """ Match (n:Author) Return distinct n.author """
    r = sessionx.run(q)
    authors = [v["n.author"] for v in r]
    authors.sort()

    q = """ Match (n:Publication) Return distinct n.title """
    r = sessionx.run(q)
    names = [v["n.title"] for v in r]
    names.sort()

    q = """ Match (n:Publication) Return distinct n.year """
    r = sessionx.run(q)
    years = [v["n.year"] for v in r]
    years.sort()

    return render_template("main.html", authors=authors, names=names, years=years)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if "username" in session:
        return redirect(url_for("admin_page"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        search = Users.query.filter_by(mail=username, password=password).first()

        if search is not None:
            session.permanent = False
            session["username"] = username
            return redirect(url_for("admin_page"))

    return render_template("login.html")


@app.route("/admin", methods=["GET", "POST"])
def admin_page():
    if "username" not in session:
        return redirect(url_for("login_page"))

    if "logout" in request.form:
        del session["username"]
        return redirect(url_for("main_page"))

    return render_template("admin.html")


@app.route("/graph", methods=["GET", "POST"])
def graph_page():
    author = request.args["author"]
    title = request.args["title"]
    year = request.args["year"]
    return render_template("graph.html", author=author, title=title, year=year)


@socketio.on("add")
def add(data):
    q = """ Merge(name:Type{type:$type}) """
    sessionx.run(q, {"type": data["type"]})

    title = data["name"]
    year = data["year"]
    journal = data["journal"]
    q = """ Merge(name:Publication{title:$title,year:$year,place:$journal}) """
    sessionx.run(q, {"title": title, "year": year, "journal": journal})

    q = """ Match (a:Type{type:$type}),(b:Publication{title:$title,year:$year,place:$journal}) Merge (b)-[
        :Turudur]->(a) """
    sessionx.run(q, {"type": data["type"], "title": title, "year": year, "journal": journal})

    data["coauthors"].append(data["author"])
    for author in data["coauthors"]:
        q = """ Merge(name:Author{author:$author}) """
        sessionx.run(q, {"author": author})
        q = """Match (a:Author{author:$author}),(b:Publication{title:$title,year:$year,place:$journal}) Merge 
            (a)-[:Yayinladi]->(b) """
        sessionx.run(q, {"author": author, "title": title, "year": year, "journal": journal})
        q = """Match (b:Author{author:$author}),(a:Author{author:$mainauthor}) Merge (a)-[
            :OrtakCalisir]->(b) """
        sessionx.run(q, {"author": author, "mainauthor": data["author"]})

    q = """ Match(a:Author{author:$mainauthor}) Match (a)-[r:OrtakCalisir]->(a) Delete r """
    sessionx.run(q, {"mainauthor": data["author"]})


@socketio.on("SearchRequest")
def _search(data):
    print(data)
    r = sessionx.run(detectquery(data), {"author": data["author"], "title": data["title"], "year": data["year"]})
    result = [v for v in r]
    result.sort()
    socketio.emit("SearchResponse", result)
    if len(result) > 0:
        webbrowser.open(
            "http://127.0.0.1:5000/graph?author=" + data["author"] + "&title=" + data["title"] + "&year=" + data[
                "year"])


def detectquery(data):
    global q
    returnstr = " Return id(y), a.author as author, y.title as title, y.year as year,y.place as place,t.type as type"
    if data["author"] == "tüm araştırmacılar..":
        if data["title"] == "tüm yayınlar..":
            if data["year"] == "tüm yıllar..":
                q = """Match (a:Author)--(y:Publication)--(t:Type)""" + returnstr
            else:
                q = """Match (a:Author)--(y:Publication{year:$year})--(t:Type)""" + returnstr
        else:
            if data["year"] == "tüm yıllar..":
                q = """Match (a:Author)--(y:Publication{title:$title})--(t:Type)""" + returnstr
            else:
                q = """Match (a:Author)--(y:Publication{title:$title,year:$year})--(t:Type)""" + returnstr
    else:
        if data["title"] == "tüm yayınlar..":
            if data["year"] == "tüm yıllar..":
                q = """Match (a:Author{author:$author})--(y:Publication)--(t:Type)""" + returnstr
            else:
                q = """Match (a:Author{author:$author})--(y:Publication{year:$year})--(t:Type)""" + returnstr
        else:
            if data["year"] == "tüm yıllar..":
                q = """Match (a:Author{author:$author})--(y:Publication{title:$title})--(t:Type)""" + returnstr
            else:
                q = """Match (a:Author{author:$author})--(y:Publication{title:$title,year:$year})--(t:Type)""" + returnstr
    return q


def LoadExampleXML(xmlname):
    root = parse("ExampleXML/" + xmlname).getroot()
    mainauthor = root.find("./person").find("./author").text
    print(mainauthor, "yükleniyor...")

    for r in root.findall("./r"):
        article = r.find("./article")
        inproceedings = r.find("./inproceedings")
        node = article if article is not None else inproceedings
        type = "Article" if article is not None else "Inproceeding"
        journal = "./journal" if article is not None else "./booktitle"

        q = """ Merge(name:Type{type:$type}) """
        sessionx.run(q, {"type": type})

        title = node.find("./title").text
        year = node.find("./year").text
        journal = node.find(journal).text
        q = """ Merge(name:Publication{title:$title,year:$year,place:$journal}) """
        sessionx.run(q, {"title": title, "year": year, "journal": journal})

        q = """Match (a:Type{type:$type}),(b:Publication{title:$title,year:$year,place:$journal}) Merge (b)-[
        :Turudur]->(a) """
        sessionx.run(q, {"type": type, "title": title, "year": year, "journal": journal})

        for author in node.findall("./author"):
            author = author.text
            q = """ Merge(name:Author{author:$author}) """
            sessionx.run(q, {"author": author})
            q = """Match (a:Author{author:$author}),(b:Publication{title:$title,year:$year,place:$journal}) Merge 
            (a)-[:Yayinladi]->(b) """
            sessionx.run(q, {"author": author, "title": title, "year": year, "journal": journal})
            q = """Match (b:Author{author:$author}),(a:Author{author:$mainauthor}) Merge (a)-[
            :OrtakCalisir]->(b) """
            sessionx.run(q, {"author": author, "mainauthor": mainauthor})

    q = """ Match(a:Author{author:$mainauthor}) Match (a)-[r:OrtakCalisir]->(a) Delete r """
    sessionx.run(q, {"mainauthor": mainauthor})
    print(mainauthor, "yüklendi.")


if __name__ == "__main__":
    if not os.path.exists(DB_NAME):
        db.create_all()
    app.run(debug=True)
    socketio.run(app)

# LoadExampleXML("ahmetsayar.xml")
# LoadExampleXML("fulyaakdeniz.xml")
# LoadExampleXML("yasarbecerikli.xml")
