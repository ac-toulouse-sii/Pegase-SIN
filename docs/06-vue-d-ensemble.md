# 06 Vue d'ensemble

Le projet est composé de deux architectures indépendantes :

- `rasp-IA-architecture` : détection d'objets par IA (YOLO) à partir du flux vidéo d'une ESP32-S3 AICAM
- `esp32-IA-architecture` : réception des détections envoyées directement par le module camera IA DFrobot

modele de camera : 
https://www.gotronic.fr/art-module-cam-ai-esp32-s3-47927.htm

Chacune tourne sur son propre Raspberry Pi, envoie ses données à la même API Symfony, et affiche l'état sur son propre écran LCD.
