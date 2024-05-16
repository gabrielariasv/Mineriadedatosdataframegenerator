from TikTokApi import TikTokApi
import csv
from datetime import date
import os
import asyncio

ms_token = os.environ.get("Y8tXeEIb0ML1y9Kl4sfChd63KBLt9-dvemIuWNPv1V6MGToVlYg3ErOChI4O_MUxBE-1eRzzz7TurwmPcwLjQt3MGRpDZeStUgK4T170ALpnZgQKOzRXNTzpY4hA", None) 
async def trending_videos(count):
    currentDate = date.today().isoformat() # Obtiene la fecha actual en formato YYYY-MM-DD
    index = 0
    result = []
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens = [ms_token], num_sessions=(int(count/30)), sleep_after=9, headless = False )
        for _ in range(int(count/30)):
            async for video in api.trending.videos(count=30):
                tiktok = video.as_dict
                top50 = {
                'position': index + 1, # Añade la posición del video en la lista
                'title': tiktok['desc'],
                'user': tiktok['author']['nickname'] + "; " +tiktok['author']['id'] ,
                'views': tiktok['stats']['playCount'],
                'likes': tiktok['stats']['diggCount'],
                'comments':tiktok['stats']['commentCount'],
                'original_music': tiktok['music']['original'],
                'musicTitle': tiktok['music']['title'],
                'musicId': tiktok['music']['id'],
                'date': currentDate # Añade la fecha del día
                }
                result.append(top50)
                index+=1
    return result

def tiktokcsv(results):
    with open('data/tiktokData.csv', 'a',  newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        if f.tell() == 0:
            writer.writeheader()  # Si el archivo está vacío, escribe los nombres de las columnas
        writer.writerows(results)
