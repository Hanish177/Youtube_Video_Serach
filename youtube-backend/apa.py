from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/api/videos', methods=['GET'])
def get_videos():
    query = request.args.get('query', 'cricket')  # Default to 'cricket'
    api_key = 'AIzaSyBfFYIQE0fy3-MtlpKGSC8YxqHkTiDALPU'  # Replace with your actual API key
    search_url = "https://www.googleapis.com/youtube/v3/search"
    video_details_url = "https://www.googleapis.com/youtube/v3/videos"

    # Step 1: Fetch video IDs
    search_params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 50,
        "fields": "items(id/videoId)",
        "key": api_key
    }
    search_response = requests.get(search_url, params=search_params)
    video_ids = [item["id"]["videoId"] for item in search_response.json().get("items", [])]

    # Step 2: Fetch video details
    if video_ids:
        details_params = {
            "part": "snippet",
            "id": ",".join(video_ids),
            "fields": "items(id,snippet/title,snippet/description,snippet/publishedAt,snippet/thumbnails,snippet/tags)",
            "key": api_key
        }
        details_response = requests.get(video_details_url, params=details_params)
        return jsonify(details_response.json())
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)
