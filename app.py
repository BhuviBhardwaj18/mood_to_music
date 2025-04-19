from flask import Flask, render_template, request
from transformers import pipeline
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

# Load the emotion detection pipeline
emotion_classifier = pipeline(
    "text-classification",
    model="nateraw/bert-base-uncased-emotion",
    device=0  # Change to -1 if not using GPU
)

# Spotify credentials (ensure your credentials are secure!)
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="YOUR_SPOTIFY_CLIENT_ID",
    client_secret="YOUR_SPOTIFY_CLIENT_SECRET"
))

# Emotion to Spotify genre mapping
GENRE_MAP = {
    "joy": "happy",
    "sadness": "sad",
    "anger": "rock",
    "fear": "ambient",
    "love": "romance",
    "surprise": "dance",
    "neutral": "pop"
}

# Emotion to theme mapping
EMOTION_THEMES = {
    "joy": {"bg": "#FFF8DC", "text": "#FF8C00", "accent": "#FFD700"},
    "sadness": {"bg": "#D3D3D3", "text": "#2F4F4F", "accent": "#1E90FF"},
    "anger": {"bg": "#FFE4E1", "text": "#B22222", "accent": "#DC143C"},
    "fear": {"bg": "#F5F5F5", "text": "#4B0082", "accent": "#8A2BE2"},
    "love": {"bg": "#FFF0F5", "text": "#C71585", "accent": "#FF69B4"},
    "surprise": {"bg": "#F0FFFF", "text": "#DAA520", "accent": "#7FFFD4"},
    "neutral": {"bg": "#FFFFFF", "text": "#000000", "accent": "#CCCCCC"}
}

def detect_emotion(text):
    result = emotion_classifier(text)[0]
    return result['label'].lower(), float(result['score'])

def get_music_recommendations(emotion, limit=5):
    genre = GENRE_MAP.get(emotion, "pop")
    results = sp.search(q=f"genre:{genre}", type="track", limit=limit)
    return [{
        "name": item["name"],
        "artist": item["artists"][0]["name"],
        "url": item["external_urls"]["spotify"]
    } for item in results["tracks"]["items"]]

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        text = request.form["text"]
        emotion, confidence = detect_emotion(text)
        theme = EMOTION_THEMES.get(emotion, EMOTION_THEMES["neutral"])
        songs = get_music_recommendations(emotion)
        return render_template("result.html", emotion=emotion, confidence=confidence, songs=songs, theme=theme)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
