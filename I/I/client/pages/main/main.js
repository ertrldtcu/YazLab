var list = document.querySelector("#list");
const electron = require("electron");
const {
    ipcRenderer
} = electron;

ipcRenderer.on("addAllCargosToMain", (e, cargos) => {
    cargos = JSON.parse(cargos);
    console.log(cargos);
    cargos.forEach(cargo => {
        addCargo(cargo);
    });
});

ipcRenderer.on("addCargo", (e, cargo) => {
    addCargo(JSON.parse(cargo));
});

function addCargo(cargo) {
    console.log(cargo);
    var item = document.createElement("li");
    item.id = "li" + cargo.id;

    var cargoid = document.createElement("div");
    cargoid.setAttribute("class", "IDli");
    cargoid.innerHTML = "#" + cargo.id;
    item.appendChild(cargoid);

    var customerName = document.createElement("div");
    customerName.setAttribute("class", "customerli");
    customerName.innerHTML = cargo.customerName + " <i style=\"font-size:12px;\"> (" + cargo.address + ") </i>";
    item.appendChild(customerName);

    var location = document.createElement("div");
    location.setAttribute("class", "locationli");
    location.innerHTML = cargo.lat + "," + cargo.lng;
    item.appendChild(location);

    var status = document.createElement("input");
    status.setAttribute("type", "checkbox")
    status.setAttribute("checked", "")
    status.setAttribute("class", "statusli");
    item.appendChild(status);
    status.addEventListener("click", () => {
        ipcRenderer.send("updateStatus", JSON.stringify({
            id: cargo.id,
            status: status.checked
        }));
    });

    var startPoint = document.createElement("input");
    startPoint.setAttribute("type", "radio")
    startPoint.setAttribute("name", "startPoint")
    startPoint.setAttribute("class", "startPointli");
    item.appendChild(startPoint);

    var deleteButton = document.createElement("button");
    deleteButton.setAttribute("class", "deleteButton");
    var img = document.createElement("img");
    img.setAttribute("src", "remove.png");
    deleteButton.appendChild(img);
    item.appendChild(deleteButton);
    deleteButton.addEventListener("click", () => {
        list.removeChild(item);
        ipcRenderer.send("removeCargo", cargo.id)
    });

    startPoint.addEventListener("change", () => {
        ipcRenderer.send("updateStartPoint", cargo.id);
    })





    list.appendChild(item);
};