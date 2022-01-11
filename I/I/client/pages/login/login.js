const { ipcRenderer } = require("electron");
const http = require('http');

var server = {
    hostname: "137.117.197.64",
    port: 8080,
    path: "/",
    method: "GET",
}

document.querySelector("#signin").onclick = () => {

    if (document.querySelector("#username").value == "") return;
    if (document.querySelector("#password").value == "") return;

    server.path = encodeURI("/login?username=" + document.querySelector("#username").value + "&password=" + document.querySelector("#password").value);

    const req = http.request(server, (res) => {

        res.on("data", (data) => {
            ipcRenderer.send("loginsuccess", JSON.stringify(JSON.parse(data)));
        });

    });

    req.end();
}

document.querySelector("#exit").addEventListener("click", () => {
    console.log("asd");
    ipcRenderer.send("exit");
});