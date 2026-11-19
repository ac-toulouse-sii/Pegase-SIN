#include <WiFi.h>
#include <HTTPClient.h>
#include <WebServer.h>
#include "esp_camera.h"

extern uint8_t *debug_jpeg;
extern size_t debug_jpeg_len;

unsigned long derniereConnexion = millis();


WebServer server(80);

void envoyerSiDetection(const char* objet, float score)
{
if(WiFi.status() == WL_CONNECTED)
    {
        HTTPClient http;
        /* Adresse du RASPBERRY (et non de la caméra).
        Elle dépend du réseau : à changer en même temps que WiFi.begin().*/

        /*exemples de reseaux */
        //http.begin("http://192.168.1.63:5000/detection");
        // http.begin("http://172.20.10.13:5000/detection");

        http.begin("http://10.42.0.1:5000/detection");  // adresse Hotspot Raspberry

        http.addHeader("Content-Type", "application/json");

        String json ="{\"objet\":\"" + String(objet) + "\", \"score\":" + String(score, 2) + "}";
        int retour = http.POST(json);

        Serial.println("envoi raspberry : " + json);
        http.end();
}
}
void initWifi()
{   // Réseau auquel la caméra se connecte (un seul actif à la fois)

    //WiFi.begin("login", "password");      // à changer selon le réseau
    WiFi.begin("PEGASE", "PEGASE123456");   // à changer selon le réseau

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
    if (millis() - derniereConnexion > 5000)
    {
        derniereConnexion = millis();
        Serial.print("IP CAMERA :");
        Serial.println(WiFi.localIP());
    }
}