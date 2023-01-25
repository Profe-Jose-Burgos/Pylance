import os
import pyautogui as gui
import pyperclip as pc
from datetime import datetime
from tkinter import Button
from pynput.mouse import Controller
from unidecode import unidecode
from time import sleep
from tensorflow import keras
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.inception_v3 import preprocess_input
from keras.applications.inception_v3 import InceptionV3, decode_predictions
from google.cloud.dialogflow_v2 import types
from google.cloud import translate_v2 as translate
from google.cloud import dialogflow as df

mouse = Controller()
session_client = df.SessionsClient()
session = session_client.session_path("rare-array-375704", "me")
credential_path = r"C:\Users\alanv\Desktop\Hackaton\rare-array-375704-80556aca21e2.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
translate_client = translate.Client()
iv3 = InceptionV3()
Imagentemporal = r"C:\Users\alanv\Desktop\Hackaton\1.jpg"

class whatsapp:

    #Timestamps
    def log(self, message):
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"[{current_time}] {message}")

    #Borrar imagen temporal
    def borrarimagen(self):
        if os.path.isfile(Imagentemporal):
            os.remove(Imagentemporal)
        else:
            self.log("No hay imagen temporal.")
    
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
                gui.rightClick(interval=self.click_speed)
        except Exception as ex:
            self.log("No hay ventana de WhatsApp abierta.")
    
    #Obtener el mensaje
    def clicks(self):
        position_type = gui.locateOnScreen("typeames.jpg", confidence=.7)
        position_x = gui.locateOnScreen("x.png", confidence=.9)
        gui.rightClick()
        position_save = gui.locateOnScreen("save.jpg", confidence=.8)
        tipo = None
        if position_save is not None:
            try:
                gui.moveTo(position_save[0:2], duration=self.speed)
                gui.doubleClick(interval=self.click_speed)
                sleep(2)
                position_arrow = gui.locateOnScreen("left_arrow.jpg", confidence=.7)
                gui.moveTo(position_arrow[0:2], duration=self.speed)
                gui.click(interval=self.click_speed)
                gui.typewrite("1")
                gui.press('enter')
                gui.typewrite('y')
                gui.moveTo(position_type[0:2], duration=self.speed)
                gui.click()
                tipo = "imagen"
                self.log("Mensaje tipo: imagen")
                return tipo
            except Exception as ex:
                self.log(ex)
            gui.doubleClick()
        elif position_x is not None:
            gui.moveTo(position_x[0:2], duration=self.speed)
            tipo = None
            self.log("Mensaje tipo: None")
            return tipo
        else:
            gui.click()
            gui.rightClick(interval=self.click_speed)
            position_copy = gui.locateOnScreen('copy.png', confidence=.8)
            if position_copy is not None:
                self.log("Mensaje recibido.")
                gui.moveTo(position_copy[0:2], duration=self.speed)
                gui.doubleClick(interval=self.click_speed)
                gui.moveTo(position_type[0:2], duration=self.speed)
                gui.doubleClick(interval=self.click_speed)
                tipo = "text"
                self.log("Mensaje tipo: text")
            return tipo
    
    #Enviar el mensaje
    def send(self):
        try:
            gui.press('enter')
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
    Bot = whatsapp(speed=0.1, click_speed=0)
    Bot.borrarimagen()
    Bot.boton_verde()
    Bot.paperclip()
    result = Bot.clicks()
    if result == None:
        sleep(2)
    elif result == "imagen":
        try:
            #Preparar la descripción de la imagen
            img_path = r"C:\Users\alanv\Desktop\Hackaton\1.jpg"
            img = image.load_img(img_path, target_size=(299, 299))
            x = img_to_array(img)
            x = x.reshape([1, x.shape[0], x.shape[1], x.shape[2]]) 
            keras.applications.inception_v3.preprocess_input(x)
            y = iv3.predict(x)
            info = decode_predictions(y)
            desc = translate_client.translate(str(info[0][0][1]), target_language='es')
            desc = desc['translatedText']
            print(desc)
            gui.typewrite("Esta imagen puede ser: " + desc)
            gui.press('enter')
            os.remove(r"C:\Users\alanv\Desktop\Hackaton\1.jpg")
            Bot.start()
        except Exception as ex:
            print("Ocurrió un error:", ex)
    else:
        #Preparar la respuesta
        text = pc.paste()
        mensaje = translate_client.translate(str(text), target_language='en')
        translated = mensaje['translatedText']
        textinput = types.TextInput(text=translated, language_code='en')
        query = types.QueryInput(text=textinput)
        print(query)
        try:
            enviar = session_client.detect_intent(session=session, query_input=query)
            respuesta = enviar.query_result.fulfillment_text
            #Imprimir y enviar mensaje
            a = respuesta
            b = translate_client.translate(str(a), target_language='es')
            c = b['translatedText']
            res = unidecode(c)
            gui.typewrite(res)
            sleep(1)
            Bot.send()
            sleep(0.5)
            Bot.start()
        except Exception as ex:
            print("Ocurrió un error:", ex)
            Bot.start()
