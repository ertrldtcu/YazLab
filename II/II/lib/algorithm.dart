import "dart:math";
import 'package:cloud_firestore/cloud_firestore.dart';

FirebaseFirestore fs = FirebaseFirestore.instance;
CollectionReference stationsRef = fs.collection('stations');

List busCapacities = [25, 30, 40, 25];

// [ INT stationid, String "durak ismi", double lat, double lng, int yolcu_sayisi ],
List stations = [];

Future<void> getData() async {
  var querySnapshot = await stationsRef.get();
  for (var doc in querySnapshot.docs) {
    stations.add([
      doc.get("id"),
      doc.get("name"),
      doc.get("lat"),
      doc.get("lng"),
      doc.get("passengerCount")
    ]);
    visited.add(doc.get("passengerCount") == 0);
  }
}

double distance(lat1, lon1, lat2, lon2) {
  var p = 0.017453292519943295;
  var a = 0.5 -
      cos((lat2 - lat1) * p) / 2 +
      cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2;
  return 12742 * asin(sqrt(a));
}

List adjacencyMatrix = [];
//  e.g: [ 0_to_1, 0_to_2, ... ]

void fillAdjacencyMatrix() {
  for (int i = 0; i < stations.length; i++) {
    adjacencyMatrix.add([]);
    for (int j = 0; j < stations.length; j++) {
      if (i == j) {
        adjacencyMatrix[i].add(0);
      } else if (i > j) {
        adjacencyMatrix[i].add(adjacencyMatrix[j][i]);
      } else {
        adjacencyMatrix[i].add(distance(
            stations[i][2], stations[i][3], stations[j][2], stations[j][3]));
      }
    }
  }
}

List<bool> visited = [];

List<List> calculatePath() {

  while (totalPassengerCount() > totalCapacity()) {
    busCapacities.add(25);
  }

  fillAdjacencyMatrix();

  List<List> path = [];

//   List<int>

  for (int bus = 0; bus < busCapacities.length; bus++) {
    path.add([]);

    for (int i = 0; i < visited.length; i++) {
      if (!visited[i]) {
        path[bus].add(i);
        visited[i] = true;
        busCapacities[bus] -= int.parse(stations[i][4].toString());
        break;
      }
    }

    int nearestStationID = -1;
    do {
      nearestStationID = getNearestStation(
          path[bus][path[bus].length - 1], busCapacities[bus]);
      if (nearestStationID != -1) {
        busCapacities[bus] -= int.parse(stations[nearestStationID][4].toString());
        visited[nearestStationID] = true;
        path[bus].add(nearestStationID);
      } else {
        break;
      }
    } while (!isAllStationsVisited() && busCapacities[bus] > 0);
  }

  return path;
}

bool isAllStationsVisited() {
  for (int i = 0; i < visited.length; i++) {
    if (!visited[i]) {
      return false;
    }
  }
  return true;
}

bool canBusTakeMorePassenger(int busid) {
  for (int i = 0; i < visited.length; i++) {
    if (!visited[i] && int.parse(stations[i][4].toString())<= busCapacities[busid]) {
      return true;
    }
  }
  return false;
}

int getNearestStation(int stationid, int capacity) {
  print("stationid: $stationid capacity: $capacity");
  int nearestStation = -1;
  double nearestDistance = double.infinity;

  for (int j = 0; j < adjacencyMatrix.length; j++) {
    if (stationid != j &&
        !visited[j] &&
        adjacencyMatrix[stationid][j] < nearestDistance &&
        stations[j][4] <= capacity) {
      nearestStation = j;
      nearestDistance = adjacencyMatrix[stationid][j];
    }
  }

  return nearestStation;
}

int totalPassengerCount() {
  int c = 0;
  for (int i = 0; i < stations.length; i++) {
    c += int.parse(stations[i][4].toString());
  }
  return c;
}

int totalCapacity() {
  int c = 0;
  for (int i = 0; i < busCapacities.length; i++) {
    c += int.parse(busCapacities[i].toString());
  }
  return c;
}
