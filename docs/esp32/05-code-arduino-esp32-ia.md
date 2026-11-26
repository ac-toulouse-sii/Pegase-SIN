# 05 : Code ESP32-S3 pour l'architecture Edge Impulse (IA embarquée)

Développé dans VS Code + PlatformIO (voir la fiche 02).

## `platformio.ini` : configuration du projet

- Carte : DFRobot FireBeetle 2 ESP32-S3
- PSRAM activée (nécessaire : le buffer image brut fait environ 900 Ko)
- Port USB natif configuré comme port série

## `main.cpp` : orchestration et inférence

- `setup()` appelle dans l'ordre `initCamera()`, `initWifi()` et `test_camera()`,
  passe `is_initialised` à `true`, puis appelle `initBuffers()` (allocation des buffers
  image).
- `loop()` appelle `handleWifi()`, capture et prétraite l'image, puis lance
  `run_classifier()` (inférence Edge Impulse). Si le score de `"Bouteille"` dépasse
  `0.60`, il appelle `envoyerSiDetection()`.

Traitement de l'image, étape par étape :

1. capture JPEG (640×480) ;
2. conversion en RGB888 ;
3. redimensionnement à 96×96 (taille d'entrée du modèle) ;
4. copie de debug ré-encodée en JPEG (affichée par la route `/ai`).

## `camera.cpp` : caméra

- `initCamera()` configure les pins de la caméra, puis choisit la résolution et la
  qualité JPEG selon la PSRAM : UXGA et haute qualité si elle est présente, sinon repli
  en SVGA dans la DRAM. Une fois la caméra initialisée, la résolution redescend en VGA.
- `test_camera()` capture une image et affiche sa résolution et sa taille. Elle n'est
  appelée qu'une fois, dans `setup()`, pour une vérification ponctuelle.

## `http_wifi.cpp` : connexion et serveur HTTP

- `initWifi()` se connecte au hotspot `PEGASE` et démarre un serveur HTTP (port 80)
  avec deux routes : `/` (dernière image brute) et `/ai` (image réellement envoyée au
  modèle, pour le debug).
- `envoyerSiDetection(objet, score)` envoie un `POST` JSON vers
  `http://10.42.0.1:5000/detection`.
- `handleWifi()` traite les requêtes HTTP entrantes. Elle est appelée en boucle dans
  `loop()`.
