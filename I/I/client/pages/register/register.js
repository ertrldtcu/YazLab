const { ipcRenderer } = require("electron");
const http = require('http');

var server = {
    hostname: "137.117.197.64",
    port: 8080,
    path: "/",
    method: "GET",
}

document.querySelector("#signup").onclick = () => {

    if (document.querySelector("#username").value == "") return;
    if (document.querySelector("#password").value == "") return;
    if (document.querySelector("#repassword").value == "") return;
    if (document.querySelector("#password").value != document.querySelector("#repassword").value) return;
    server.path = encodeURI("/register?username=" + document.querySelector("#username").value + "&password=" + document.querySelector("#password").value);

    const req = http.request(server, (res) => {});

    req.end();

}

document.querySelector("#exit").addEventListener("click", () => {
    console.log("asd");
    ipcRenderer.send("exit");
});