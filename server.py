from flask import Flask, jsonify
import asyncio
from spotify import get_spotify_token, get_spotify_data
from tiktok import tiktokcsv, trending_videos


app = Flask(__name__)

@app.route('/SpotifyData')
def spotify_data():
    accessToken = get_spotify_token()
    message = get_spotify_data(accessToken)
    return message

@app.route('/TikTokData')
def tiktok_data():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(trending_videos(90))
    tiktokcsv(result)

if __name__ == '__main__':
    app.run(port=3000)