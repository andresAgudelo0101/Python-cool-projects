import speech_recognition as sr
import webbrowser
import keyboard
import pyautogui as pg
import pygame 


# Lista de comandos de voz y sus URLs correspondientes
command_urls = {
    "videos": "https://www.youtube.com/",
    "directos": "https://www.twitch.tv/",
    "Abre YouTube":"https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "Pon la radio":"https://radios.com.co/#radioactiva",
    "quiero ver a mi padre":"https://www.twitch.tv/elxokas"
}

# Diccionario de comandos de voz y combinaciones de teclas correspondientes
key_commands = {
    "nueva": ["ctrl", "t"],
    "cerrar": ["ctrl", "w"],
    "copiar": ["ctrl", "c"],
    "pegar": ["ctrl", "v"],
    "tareas": ["ctrl", "shift","esc"],
    "completa": ["f11"],
    "pausar": ["mediaplaypause"],
    "siguiente": ["medianexttrack"],
    "anterior": ["mediaprevioustrack"],
    "subir": ["volumeup"],
    "bajar": ["volumedown"],
    "silenciar": ["volumemute"],
    "atras": ["ctrl","z"]
}

#inicializamos pygame
pygame.init()
pygame.mixer.init()

#sonido de comando reconocido
sound1 = pygame.mixer.Sound('success.wav')

#sonido de comando no reconocido
sound2 = pygame.mixer.Sound('error.wav')


# Función que reconoce el comando de voz y ejecuta la acción correspondiente
def recognize_and_execute():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Di algo!")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio,language='es-Mx')
        url = command_urls.get(command)
        if url:
            sound1.play()
            webbrowser.open(url)
        elif command in key_commands:
            # Enviamos la combinación de teclas al sistema
            sound1.play()
            pg.hotkey(*key_commands[command])
        else:
            print("El comando de voz no coincide con ninguna acción.")
            sound2.play()
    except sr.UnknownValueError:
        print("No se pudo entender el comando de voz.")
    except sr.RequestError as e:
        print(f"No se pudo obtener respuesta del servicio de reconocimiento de voz: {e}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

# Función que se llama cuando se presiona la tecla especificada
def on_press_callback(event):
    if event.name == "f10":
        recognize_and_execute()

# Función que se llama cuando se suelta la tecla especificada
def on_release_callback(event):
    pass

# Registramos las funciones de callback para cuando se presiona y se suelta la tecla especificada
keyboard.on_press_key("f10", on_press_callback)
keyboard.on_release_key("f10", on_release_callback)

# Mantenemos el programa en ejecución
print("Presione la tecla 'f10' para activar el reconocimiento de voz.")
print('estos son los comandos')
print(key_commands,command_urls)
keyboard.wait()
