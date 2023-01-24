import os
import pyautogui as gui
import pyperclip as pc
import openai
from datetime import datetime
from tkinter import Button
from pynput.mouse import Controller
from time import sleep
from google.cloud import translate_v2 as translate

mouse = Controller()
openai.api_key = "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"
credential_path = r"C:\Users\alanv\Desktop\Hackaton\rare-array-375704-712d7a5f186a.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
translate_client = translate.Client()

class whatsapp:

    #Timestamps
    def log(self, message):
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"[{current_time}] {message}")

    #Parametros
    def __init__(self, speed=.5, click_speed=.3):
        self.speed = speed
        self.click_speed = click_speed

    #Ir al boton verde
    def boton_verde(self):
        try:
            position = gui.locateOnScreen('boton.png', confidence=.9)
            gui.moveTo(position[0:2], duration=self.speed)
            gui.doubleClick(interval=self.click_speed)
        except:
            return

    #Ir a la caja de escribir mensaje
    def paperclip(self):
        try:
            position = gui.locateOnScreen('clip.png', confidence=.9)
            gui.moveTo(position[0:2], duration=self.speed)
            gui.moveRel(170, -55, duration=self.speed)
            gui.doubleClick(interval=self.click_speed)
        except Exception as ex:
            self.log("No hay ventana de WhatsApp abierta.")
    
    #Obtener el mensaje
    def clicks(self):
        gui.tripleClick()
        gui.rightClick()
        position_x = gui.locateOnScreen("x.png", confidence=0.9)
        if position_x is not None:
            gui.moveTo(position_x[0:2], duration=self.speed)
            gui.doubleClick(interval=self.click_speed)
            return False
        else:
            position_copy = gui.locateOnScreen('copy.png', confidence=.8)
            if position_copy is not None:
                self.log("Mensaje recibido.")
                gui.moveTo(position_copy[0:2], duration=self.speed)
                gui.doubleClick(interval=self.click_speed)
                gui.moveRel(0, 300, duration=self.speed)
                gui.doubleClick(interval=self.click_speed)
                return True
        Bot.start()
        return False

    #Enviar el mensaje
    def send(self):
        try:
            position = gui.locateOnScreen('enviar.png', confidence=.8)
            gui.moveTo(position[0:2], duration=self.speed)
            gui.doubleClick()
        except Exception as ex:
            self.log("No hay mensaje para enviar.")
    
    #Reinicia el programa
    def start(self):
        position = gui.locateOnScreen('standby.png', confidence=.8)
        gui.moveTo(position[0:2], duration=self.speed)
        gui.doubleClick()
        self.log("Mensaje enviado.")
        sleep(2)

while True:
    Bot = whatsapp(speed=0.1, click_speed=0.1)
    Bot.boton_verde()
    Bot.paperclip()
    if Bot.clicks() == False:
        sleep(2)
    else:
        #Preparar la respuesta
        text = pc.paste()
   
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"{text}",
            max_tokens=50,
            temperature=0.7
        )
        #Imprimir y enviar la respuesta
        res = response["choices"][0]["text"]
        gui.typewrite(res)
        sleep(1)
        Bot.send()
        sleep(0.5)
        Bot.start()
