"""
Gestion du LCD Grove RGB via le bus I2C.
"""
import os
import json
import time
import subprocess

from smbus2 import SMBus

LCD_FILE = "/data/lcd.json"
etat_lcd = {
    "dernier_affichage": "",
    "index_compteur": 0,
    "dernier_changement": 0
}

# from : https://wiki.seeedstudio.com/Grove-LCD_RGB_Backlight/
# this device has two I2C addresses
DISPLAY_RGB_ADDR = 0x62
DISPLAY_TEXT_ADDR = 0x3E


# set backlight to (R,G,B) (values from 0..255 for each)
def set_rgb(r, g, b):
    """
    Modifie la couleur du rétroéclairage RGB du LCD.

    Args:
        r: intensité rouge (0 à 255)
        g: intensité vert (0 à 255)
        b: intensité bleu (0 à 255)
    """
    bus.write_byte_data(DISPLAY_RGB_ADDR, 0, 0)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 1, 0)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 0x08, 0xAA)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 4, r)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 3, g)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 2, b)


# send command to display (no need for external use)
def text_command(cmd):
    """
    0x80 indique que la donnée envoyée est une instruction LCD
    Exemple :
    0x01 = effacer l'écran
    0x02 = retour curseur
    0x28 = configuration 2 lignes
    """
    bus.write_byte_data(DISPLAY_TEXT_ADDR, 0x80, cmd)


# set display text \n for second line(or auto wrap)
def set_text(text):
    """
    Affiche un texte sur le LCD 16x2.
    """
    text_command(0x01)  # clear display
    time.sleep(0.05)
    text_command(0x08 | 0x04)  # display on, no cursor
    text_command(0x28)  # 2 lines
    time.sleep(0.05)
    count = 0
    row = 0
    for c in text:
        if c == "\n" or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            text_command(0xC0)
            if c == "\n":
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR, 0x40, ord(c))


# Update the display without erasing the display
def set_text_norefresh(text):
    """
    Affiche un texte sans effacer complètement l'écran.
    """
    text_command(0x02)  # return home
    time.sleep(0.05)
    text_command(0x08 | 0x04)  # display on, no cursor
    text_command(0x28)  # 2 lines
    time.sleep(0.05)
    count = 0
    row = 0
    while len(text) < 32:  # clears the rest of the screen
        text += " "
    for c in text:
        if c == "\n" or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            text_command(0xC0)
            if c == "\n":
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR, 0x40, ord(c))


def test_rgb():
    """
    Test du rétroéclairage RGB.
    """
    for _ in range(2):
        set_rgb(255, 0, 0)  # red
        time.sleep(0.5)
        set_rgb(0, 255, 0)  # green
        time.sleep(0.5)
        set_rgb (0, 0, 255)  # blue
        time.sleep(0.5)


def test_lcd():
    """
    Test complet de l'afficheur.
    """
    test_rgb()
    set_text("Hello world\nLCD 16x2 RGB")
    time.sleep(2)
    # la commande suivante garde la prmeière ligne et
    # met à jour la deuxième ligne sans effacer l'écran
    set_text_norefresh("Hello world\nSIN")
    time.sleep(2)
    # la commande suivante garde hello world et mofidiie uniquement la deuxiemee ligne
    set_text_norefresh("Hello world\n2I2D")
    time.sleep(2)
    text_command(0x01)  # clear display

def lire_lcd():
    """
    Lit le fichier lcd.json et met à jour l'afficheur.
    """
    if not os.path.exists(LCD_FILE):
        print("Fichier LCD inexistant")
        return

    try:
        with open(LCD_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            print("Lecture LCD :", data)

        return data

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("Erreur lecture LCD :", e)
        return None


def afficher_lcd():
    """
    Lit le fichier lcd.json et met à jour l'afficheur seulement si nécessaire.
    """

    data = lire_lcd()

    if data is None:
        return

    mode = data.get("mode", "compteur")

    if mode == "detection":

        objet = data.get("objet", "?")
        score = data.get("score", 0)

        texte = f"{objet}\n{score:.2f}"

        # affichage seulement si différent
        if texte != etat_lcd["dernier_affichage"]:
            set_text(texte)
            set_rgb(255, 120, 0)  # orange
            etat_lcd["dernier_affichage"] = texte

        time.sleep(1)

        data["mode"] = "compteur"

        with open(LCD_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)


    else:
        compteurs = data.get("compteurs", {})

        if not compteurs:
            return

        objets = list(compteurs.items())

        # changement toutes les 3 secondes
        if time.time() - etat_lcd["dernier_changement"] > 2:
            etat_lcd["index_compteur"] += 2
            etat_lcd["dernier_changement"] = time.time()

        # retour au début
        if etat_lcd["index_compteur"] >= len(objets):
            etat_lcd["index_compteur"] = 0

        texte = ""

        for objet, nombre in objets[
            etat_lcd["index_compteur"]:
            etat_lcd["index_compteur"] + 2
        ]:
            texte += f"{objet}:{nombre}\n"

        if texte != etat_lcd["dernier_affichage"]:
            set_rgb(0, 100, 255)  # bleu
            set_text(texte)
            etat_lcd["dernier_affichage"] = texte


def get_ip(interface):

    """
    Récupère l'IP d'une interface réseau.
    """
    try:
        resultat = subprocess.check_output(
            ["ip", "-4", "addr", "show", interface],
            text=True
        )

        for ligne in resultat.splitlines():
            if "inet " in ligne:
                return ligne.split()[1].split("/")[0]

    except (subprocess.CalledProcessError, FileNotFoundError):
        return "OFF"

    return "OFF"


def get_ip_address():
    """
    Récupère l'adresse IP du Raspberry Pi.
    """
    wifi = get_ip("wlan0")
    ethernet = get_ip("eth0")

    print("WiFi :", wifi)
    print("Ethernet :", ethernet)

    if wifi != "OFF" or ethernet != "OFF":
        set_rgb(0, 255, 0)
    else:
        set_rgb(255, 0, 0)

    set_text(
        f"W:{wifi}\nE:{ethernet}"
    )

    time.sleep(10)

def afficher_ip_esp32():
    """
    Affiche l'IP du dernier ESP32 détecté.
    """
    data = lire_lcd()

    if data is None:
        return

    ip_esp32 = data.get("esp32", "OFF")

    set_rgb(0, 255, 0)  # vert
    set_text(f"ESP32:\n{ip_esp32}")

    time.sleep(3)

print("Initialisation du s ervice affichage LCD")
bus = SMBus(1)
# test_lcd()
# print("BUS I2C fermé")
# bus.close()


# while True:
#     time.sleep(10)

get_ip_address()
afficher_ip_esp32()


while True:
    afficher_lcd()

    time.sleep(1)
