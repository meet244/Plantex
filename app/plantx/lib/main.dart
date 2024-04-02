import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      // title: 'Web App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(url: 'https://plantex-earth.netlify.app'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  final String url;

  MyHomePage({required this.url});

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  bool _isLoading = true;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // appBar: AppBar(
        // title: Text('Web App'),
      // ),
      body: SafeArea(
        child: Stack(
          children: [
            WebView(
              initialUrl: widget.url,
              javascriptMode: JavascriptMode.unrestricted,
              onPageFinished: (_) {
                setState(() {
                  _isLoading = false;
                });
              },
            ),
            Visibility(
              visible: _isLoading,
              child: Center(
                child: CircularProgressIndicator(),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
