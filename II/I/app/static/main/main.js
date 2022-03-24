let infoID = document.querySelector("#infoID")
let date_start = document.querySelector("#date_start")
let date_end = document.querySelector("#date_end")
const socket = io.connect('http://127.0.0.1:5000');
let map;


function show_on_information(event) {
    let id;
    if (typeof event.target.value == "undefined")
        id = event.target.parentNode.value
    else
        id = event.target.value
    socket.emit("get_car_dates", id)
}

function show_on_map() {
    const id = infoID.value
    if (id === undefined)
        return alert("Lütfen araç seçiniz!")

    let start = date_start.value
    let end = date_end.value
    if (start.length === 0 || end.length === 0)
        return alert("Lütfen tüm tarihleri seçiniz!")

    start = start.replace("T", " ")
    end = end.replace("T", " ")

    socket.emit("get_car_rotate", {
        "carid": id,
        "date_start": start,
        "date_end": end
    })

}

const date_info = document.querySelector("#date_info");
socket.on('send_car_dates', dates => {

    date_info.innerHTML = dates["date_start"] + " <> " + dates["date_end"]
    date_start.value = dates["date_end"].replace(" ", "T")
    date_start.stepDown(30)
    date_end.value = dates["date_end"].replace(" ", "T")

    infoID.innerHTML = "#" + dates["id"]
    infoID.value = dates["id"]

    socket.emit("get_car_rotate", {
        "carid": dates["id"],
        "date_start": date_start.value.replace("T", " "),
        "date_end": dates["date_end"]
    })
});

markers = []

socket.on('send_car_rotate', data => {

    markers.forEach((v, index) => {
        if (v["id"] === data["carid"])
            v["marker"].setMap(null)
    })


    let markerImage = {  // https://developers.google.com/maps/documentation/javascript/reference/marker#MarkerLabel
        path: "M12,11.5A2.5,2.5 0 0,1 9.5,9A2.5,2.5 0 0,1 12,6.5A2.5,2.5 0 0,1 14.5,9A2.5,2.5 0 0,1 12,11.5M12,2A7,7 0 0,0 5,9C5,14.25 12,22 12,22C12,22 19,14.25 19,9A7,7 0 0,0 12,2Z",
        anchor: new google.maps.Point(12, 17),
        fillOpacity: 1,
        fillColor: "#" + Math.floor(Math.random() * 16777215).toString(16),
        strokeWeight: 1,
        strokeColor: "#000000",
        scale: 1,
        labelOrigin: new google.maps.Point(12, 15)
    };
    data["locs"].forEach((loc, index) => {
        // lat lang: loc[0], loc[1]
        let marker = new google.maps.Marker({
            position: new google.maps.LatLng(loc[0], loc[1]),
            icon: markerImage,
            map
        });
        markers.push({
            "id": data["carid"],
            "marker": marker
        })
    })

});

/* GOOGLE MAP */
function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: {lat: 59.27101964642515, lng: 17.088348218417405},
        zoom: 8,
    });
    Array.from(document.getElementsByClassName("show_on_information")).forEach(
        function (element, index, array) {
            socket.emit("get_car_dates", element.value)
        }
    );
}
