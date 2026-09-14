#include <WiFi.h>
#include <HTTPClient.h>
#include <WebServer.h>
#include "esp_camera.h"

extern uint8_t *debug_jpeg;
extern size_t debug_jpeg_len;

WebServer server(80);

void envoyerSiDetection(const char* objet, float score)
{
if(WiFi.status() == WL_CONNECTED)
    {
        HTTPClient http;
        http.begin("http://10.42.0.1:5000/detection");
        http.addHeader("Content-Type", "application/json");

        String json ="{\"objet\":\"" + String(objet) + "\", \"score\":" + String(score, 2) + "}";
        int retour = http.POST(json);

        Serial.println("envoi raspberry : " + json);
        http.end();
}
}
void initWifi()
{
    // WiFi.begin("GUARA SOMONTANO", "guarasomontano");
    WiFi.begin("PEGASE", "PEGASE123456");

    Serial.print("Connexion WiFi");

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }

    Serial.println();

    Serial.print("IP : ");
    Serial.println(WiFi.localIP());

    server.on("/", HTTP_GET, []()
              {
        camera_fb_t *fb = esp_camera_fb_get();

        if (!fb)
        {
            server.send(500, "text/plain", "capture erreur");
            return;
        }

        server.sendHeader("Content-Disposition", "inline; filename=image.jpg");

        server.send_P(
            200,
            "image/jpeg",
            (const char *)fb->buf,
            fb->len
        );

        esp_camera_fb_return(fb); });

    // Route image envoyée à Edge Impulse
    server.on("/ai", HTTP_GET, []()
              {
        if(debug_jpeg == nullptr)
        {
            server.send(404, "text/plain", "pas encore d'image AI");
            return;
        }

        server.send_P(
            200,
            "image/jpeg",
            (const char*)debug_jpeg,
            debug_jpeg_len
        ); });

    server.begin();

    Serial.println("Serveur HTTP OK");
}

void handleWifi()
{
    server.handleClient();
}