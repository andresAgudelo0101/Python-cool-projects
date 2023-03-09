import speech_recognition as sr
import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment
import os

# Crea la ventana principal de la aplicación
root = tk.Tk()
root.withdraw()

# Abre un cuadro de diálogo para que el usuario seleccione el archivo de audio
file_path = filedialog.askopenfilename()

# Carga el archivo de audio y obtiene su duración en milisegundos
audio_file = AudioSegment.from_file(file_path)
audio_duration = len(audio_file)

# Define la duración de cada parte en milisegundos y calcula el número de partes
part_duration = 30000  # Duración de cada parte en milisegundos (30 segundos)
num_parts = audio_duration // part_duration + 1

# Recorta el archivo de audio en partes y guarda cada parte en un archivo separado
for i in range(num_parts):
    os.makedirs('audio_partition', exist_ok=True)
    start_time = i * part_duration
    end_time = min((i + 1) * part_duration, audio_duration)
    part = audio_file[start_time:end_time]
    part.export(f"audio_partition/parte_{i+1}.wav", format="wav")


#lista de las transcripciones
transcripciones = []

for i in range(num_parts):
    # Crea un objeto Recognizer y transcribe el audio
    r = sr.Recognizer()
    with sr.AudioFile(os.path.join(".", f"audio_partition/parte_{i+1}.wav")) as source:
        audio = r.record(source)
    text = r.recognize_google(audio, show_all=True, language='es-ES')
    if 'alternative' in text and len(text['alternative']) > 0:
        transcript = text['alternative'][0]['transcript']
        print(transcript)
        transcripciones.append(transcript)
    else:
        print(f"No se encontraron alternativas para la parte {i+1}.")

# Crea un archivo de texto para almacenar las transcripciones
with open('resultado_transcripcion.txt', 'w') as f:
    for transcripcion in transcripciones:
        f.write(transcripcion + "\n")

# Elimina los archivos de audio creados
for i in range(num_parts):
    os.remove(f"audio_partition/parte_{i+1}.wav")

# Elimina el directorio de audio_partition
os.rmdir("audio_partition")
