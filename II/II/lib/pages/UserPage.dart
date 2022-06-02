import 'package:flutter/material.dart';
import 'package:routeplanning/GradientButton.dart';
import '../MainBackground.dart';
import 'package:cloud_firestore/cloud_firestore.dart';

FirebaseFirestore fs = FirebaseFirestore.instance;
CollectionReference stationsRef = fs.collection('stations');
CollectionReference users_stationsRef = fs.collection('users_stations');

class UserPage extends StatefulWidget {
  final int userid;

  const UserPage({Key? key, this.userid = -1}) : super(key: key);

  @override
  State<UserPage> createState() => _UserPageState();
}

class _UserPageState extends State<UserPage> {
  List busStations = [];
  List stationIDs = [];

  String? dropdownValue;
  String _groupValue = "-1";

  void getData() async {
    // Get docs from collection reference
    var querySnapshot = await stationsRef.get();
    for (var doc in querySnapshot.docs) {
      busStations.add(doc.get("name"));
      stationIDs.add(doc.get("id"));
      setState(() {});
    }
  }

  void saveStation() async {
    int stationIndex = int.parse(_groupValue);
    if (stationIndex == -1) {
      return showDialog(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text('Hata'),
          content: const Text('Lütfen bir durak seçiniz.'),
          actions: <Widget>[
            FlatButton(
              onPressed: () {
                Navigator.of(context, rootNavigator: true)
                    .pop(); // dismisses only the dialog and returns nothing
              },
              child: const Text('OK'),
            ),
          ],
        ),
      );
    }
    users_stationsRef
        .where("users", isEqualTo: widget.userid)
        .get()
        .then((value) => print(value.size));
  }

  void _handleRadioValueChange(String? value) {
    setState(() {
      _groupValue = value.toString();
    });
  }

  _builtListItem(context, index) => GestureDetector(
        onTap: () => setState(() {
          _handleRadioValueChange(index.toString());
        }),
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 8.0, vertical: 4.0),
          child: Container(
            decoration: const BoxDecoration(
              color: Color(0x40FFFFFF),
              boxShadow: [
                BoxShadow(
                  color: Color(0x30000000),
                  blurRadius: 4,
                  offset: Offset(0, 0),
                ),
              ],
              borderRadius: BorderRadius.all(Radius.circular(50.0)),
            ),
            child: Row(
              children: [
                Radio(
                  value: index.toString(),
                  groupValue: _groupValue,
                  onChanged: _handleRadioValueChange,
                  activeColor: const Color(0xFFFF5C00),
                ),
                Text(
                  busStations[index],
                  style: const TextStyle(
                      fontSize: 20.0, fontWeight: FontWeight.w600),
                ),
              ],
            ),
          ),
        ),
      );

  _builtUserPage() => SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(28.0),
          child: Column(
            children: <Widget>[
              Expanded(
                child: ListView.builder(
                  itemCount: busStations.length,
                  itemBuilder: (context, index) =>
                      _builtListItem(context, index),
                ),
              ),
              const SizedBox(height: 15),
              GradientButton(
                text: "Kaydet ve Rotayı Göster",
                color: const <Color>[
                  Color(0xFF4527A0),
                  Color(0xFF7E57C2),
                  Color(0xFF2EE2B3),
                ],
                onPressed: saveStation,
              )
            ],
          ),
        ),
      );

  @override
  Widget build(BuildContext context) {
    if (busStations.isEmpty) {
      getData();
    }
    // stationsRef.snapshots().
    return Scaffold(
      body: Center(
        child: Stack(
          children: [
            const MainBackground(),
            _builtUserPage(),
          ],
        ),
      ),
    );
  }
}
