import 'package:flutter/material.dart';

class GradientButton extends StatelessWidget {
  final String text;
  final List<Color> color;
  final IconData? icon;
  final VoidCallback? onPressed;
  final double width, height;

  const GradientButton(
      {Key? key,
      this.text = "",
      this.color = const <Color>[Colors.transparent, Colors.transparent],
      this.icon,
      this.onPressed,
      this.height = 50.0,
      this.width = double.infinity})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: width,
      height: height,
      child: RaisedButton(
        color: Colors.transparent,
        shape:
            RoundedRectangleBorder(borderRadius: BorderRadius.circular(80.0)),
        padding: const EdgeInsets.all(0.0),
        child: Ink(
          decoration: BoxDecoration(
            gradient: LinearGradient(
              colors: color,
            ),
            borderRadius: const BorderRadius.all(Radius.circular(80.0)),
          ),
          child: Container(
            color: Colors.transparent,
            constraints: BoxConstraints(minWidth: width, minHeight: height),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Text(
                  text,
                  textAlign: TextAlign.center,
                  style: const TextStyle(color: Colors.white, fontSize: 24.0),
                ),
                icon == null || text == ""
                    ? Container()
                    : const SizedBox(width: 5),
                icon == null ? Container() : Icon(icon, color: Colors.white),
              ],
            ),
          ),
        ),
        onPressed: onPressed ?? () {},
      ),
    );
  }
}
