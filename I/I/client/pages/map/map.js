const { ipcRenderer } = require("electron");
var customerName = document.querySelector("#customerName");
var lat = document.querySelector("#lat");
var lng = document.querySelector("#lng");
var addCargo = document.querySelector("#addCargo");

var markers = [];
var adjacencyMatrix = [];
var startPoint;

var directionsService, directionsRenderer, geocoder;

var map, tempMarker;

addCargo.addEventListener("click", () => {
    if (customerName.value != "" && lat.value != "" && lng.value != "")
        geocoder.geocode({ latLng: new google.maps.LatLng(parseFloat(lat.value), parseFloat(lng.value)) }, (responses) => {
            if (responses && responses.length > 0) {
                ipcRenderer.send("addCargo", JSON.stringify({
                    customerName: customerName.value,
                    address: responses[0].formatted_address,
                    lat: parseFloat(lat.value),
                    lng: parseFloat(lng.value)
                }));
            }
        });
});

var query = 0;

function addMarker(cargo, calculate) {

    var marker = new google.maps.Marker({
        position: new google.maps.LatLng(cargo.lat, cargo.lng),
        map: map
    });

    markers[cargo.id] = marker;

    adjacencyMatrix[cargo.id] = []

    markers.forEach((target, i) => {
        adjacencyMatrix[cargo.id][i] = 0;
        if (!adjacencyMatrix[i])
            adjacencyMatrix[i] = []

        if (i != cargo.id) {

            setTimeout(() => {
                const route = {
                    origin: new google.maps.LatLng(marker.getPosition().lat(), marker.getPosition().lng()),
                    destination: new google.maps.LatLng(target.getPosition().lat(), target.getPosition().lng()),
                    travelMode: 'WALKING'
                };
                directionsService.route(route, (response, status) => {
                    if (status == 'OK') {
                        adjacencyMatrix[cargo.id][i] = parseFloat(response.routes[0].legs[0].distance.value);
                        adjacencyMatrix[i][cargo.id] = parseFloat(response.routes[0].legs[0].distance.value);
                        query--;
                        if (query == 0)
                            document.querySelector("#map").setAttribute("class", "");
                    }
                });
            }, query * 1000);
            query++;
            if (query != 0)
                document.querySelector("#map").setAttribute("class", "loading");
        }
    });

    if (calculate) {
        setTimeout(calculateShortestPath, query * 1000);
    }

};

ipcRenderer.on("addAllCargosToMap", (e, cargos) => {
    cargos = JSON.parse(cargos);
    cargos.forEach((cargo) => {
        addMarker(cargo);
    });
});

ipcRenderer.on("addCargo", (e, cargo) => {
    addMarker(JSON.parse(cargo), true);
});

ipcRenderer.on("removeCargo", (e, id) => {
    markers[id].setMap(null);
    delete markers[id];
    calculateShortestPath();
});

ipcRenderer.on("updateStartPoint", (err, newStartPointID) => {
    startPoint = newStartPointID;
    calculateShortestPath();
})

ipcRenderer.on("updateStatus", (err, newStatus) => {
    newStatus = JSON.parse(newStatus);
    console.log("önce", markers[newStatus.id].getMap());
    if (markers[newStatus.id].getMap() && !newStatus.status) {
        markers[newStatus.id].setMap(null);
        calculateShortestPath();
    } else if (!markers[newStatus.id].getMap() && newStatus.status) {
        markers[newStatus.id].setMap(map);
        calculateShortestPath();
    }
    console.log("sonra", markers[newStatus.id].getMap());

})

function initMap() {

    map = new google.maps.Map(document.getElementById("map"), {
        center: new google.maps.LatLng(39.925533, 32.866287),
        zoom: 4
    });

    google.maps.event.addListener(map, "click", (event) => {
        if (tempMarker == null) {
            tempMarker = new google.maps.Marker({
                position: event.latLng,
                map: map,
                draggable: true
            });
            tempMarker.addListener("click", () => {
                tempMarker.setMap(null);
            });
        } else {
            tempMarker.setPosition(event.latLng);
            tempMarker.setMap(map);
        }

        lat.value = event.latLng.lat();
        lng.value = event.latLng.lng();
    });

    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer({
        suppressMarkers: true,
        map: map
    });
    geocoder = new google.maps.Geocoder();

};

function calculateShortestPath() {

    if (!startPoint && !markers[startPoint].getMap())
        return;

    var shortestPathIDs = [];
    markers.forEach((element, index) => {
        if (element.getMap())
            shortestPathIDs.push(index);
    });

    var paths = permutations(shortestPathIDs);

    paths = paths.filter(x => x[0] == startPoint);
    var shortestPath = [];
    var min_cost = Number.MAX_SAFE_INTEGER;

    paths.forEach((path) => {
        var cost = 0;
        path.forEach(function(current, index) {
            var next = path[index + 1];
            if (index < path.length - 2) {
                cost = cost + adjacencyMatrix[current][next];
            }
        });
        if (cost != 0 && cost <= min_cost) {
            min_cost = cost;
            shortestPath = [];
            path.forEach(element => {
                shortestPath.push(element);
            });
        };
    });

    var route = {
        origin: "",
        destination: "",
        waypoints: [],
        optimizeWaypoints: true,
        travelMode: "WALKING",
    };

    shortestPath.forEach((id, index) => {
        var marker = markers[id];
        if (index == 0)
            route.origin = new google.maps.LatLng(marker.getPosition().lat(), marker.getPosition().lng());
        else if (index == shortestPath.length - 1)
            route.destination = new google.maps.LatLng(marker.getPosition().lat(), marker.getPosition().lng());
        else
            route.waypoints.push({
                location: marker.getPosition().lat() + ", " + marker.getPosition().lng(),
                stopover: true
            });
    });

    directionsService.route(route, (response, status) => {
        if (status == "OK") {
            directionsRenderer.setMap(null);
            //directionsRenderer.setPanel(null); //dene bi bunsuz oluyo mu
            directionsRenderer = new google.maps.DirectionsRenderer({
                suppressMarkers: true,
                map: map
            });
            directionsRenderer.setDirections(response);
            query--;
        }
    });

}

function permutations(nums) {
    var result = [];
    if (nums.length === 0) return [];
    if (nums.length === 1) return [nums];
    for (var i = 0; i < nums.length; i++) {
        const currentNum = nums[i];
        const remainingNums = nums.slice(0, i).concat(nums.slice(i + 1));
        const remainingNumsPermuted = permutations(remainingNums);
        for (var j = 0; j < remainingNumsPermuted.length; j++) {
            const permutedArray = [currentNum].concat(remainingNumsPermuted[j]);
            result.push(permutedArray);
        }
    }
    return result;
}