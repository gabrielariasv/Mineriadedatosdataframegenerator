import yt_dlp as youtube_dl
import asyncio
from shazamio import Shazam
import os
import pandas as pd
import csv
from TikTokApi import TikTokApi

ms_token = os.environ.get("Y8tXeEIb0ML1y9Kl4sfChd63KBLt9-dvemIuWNPv1V6MGToVlYg3ErOChI4O_MUxBE-1eRzzz7TurwmPcwLjQt3MGRpDZeStUgK4T170ALpnZgQKOzRXNTzpY4hA", None)

async def alivevid(sound_id):
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=1, headless = False)
        async for sound in api.sound(id=sound_id).videos(count=1):
            tiktok = sound.as_dict
            video = tiktok['id']
            user = tiktok['author']['uniqueId']
            url = f"https://www.tiktok.com/@{user}/video/{video}"
        return url

async def music_identifier(sound_id, url):

    # Configura las opciones para yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best', 
        'outtmpl': f'downloads/{sound_id}.mp3', 
    }

    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        shazam = Shazam()
        out = await shazam.recognize(f'downloads/{sound_id}.mp3')

        # Elimina el archivo descargado después de reconocer la música
        os.remove(f'downloads/{sound_id}.mp3') 

        return sound_id, out['track']['title'], out['track']['subtitle']
    except Exception as e:
        print(f"Error en la descarga o reconocimiento: {e}")
        return None

def shazamcsv(results):
    with open('data/tiktokData.csv', 'a',  newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        if f.tell() == 0:
            writer.writeheader()  # Si el archivo está vacío, escribe los nombres de las columnas
        writer.writerows(results)

def tiktok_real_music(data):
    results = []
    df = pd.read_csv(data, encoding="iso-8859-1")
    for row in df.itertuples():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        url = loop.run_until_complete(alivevid(row.musicId))
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        musica = loop.run_until_complete(music_identifier(row.musicId, url))
        if musica:
            results.append(musica)
    shazamcsv(results)



tiktok_real_music("data/tiktokData.csv")

