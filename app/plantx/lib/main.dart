// ignore_for_file: prefer_const_constructors

import 'package:flutter/material.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_svg/svg.dart';
import 'package:webview_flutter/webview_flutter.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
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

class _MyHomePageState extends State<MyHomePage> with TickerProviderStateMixin {
  bool _isLoading = true;

  late AnimationController _controller;
  late Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      vsync: this,
      duration: Duration(milliseconds: 1500), // Set the animation duration
    );

    _scaleAnimation = Tween<double>(
      begin: 0.5,
      end: 1.0, // Scale to full size
    ).animate(CurvedAnimation(
      parent: _controller,
      curve: Curves.ease, // Use the ease curve for smoother animation
    ));

    // Start the animation when the page loads
    _controller.forward();

    // Delay setting _isLoading to false by 2 seconds
    Future.delayed(Duration(seconds: 2), () {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Stack(
          children: [
            // Show the WebView only if not loading
            Visibility(
              visible: !_isLoading,
              child: WebView(
                initialUrl: widget.url,
                javascriptMode: JavascriptMode.unrestricted,
                onPageFinished: (_) {
                  // setState(() {
                  //   // _isLoading = false;
                  // });
                },
              ),
            ),
            // Show the splash logo while loading
            Visibility(
              visible: _isLoading,
              child: AnimatedBuilder(
                animation: _controller,
                builder: (context, child) {
                  return Center(
                    child: Transform.scale(
                      scale: _scaleAnimation.value,
                      child: SvgPicture.asset(
                        'assets/logo.svg',
                        width: 200, // specify the width
                        height: 200, // specify the height
                        // you can also use other properties like color, alignment, etc.
                      ),
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
}
