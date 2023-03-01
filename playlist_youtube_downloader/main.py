from tkinter import *
from tkinter import messagebox
from pytube import Playlist
from moviepy.editor import *
from pytube import YouTube


def download_playlist():
    # Obtener la URL de la lista de reproducción ingresada por el usuario
    playlist_url = url_entry.get()

    # Descargar todos los videos de la lista de reproducción
    playlist = Playlist(playlist_url)
    def filter_audio_low_quality(stream):
        return 'audio' in stream.mime_type and stream.abr <= '128kbps'
    for video_url in playlist.video_urls:
        yt = YouTube(video_url)
        stream = yt.streams.filter(filter_audio_low_quality).first()
        stream.download(output_path='./audio', filename=yt.title + '.mp4')

    # Convertir todos los archivos MP4 descargados a MP3
    for mp4_file in os.listdir('./audio'):
        if mp4_file.endswith('.mp4'):
            mp4_path = os.path.join('./audio', mp4_file)
            mp3_path = os.path.join('./audio', mp4_file[:-4] + '.mp3')
            audio = AudioFileClip(mp4_path)
            audio.write_audiofile(mp3_path)
            os.remove(mp4_path)

    # Mostrar un mensaje de éxito al usuario
    messagebox.showinfo('Descarga completada', 'Todos los videos de la lista de reproducción han sido descargados y convertidos a MP3.')

# Crear una ventana de la aplicación
root = Tk()
root.title('Descargar lista de reproducción de YouTube')

# Agregar un cuadro de entrada para la URL de la lista de reproducción
url_label = Label(root, text='URL de la lista de reproducción:')
url_label.pack()
url_entry = Entry(root, width=50)
url_entry.pack()

# Agregar un botón para descargar la lista de reproducción
download_button = Button(root, text='Descargar lista de reproducción', command=download_playlist)
download_button.pack()

# Ejecutar el bucle principal de la ventana
root.mainloop()
