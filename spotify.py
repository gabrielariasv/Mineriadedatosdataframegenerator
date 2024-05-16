import requests
import csv
from datetime import date
import os

def get_spotify_token(id,secret):
    data = {
        'grant_type': 'client_credentials',
        'client_id': id,
        'client_secret': secret
    }

    response = requests.post('https://accounts.spotify.com/api/token', data=data)
    return response.json().get('access_token')

def get_spotify_data(accessToken):
    headers = { 
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {accessToken}'
    }

    response = requests.get('https://api.spotify.com/v1/playlists/37i9dQZEVXbMDoHDwVN2tF', headers=headers)
    data = response.json()

    currentDate = date.today().isoformat() # Obtiene la fecha actual en formato YYYY-MM-DD
    top50 = [{
        'position': index + 1, # Añade la posición de la pista en la playlist
        'trackName': item['track']['name'],
        'trackId': item['track']['id'], # Añade la ID del track
        'artists': '; '.join([artist['name'] for artist in item['track']['artists']]), # Añade todos los artistas
        'date': currentDate # Añade la fecha del día
    } for index, item in enumerate(data['tracks']['items'])]

    file_exists = os.path.isfile('data/spotifyData.csv')
    with open('data/spotifyData.csv', 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=top50[0].keys())
        if f.tell() == 0:
            writer.writeheader()  # Si el archivo está vacío, escribe los nombres de las columnas
        writer.writerows(top50)

    return 'Datos guardados correctamente'
