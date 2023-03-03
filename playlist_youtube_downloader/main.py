import os
from pytube import Playlist,exceptions
import pytube
import re

# Obtener la URL de la playlist
playlist_url = 'https://www.youtube.com/playlist?list=PLzXxn0InEuYjep7QBJT04AkdpLUWgS3d4'

# Crear un objeto Playlist de pytube
playlist = Playlist(playlist_url)

# Obtener el título de la playlist y crear una carpeta con ese nombre
playlist_title = playlist.title
os.makedirs(playlist_title, exist_ok=True)

#caracteres especiales
special_chars_regex = r'[\"\'\\\/\|\?\-\[\]\&\*<>]'

# Descargar cada video de la playlist
for video in playlist.videos:
    # Verificar que el título del video no tenga caracteres no ASCII
    try:
        video_title = video.title.encode('ASCII', 'ignore').decode('utf-8')
        if video_title != video.title or re.search(special_chars_regex, video_title):
            video_title = re.sub(special_chars_regex, '', video_title)
        
        # Descargar el video
        video.streams.get_lowest_resolution().download(output_path=playlist_title, filename=video_title)
    except (KeyError, exceptions.PytubeError)as e:
        print(f"Skipping video with error: {str(e)}")
        continue  # Ir al siguiente video en caso de error

    # Verificar si el archivo de video existe antes de convertirlo a mp3
    video_file = os.path.join(playlist_title, f'{video_title}')
    if not os.path.exists(video_file):
        print(f"Skipping video '{video_title}' because video file not found.")
        continue  # Ir al siguiente video si el archivo no existe

    audio_file = os.path.join(playlist_title, f'{video_title}.mp3')
    os.system(f'ffmpeg -i "{video_file}" -vn -ar 44100 -ac 2 -ab 192k -f mp3 -n "{audio_file}"')

    # Elimina el archivo de video original
    os.remove(video_file)

print('Descarga finalizada')

