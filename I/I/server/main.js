const mysql = require("mysql");
const { login } = require("./login.js");
const { register } = require("./register.js");
const { addCargo, removeCargo, updateCargoStatus } = require("./cargo.js");

var db = mysql.createConnection({
    host: "localhost",
    user: "root",
    pass: ""
});

const express = require('express');
const app = express();

app.listen(8080, (err) => {
    if (err) throw err;
    console.log("Sunucu başlatıldı, 8080 Port'u dinleniyor.");
});

app.get("/login", (req, res) => {
    login(db, decodeURI(req.query.username), decodeURI(req.query.password), res);
});

app.get("/register", (req) => {
    register(db, decodeURI(req.query.username), decodeURI(req.query.password));
});

app.get("/addCargo", (req, res) => {
    addCargo(db, decodeURI(req.query.userID), JSON.parse(decodeURI(req.query.cargo)), res);
});

app.get("/removeCargo", (req) => {
    removeCargo(db, req.query.cargoID);
});

app.get("/updateCargoStatus", (req) => {
    updateCargoStatus(db, req.query.cargoID, req.query.newStatus != "true")
})

db.connect((err) => {

    if (err) throw err;

    var createDB = "CREATE DATABASE yazlab";
    db.query(createDB, (err) => {
        if (!err)
            console.log("Veritabanı olmadığı için oluşturuldu.");
    });

    var use = "USE yazlab";
    db.query(use, () => {
        console.log("Veritabanına erişim sağlandı.");
    });

    var usersTable = "CREATE TABLE users (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, username VARCHAR(32) NOT NULL, password VARCHAR(32) NOT NULL)";

    db.query(usersTable, (err) => {
        if (err) console.log("Kullanıcılar tablosuna erişim sağlandı.");
        else console.log("Kullanıcılar tablosu olmadığı için oluşturuldu.");
    });

    var cargosTable = "CREATE TABLE cargos (" +
        "id INT PRIMARY KEY NOT NULL AUTO_INCREMENT," +
        "userID INT NOT NULL," +
        "customerName VARCHAR(32) NOT NULL," +
        "address VARCHAR(100) NOT NULL," +
        "lat DOUBLE NOT NULL," +
        "lng DOUBLE NOT NULL," +
        "status BIT(1)" +
        ")";
    db.query(cargosTable, (err) => {
        if (err) console.log("Kargolar tablosuna erişim sağlandı.");
        else console.log("Kargolar tablosu olmadığı için oluşturuldu.");
    });

});