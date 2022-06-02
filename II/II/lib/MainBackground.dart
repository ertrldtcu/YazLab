import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';

class MainBackground extends StatelessWidget {
  const MainBackground({Key? key}) : super(key: key);

  _builtTopRightSVG() => Opacity(
        opacity: 0.8,
        child: SvgPicture.asset(
          "assets/background/top_right.svg",
          width: 180,
        ),
      );

  _builtLeftCenterSVG() => Opacity(
        opacity: 0.6,
        child: SvgPicture.asset(
          "assets/background/left_center.svg",
          height: 450,
        ),
      );

  _builtBottomSVG() => Opacity(
        opacity: 0.75,
        child: SvgPicture.asset(
          "assets/background/bottom.svg",
        ),
      );

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        Positioned(
          top: 0,
          right: -1,
          child: _builtTopRightSVG(),
        ),
        Positioned(
          left: 0,
          top: 190,
          child: _builtLeftCenterSVG(),
        ),
        Positioned(
          bottom: -1,
          child: _builtBottomSVG(),
        ),
      ],
    );
  }
}
