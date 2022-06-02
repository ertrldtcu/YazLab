import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';
import 'package:routeplanning/GradientButton.dart';
import 'package:flutter_polyline_points/flutter_polyline_points.dart';
import '../MainBackground.dart';
import '../algorithm.dart';

class MapPage extends StatefulWidget {
  const MapPage({Key? key}) : super(key: key);

  @override
  State<MapPage> createState() => _MapPageState();
}

class _MapPageState extends State<MapPage> {
  PolylinePoints polylinePoints = PolylinePoints();
  Map<PolylineId, Polyline> polylines = {};
  double _originLatitude = 40.8244526;
  double _originLongitude = 29.9240807;
  double _destLatitude = 40.7881197;
  double _destLongitude = 29.9736694;

  @override
  void initState() {
    super.initState();
    _getPolyline();
  }

  void _getPolyline() async {
    await getData();
    List paths = calculatePath();
    _originLatitude = stations[paths[0][0]][2]; //lat
    _originLongitude = stations[paths[0][0]][3]; //lat
    _destLatitude = stations[paths[0][paths[0].length - 1]][2]; //lat
    _destLongitude = stations[paths[0][paths[0].length - 1]][3]; //lat
    List<LatLng> polylineCoordinates = [];

    PolylineResult result = await polylinePoints.getRouteBetweenCoordinates(
      "AIzaSyCfnzBDKkq8W2992BYLqSsl-nlx6159dpw",
      PointLatLng(_originLatitude, _originLongitude),
      PointLatLng(_destLatitude, _destLongitude),
      wayPoints: [],
      travelMode: TravelMode.driving,
    );
    if (result.points.isNotEmpty) {
      for (var point in result.points) {
        polylineCoordinates.add(LatLng(point.latitude, point.longitude));
      }
    } else {
      print(result.errorMessage);
    }
    _addPolyLine(polylineCoordinates);

    // _originLatitude = 39.8244526;
    // _originLongitude = 29.9240807;
    // _destLatitude = 40.7881197;
    // _destLongitude = 29.9736694;
    // _getPolyline();
  }

  _addPolyLine(List<LatLng> polylineCoordinates) {
    PolylineId id = const PolylineId("poly");
    Polyline polyline = Polyline(
      polylineId: id,
      color: Colors.lightBlueAccent,
      points: polylineCoordinates,
      width: 4,
    );
    polylines[id] = polyline;
    setState(() {});
  }

  _builtMapPage() => SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(10.0),
          child: Column(
            children: <Widget>[
              Expanded(
                child: Padding(
                  padding: const EdgeInsets.all(4.0),
                  child: Container(
                    decoration: const BoxDecoration(
                      color: Colors.black12,
                      borderRadius: BorderRadius.all(Radius.circular(10.0)),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black54,
                          blurRadius: 15,
                          offset: Offset(0, 5),
                        ),
                      ],
                    ),
                    child: Padding(
                      padding: const EdgeInsets.all(2.0),
                      child: ClipRRect(
                        borderRadius:
                            const BorderRadius.all(Radius.circular(10.0)),
                        child: GoogleMap(
                          polylines: Set<Polyline>.of(polylines.values),
                          myLocationButtonEnabled: false,
                          zoomControlsEnabled: false,
                          initialCameraPosition: const CameraPosition(
                              target: LatLng(40.7830182, 29.9557094), zoom: 13),
                        ),
                      ),
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 15),
              const GradientButton(
                text: "Geri Dön",
                color: <Color>[
                  Color(0xFF4527A0),
                  Color(0xFF7E57C2),
                  Color(0xFF2EE2B3),
                ],
              )
            ],
          ),
        ),
      );

  @override
  Widget build(BuildContext context) {
    if (stations.isEmpty) {
      getData();
    }
    return Scaffold(
      body: Center(
        child: Stack(
          children: [
            const MainBackground(),
            _builtMapPage(),
          ],
        ),
      ),
    );
  }
}
