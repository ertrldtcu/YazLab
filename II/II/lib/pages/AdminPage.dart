import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/material.dart';
import '../MainBackground.dart';
import '../GradientButton.dart';

FirebaseFirestore fs = FirebaseFirestore.instance;
CollectionReference stationsRef = fs.collection('stations');

class AdminPage extends StatefulWidget {
  const AdminPage({Key? key}) : super(key: key);

  @override
  State<AdminPage> createState() => _AdminPageState();
}

class _AdminPageState extends State<AdminPage> {
  late TextEditingController stationNameController;
  late TextEditingController passengerCountController;

  @override
  void initState() {
    super.initState();
    stationNameController = TextEditingController();
    passengerCountController = TextEditingController();
  }

  @override
  void dispose() {
    stationNameController.dispose();
    passengerCountController.dispose();
    super.dispose();
  }

  List busStations = [];

  void getData() async {
    // Get docs from collection reference
    var querySnapshot = await stationsRef.get();
    for (var doc in querySnapshot.docs) {
      busStations.add([
        doc.get("id"),
        doc.get("name"),
        doc.get("lat"),
        doc.get("lng"),
        doc.get("passengerCount")
      ]);
      setState(() {});
    }
  }

  _builtListItem(context, index) => Padding(
        padding: const EdgeInsets.symmetric(horizontal: 8.0, vertical: 4.0),
        child: Container(
          margin: const EdgeInsets.only(bottom: 5.0),
          decoration: const BoxDecoration(
            color: Color(0x40FFFFFF),
            boxShadow: [
              BoxShadow(
                color: Color(0x50000000),
                blurRadius: 4,
                offset: Offset(0, 0),
              ),
            ],
            borderRadius: BorderRadius.all(Radius.circular(50.0)),
          ),
          child: Padding(
            padding:
                const EdgeInsets.symmetric(horizontal: 18.0, vertical: 4.0),
            child: Row(
              children: [
                Text(
                  busStations[index][1],
                  style: const TextStyle(
                      fontSize: 20.0, fontWeight: FontWeight.w600),
                ),
                Expanded(child: Container()),
                const GradientButton(
                  icon: Icons.remove_circle,
                  width: 50,
                  height: 40,
                ),
                const SizedBox(width: 5),
                GradientButton(
                  text: busStations[index][4].toString(),
                  color: const <Color>[
                    Color(0xFFFF5C00),
                    Color(0xFF7E57C2),
                  ],
                  width: 50,
                  height: 40,
                  onPressed: () {
                    changePassengerCount(busStations[index][0]);
                  },
                ),
              ],
            ),
          ),
        ),
      );

  _builtAdminPage() => SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(28.0),
          child: Column(
            children: <Widget>[
              GradientButton(
                text: "Durak Ekle",
                color: const <Color>[
                  Color(0xFFFF5C00),
                  Color(0xFF7E57C2),
                ],
                icon: Icons.directions_bus,
                onPressed: () async {
                  final stationName = await openDialog();
                  if (stationName == null || stationName.isEmpty) return;
                  print(stationName);
                },
              ),
              const SizedBox(height: 15),
              Expanded(
                child: ListView.builder(
                  itemCount: busStations.length,
                  itemBuilder: (context, index) =>
                      _builtListItem(context, index),
                ),
              ),
              const SizedBox(height: 15),
              Row(
                children: const [
                  Expanded(
                      child: GradientButton(
                    text: "Senaryo 1",
                    color: <Color>[
                      Color(0xFFFF5C00),
                      Color(0xFF7E57C2),
                    ],
                  )),
                  SizedBox(width: 5),
                  Expanded(
                      child: GradientButton(
                    text: "Senaryo 2",
                    color: <Color>[
                      Color(0xFFFF5C00),
                      Color(0xFF7E57C2),
                    ],
                  )),
                ],
              ),
            ],
          ),
        ),
      );

  @override
  Widget build(BuildContext context) {
    if (busStations.isEmpty) {
      getData();
    }
    return Scaffold(
      body: Center(
        child: Stack(
          children: [
            const MainBackground(),
            _builtAdminPage(),
          ],
        ),
      ),
    );
  }

  Future<String?> openDialog() => showDialog<String>(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text(
            "Yeni Durak Ekle",
            textAlign: TextAlign.center,
          ),
          content: Container(
            child: TextField(
              controller: stationNameController,
              autofocus: true,
              // controller: usernameController,
              decoration: const InputDecoration(
                prefixIcon: Icon(Icons.directions_bus),
                hintText: "Durak ismi",
              ),
              keyboardType: TextInputType.name,
            ),
            decoration: const BoxDecoration(
              boxShadow: [
                BoxShadow(
                  color: Colors.black38,
                  blurRadius: 15,
                  offset: Offset(0, 5),
                ),
              ],
            ),
          ),
          actions: [
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: GradientButton(
                text: "Ekle",
                color: const <Color>[
                  Color(0xFF062880),
                  Color(0xFF03ACAD),
                  Color(0xFF2EE2B3),
                ],
                onPressed: submit,
              ),
            )
          ],
        ),
      );

  Future<String?> changePassengerCount(int stationID) => showDialog<String>(
        context: context,
        builder: (context) => AlertDialog(
          title: const Text(
            "Yolcu Sayısı Değiştir",
            textAlign: TextAlign.center,
          ),
          content: Container(
            child: TextField(
              controller: passengerCountController,
              autofocus: true,
              // controller: usernameController,
              decoration: const InputDecoration(
                prefixIcon: Icon(Icons.supervisor_account_rounded),
                hintText: "Yolcu Sayısı",
              ),
              keyboardType: TextInputType.name,
            ),
            decoration: const BoxDecoration(
              boxShadow: [
                BoxShadow(
                  color: Colors.black38,
                  blurRadius: 15,
                  offset: Offset(0, 5),
                ),
              ],
            ),
          ),
          actions: [
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: GradientButton(
                text: "Değiştir",
                color: const <Color>[
                  Color(0xFF062880),
                  Color(0xFF03ACAD),
                  Color(0xFF2EE2B3),
                ],
                onPressed: () {
                  stationsRef.doc(stationID.toString()).update(
                      {"passengerCount": passengerCountController.text});
                  Navigator.of(context).pop();
                },
              ),
            )
          ],
        ),
      );

  void submit() {
    Navigator.of(context).pop(stationNameController.text);
  }
}
