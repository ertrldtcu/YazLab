const socket = io.connect('http://127.0.0.1:5000');
const author = document.getElementById("author");
const name = document.getElementById("name");
const year = document.getElementById("year");
const journal = document.getElementById("journal");
const type = document.getElementById("type");
const coauthor1 = document.getElementById("coauthor1");
const coauthor2 = document.getElementById("coauthor2");
const coauthor3 = document.getElementById("coauthor3");

function add() {

    if (author.value === "") return alert("Araştırmacı adı giriniz!");
    if (name.value === "") return alert("Yayın adı giriniz!");
    if (year.value === "") return alert("Yayın yılı giriniz!");
    if (journal.value === "") return alert("Yayın yeri giriniz!");
    if (type.value === "") return alert("Tür giriniz!");

    socket.emit("add", {
        "author": author.value,
        "name": name.value,
        "year": year.value,
        "journal": journal.value,
        "type": type.value,
        "coauthors": [coauthor1.value, coauthor2.value, coauthor3.value].filter(v => v !== "")
    });

}
