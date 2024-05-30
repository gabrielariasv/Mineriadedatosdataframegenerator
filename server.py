import asyncio
import nest_asyncio
from spotify import get_spotify_token, get_spotify_data
from tiktok import tiktokcsv, trending_videos
import sys

nest_asyncio.apply()

id = sys.argv[1]
secret = sys.argv[2]

def spotify_data():
    accessToken = get_spotify_token(id, secret)
    message = get_spotify_data(accessToken)
    return message


def tiktok_data():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(trending_videos(90))
    tiktokcsv(result)

spotify_data()
tiktok_data()
