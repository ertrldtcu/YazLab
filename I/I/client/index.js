const { app, BrowserWindow, ipcMain, webContents } = require("electron");
const path = require("path");
const http = require('http');

let mapWindow, mainWindow, userID;

var server = {
    hostname: "137.117.197.64",
    port: 8080,
    path: "/",
    method: "GET",
}


app.on("ready", () => {

    mainWindow = new BrowserWindow({
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            enableRemoteModule: true
        },
        width: 1080,
        height: 720,
        show: false,
        //resizable: false,
        //frame: false,
        //transparent: true
    });

    mainWindow.openDevTools();
    mainWindow.once('ready-to-show', function() {
        mainWindow.show()
            // mainWindow.openDevTools();
    });

    mainWindow.on("close", function() {
        app.exit(1);
    })

    mainWindow.loadFile(path.join(__dirname, "pages/login/login.html"))

    mainWindow.center();
    mainWindow.removeMenu();

    ipcMain.on("exit", () => {
        app.exit(1);
    })

    ipcMain.on("loginsuccess", (err, data) => {
        data = JSON.parse(data);
        userID = data.userID;

        mainWindow.loadFile(path.join(__dirname, "pages/main/main.html"));

        mapWindow = new BrowserWindow({
            webPreferences: {
                nodeIntegration: true,
                contextIsolation: false,
                enableRemoteModule: true
            },
            show: false
        });
        mapWindow.openDevTools();

        mapWindow.once('ready-to-show', function() {
            mapWindow.show();
            mainWindow.webContents.send("addAllCargosToMain", JSON.stringify(JSON.parse(data.cargos)));
            mapWindow.webContents.send("addAllCargosToMap", JSON.stringify(JSON.parse(data.cargos)))
        });
        mapWindow.loadFile(path.join(__dirname, "pages/map/map.html"));

    });

    ipcMain.on("addCargo", function(error, cargo) {
        server.path = encodeURI("/addCargo?userID=" + userID + "&cargo=" + cargo);

        const req = http.request(server, (res) => {

            res.on("data", (cargoID) => {
                cargo = JSON.parse(cargo);
                console.log(typeof cargoID, cargoID);
                cargo.id = parseInt(cargoID);
                mainWindow.webContents.send('addCargo', JSON.stringify(cargo));
                mapWindow.webContents.send('addCargo', JSON.stringify(cargo));
            });

        });

        req.end();
    });

    ipcMain.on("removeCargo", (e, cargoID) => {
        server.path = "/removeCargo?userID=" + userID + "&cargoID=" + cargoID;
        mapWindow.webContents.send("removeCargo", cargoID);
        const req = http.request(server, function(res) {})
        req.end();
    });

    ipcMain.on("updateStartPoint", (err, newStartPointID) => {
        mapWindow.webContents.send("updateStartPoint", newStartPointID);
    })

    ipcMain.on("updateStatus", (err, newStatus) => {
        mapWindow.webContents.send("updateStatus", newStatus);

        newStatus = JSON.parse(newStatus);

        server.path = encodeURI("/updateCargoStatus?cargoID=" + newStatus.id + "&newStatus=" + newStatus.status);

        const req = http.request(server, (res) => {});
        req.end();

    })

});