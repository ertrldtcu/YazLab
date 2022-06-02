import 'package:flutter/material.dart';

class InputTheme {
  _builtTextStyle(Color color, {double size = 16.0}) => TextStyle(
        color: color,
        fontSize: size,
      );

  _buildBorder(Color color) => const OutlineInputBorder(
        borderRadius: BorderRadius.all(Radius.circular(50.0)),
        borderSide: BorderSide.none,
      );

  InputDecorationTheme theme() {
    return InputDecorationTheme(
      // General
      contentPadding: const EdgeInsets.all(16),
      fillColor: Colors.white,
      filled: true,

      // Borders
      enabledBorder: _buildBorder(Colors.grey[600]!),
      errorBorder: _buildBorder(Colors.red),
      focusedErrorBorder: _buildBorder(Colors.green),
      focusedBorder: _buildBorder(Colors.blue),
      disabledBorder: _buildBorder(Colors.grey[400]!),

      // Text Styles
      suffixStyle: _builtTextStyle(Colors.black),
      counterStyle: _builtTextStyle(Colors.grey, size: 12.0),
      floatingLabelStyle: _builtTextStyle(Colors.black),
      errorStyle: _builtTextStyle(Colors.red, size: 12.0),
      helperStyle: _builtTextStyle(Colors.black, size: 12.0),
      hintStyle: _builtTextStyle(Colors.grey),
      labelStyle: _builtTextStyle(Colors.black),
      prefixStyle: _builtTextStyle(Colors.black),
    );
  }
}
