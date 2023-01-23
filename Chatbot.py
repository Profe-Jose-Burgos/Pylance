# Importando las librerias de reconocimiento de imagenes
import pyautogui as pt
import pyperclip as pc
from pynput.mouse import Controller
from time import sleep
mouse = Controller()

class whatsapp:

    #Velocidad del mouse
    def __init__(self, speed=5, click_speed=3):
        self.speed = speed
        self.click_speed = click_speed
        self.message = ''
        self.last_message = ''

    #Ir al boton verde
    def boton_verde(self):
        try:
            position = pt.locateOnScreen('')
            pt.moveTo(position[0:2], duration=self.speed)
            pt.moveRel(-100, 0, duration=self.speed)
            pt.doubleClick(interval=self.click_speed)
        except Exception as ex:
            print('Ocurrió un error: ', ex)

Bot = whatsapp(speed=.5, click_speed=.4)
Bot.boton_verde()