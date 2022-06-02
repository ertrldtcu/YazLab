const socket = io.connect('http://127.0.0.1:5000');
const author = document.getElementById("author");
const name = document.getElementById("name");
const year = document.getElementById("year");
const list = document.getElementById("list");

function search() {
    if (author.value === "")
        return alert("Araştırmacı seçiniz!");
    if (name.value === "")
        return alert("Yayın adı seçiniz!");
    if (year.value === "")
        return alert("Yayın yılı seçiniz!");

    socket.emit("SearchRequest", {
        "author": author.value,
        "title": name.value,
        "year": year.value
    });

    list.innerHTML = ""
}

socket.on("SearchResponse", (response) => {
    if (response.length === 0) {
        return alert("Sonuç bulunamadı!");
    }
    for (let i = 0; i < response.length; i++) {

        const v = response[i]

        const item = document.createElement("div");
        item.setAttribute("class", "publication");

        const id = document.createElement("div");
        id.setAttribute("class", "ID");
        id.innerHTML = "#" + v[0];
        item.appendChild(id);

        for(let j = 1; j < 6; j++) {
            var elm = document.createElement("div");
            elm.innerHTML = v[j];
            item.appendChild(elm);
        }

        list.appendChild(item);
    }
})


