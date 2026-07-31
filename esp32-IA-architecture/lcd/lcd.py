"""
Gestion du LCD Grove RGB via le bus I2C.
"""
import time
from smbus2 import SMBus

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
    # la commande suivante garde la prmeière ligne et met à jour la deuxième ligne sans effacer l'écran
    set_text_norefresh("Hello world\nSIN")
    time.sleep(2)
    # la commande suivante garde hello world et mofidiie uniquement la deuxiemee ligne
    set_text_norefresh("Hello world\n2I2D")
    time.sleep(2)
    text_command(0x01)  # clear display


print("Initialisation du service affichage LCD")
bus = SMBus(1)

test_lcd()

print("BUS I2C fermé")
bus.close()


# while True:
#     time.sleep(10)
