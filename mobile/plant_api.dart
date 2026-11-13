// Flutter мобайл апп → Docker дотор ажиллаж буй backend API холболт (Лаб 8).
// Flutter төсөлдөө lib/services/plant_api.dart болгон хуулна.
// pubspec.yaml-д нэмэх:  http: ^1.2.0
//
// Хаяг (baseUrl) аль төхөөрөмж дээр ажиллуулахаас хамаарна:
//   Android emulator  → http://10.0.2.2:3000   (emulator-ын "localhost" нь компьютер биш)
//   iOS simulator / Chrome (flutter run -d chrome) → http://localhost:3000
//   Жинхэнэ утас (нэг Wi-Fi) → http://<компьютерийн-IP>:3000
// Android дээр http (https биш) ашиглахын тулд AndroidManifest.xml-ийн <application>-д
//   android:usesCleartextTraffic="true" нэмнэ.

import 'dart:convert';

import 'package:http/http.dart' as http;

class PlantApi {
  PlantApi({this.baseUrl = 'http://10.0.2.2:3000'});

  final String baseUrl;

  /// Сервер ба өгөгдлийн сан ажиллаж байгаа эсэх
  Future<bool> isHealthy() async {
    final res = await http.get(Uri.parse('$baseUrl/health'));
    return res.statusCode == 200;
  }

  /// Таних боломжтой өвчнүүд (мэдлэгийн сан)
  Future<List<Map<String, dynamic>>> getDiseases() async {
    final res = await http.get(Uri.parse('$baseUrl/api/diseases'));
    _check(res);
    return List<Map<String, dynamic>>.from(_decode(res) as List);
  }

  /// Навчны зураг илгээж онош авах (Лаб 5-ын sequence diagram)
  Future<Map<String, dynamic>> diagnose({
    required String plantName,
    required String imagePath,
  }) async {
    final req = http.MultipartRequest('POST', Uri.parse('$baseUrl/api/diagnoses'))
      ..fields['plant_name'] = plantName
      ..files.add(await http.MultipartFile.fromPath('image', imagePath));
    final res = await http.Response.fromStream(await req.send());
    _check(res);
    return Map<String, dynamic>.from(_decode(res) as Map);
  }

  /// Оношийн түүх
  Future<List<Map<String, dynamic>>> getHistory() async {
    final res = await http.get(Uri.parse('$baseUrl/api/diagnoses'));
    _check(res);
    return List<Map<String, dynamic>>.from(_decode(res) as List);
  }

  // Монгол үсэг зөв харагдахын тулд bodyBytes-ийг utf8-аар задална
  dynamic _decode(http.Response res) => jsonDecode(utf8.decode(res.bodyBytes));

  void _check(http.Response res) {
    if (res.statusCode >= 400) {
      final detail = (_decode(res) as Map)['detail'] ?? 'Алдаа';
      throw Exception('API ${res.statusCode}: $detail');
    }
  }
}
