import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:routeplanning/GradientButton.dart';
import 'package:routeplanning/pages/UserPage.dart';
import '../MainBackground.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_core/firebase_core.dart';

FirebaseFirestore fs = FirebaseFirestore.instance;
CollectionReference usersRef = fs.collection('users');

class LoginPage extends StatefulWidget {
  const LoginPage({Key? key}) : super(key: key);

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final usernameController = TextEditingController();
  final passwordController = TextEditingController();
  bool _showPassword = true;

  void login() async {
    await usersRef
        .where('username', isEqualTo: usernameController.text)
        .where('password', isEqualTo: passwordController.text)
        .get()
        .then((value) {
      if (value.size > 0) {
        if (value.docs[0].get("isAdmin") == true) {
          Navigator.pushNamed(context, '/adminpage');
        } else {
          Navigator.push(context, MaterialPageRoute(
            builder: (context) {
              return UserPage(
                userid: value.docs[0].get("id"),
              );
            },
          ));
        }
      } else {
        showDialog(
          context: context,
          builder: (context) => AlertDialog(
            title: const Text('Hata'),
            content: const Text('Lütfen bilgilerinizi kontrol ediniz.'),
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
    });
  }

  _builtLoginPage() => SafeArea(
        child: Center(
          child: SingleChildScrollView(
            reverse: true,
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 28.0),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  SvgPicture.asset(
                    "assets/logo.svg",
                    // width: 200,
                    height: 180,
                    // fit: BoxFit.scaleDown,
                  ),
                  const Text(
                    "Rota Oluşturma & Takip Etme",
                    style: TextStyle(fontSize: 24.0),
                  ),
                  const SizedBox(height: 60),
                  Container(
                    child: TextField(
                      controller: usernameController,
                      decoration: const InputDecoration(
                        prefixIcon: Icon(Icons.account_circle),
                        hintText: "Kullanıcı adı",
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
                  const SizedBox(height: 15),
                  Container(
                    child: TextField(
                      controller: passwordController,
                      decoration: InputDecoration(
                        prefixIcon: const Icon(Icons.lock),
                        suffixIcon: IconButton(
                          icon: Icon(_showPassword
                              ? Icons.visibility
                              : Icons.visibility_off),
                          onPressed: () =>
                              setState(() => _showPassword = !_showPassword),
                        ),
                        hintText: "Şifre",
                      ),
                      obscureText: _showPassword,
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
                  const SizedBox(height: 50),
                  GradientButton(
                    text: "Giriş Yap",
                    color: const <Color>[
                      Color(0xFF062880),
                      Color(0xFF03ACAD),
                      Color(0xFF2EE2B3),
                    ],
                    onPressed: login,
                  ),
                ],
              ),
            ),
          ),
        ),
      );

  @override
  Widget build(BuildContext context) {
    usernameController.text = "admin";
    passwordController.text = "1234";
    return Scaffold(
      body: Center(
        child: Stack(
          children: [
            const MainBackground(),
            _builtLoginPage(),
          ],
        ),
      ),
    );
  }
}
