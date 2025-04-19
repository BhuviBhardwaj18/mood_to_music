from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

sp = Spotify(auth_manager=SpotifyClientCredentials(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET"
))

GENRE_MAP = {
    "joy": "pop",
    "sadness": "acoustic",
    "anger": "metal",
    "fear": "ambient",
    "love": "romance",
    "surprise": "experimental",
    "neutral": "indie"
}

def get_music_recommendations(emotion, limit=5):
    """
    Given an emotion string, returns up to `limit` Spotify track recommendations.
    Each recommendation includes:
      - id:   Spotify track ID
      - name: Track name
      - artist: Primary artist
      - url:  Full Spotify URL
    """
    # Map emotion → genre (default to 'pop' if unknown)
    genre = GENRE_MAP.get(emotion, "pop")

    try:
        response = sp.search(q=f"genre:{genre}", type="track", limit=limit)
        items = response.get("tracks", {}).get("items", [])
    except Exception as e:
        # In production you might log this error
        print(f"Error fetching from Spotify: {e}")
        return []

    recommendations = []
    for item in items:
        recommendations.append({
            "id":     item.get("id"),
            "name":   item.get("name"),
            "artist": item.get("artists", [{}])[0].get("name", "Unknown Artist"),
            "url":    item.get("external_urls", {}).get("spotify")
        })

    return recommendations
