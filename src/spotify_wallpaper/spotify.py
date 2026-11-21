"""
Spotify Web API Client & OAuth Integration
Zero-dependency client using Python standard library (urllib + http.server).
"""

import sys
import os
import json
import base64
import urllib.request
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser
from typing import Dict, List, Optional, Tuple
from pathlib import Path

from .config import (
    ENV_FILE,
    ENV_ALT_FILE,
    DEFAULT_TRACKS_FILE,
    DEFAULT_ENGLISH_TRACKS_FILE,
    DEFAULT_LYRICS_FILE,
    DEFAULT_ENGLISH_LYRICS_FILE,
)

REDIRECT_URI = "http://127.0.0.1:8888/callback"
PORT = 8888
SCOPES = "user-top-read user-library-read"

_auth_code = None


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Local HTTP handler to receive the Spotify OAuth authorization code."""

    def do_GET(self):
        global _auth_code
        parsed_url = urllib.parse.urlparse(self.path)
        if parsed_url.path == "/callback":
            query_params = urllib.parse.parse_qs(parsed_url.query)
            if "code" in query_params:
                _auth_code = query_params["code"][0]
                self.send_response(200)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                html = """
                <!DOCTYPE html>
                <html>
                <head><title>Spotify Connected</title></head>
                <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #000; color: #fff; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0;">
                    <div style="text-align: center; padding: 48px; border-radius: 16px; background: #121212; border: 1px solid #282828; max-width: 440px;">
                        <h1 style="color: #1DB954; font-size: 24px; margin: 0 0 8px;">Spotify Authenticated!</h1>
                        <p style="color: #a0a0a0; font-size: 15px; margin: 0;">You can now close this window and return to your terminal.</p>
                    </div>
                </body>
                </html>
                """
                self.wfile.write(html.encode("utf-8"))
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Error: No authorization code received.")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        return


def load_credentials() -> Tuple[Optional[str], Optional[str]]:
    """Loads Spotify client ID and client secret from environment or env files."""
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")

    for env_path in [ENV_FILE, ENV_ALT_FILE]:
        if (not client_id or not client_secret) and os.path.isfile(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("SPOTIFY_CLIENT_ID="):
                        client_id = client_id or line.split("=", 1)[1].strip()
                    elif line.startswith("SPOTIFY_CLIENT_SECRET="):
                        client_secret = client_secret or line.split("=", 1)[1].strip()

    return client_id, client_secret


def save_credentials_to_env(client_id: str, client_secret: str, path: Optional[Path] = None):
    """Saves credentials to env file."""
    target = path or ENV_FILE
    with open(target, "w", encoding="utf-8") as f:
        f.write(f"SPOTIFY_CLIENT_ID={client_id}\n")
        f.write(f"SPOTIFY_CLIENT_SECRET={client_secret}\n")


def get_access_token(client_id: str, client_secret: str) -> str:
    """Performs OAuth authorization code flow and exchanges for an access token."""
    global _auth_code
    _auth_code = None

    auth_params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "show_dialog": "false",
    }
    auth_url = f"https://accounts.spotify.com/authorize?{urllib.parse.urlencode(auth_params)}"

    print("\n" + "=" * 65)
    print("Opening browser to authenticate with Spotify...")
    print(f"If your browser does not open automatically, visit:\n{auth_url}")
    print("=" * 65 + "\n")

    webbrowser.open(auth_url)

    server = HTTPServer(("127.0.0.1", PORT), OAuthCallbackHandler)
    while _auth_code is None:
        server.handle_request()
    server.server_close()

    token_url = "https://accounts.spotify.com/api/token"
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("utf-8")
    data = urllib.parse.urlencode({
        "grant_type": "authorization_code",
        "code": _auth_code,
        "redirect_uri": REDIRECT_URI,
    }).encode("utf-8")

    req = urllib.request.Request(
        token_url,
        data=data,
        headers={
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        return res["access_token"]


def fetch_top_tracks(access_token: str, time_range: str = "long_term", limit: int = 50) -> Dict:
    """Fetches user top tracks for a specified time range."""
    url = f"https://api.spotify.com/v1/me/top/tracks?time_range={time_range}&limit={limit}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {access_token}"})
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Warning: Failed to fetch top tracks ({time_range}): {e}")
        return {}


def fetch_paged_tracks(access_token: str, endpoint: str, limit: int = 50, offset: int = 0) -> Dict:
    """Fetches paged data from Spotify Web API."""
    url = f"{endpoint}?limit={limit}&offset={offset}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {access_token}"})
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Warning: Failed to fetch {url}: {e}")
        return {}


def format_track_items(raw_items: List[Dict]) -> List[Dict]:
    """Formats raw Spotify track dicts into clean, normalized track objects."""
    results = []
    for item in raw_items:
        track_obj = item.get("track", item)
        if not track_obj or not track_obj.get("name"):
            continue

        album_images = (track_obj.get("album", {}).get("images") or [{}])
        results.append({
            "id": track_obj.get("id"),
            "name": track_obj.get("name"),
            "artists": [a.get("name") for a in track_obj.get("artists", [])],
            "album": track_obj.get("album", {}).get("name"),
            "album_art": album_images[0].get("url") if album_images else "",
            "popularity": track_obj.get("popularity", 0),
            "spotify_url": track_obj.get("external_urls", {}).get("spotify", ""),
        })
    return results


def is_english_music(track_name: str, artists: List[str], album: str = "") -> bool:
    """Filters tracks to check if text uses standard Latin / English character sets."""
    full_text = f"{track_name} {' '.join(artists)} {album}"
    if not full_text.strip():
        return True
    ascii_count = sum(1 for c in full_text if ord(c) < 128)
    return (ascii_count / len(full_text)) >= 0.85


def curate_english_lyrics(tracks: List[Dict]) -> List[Dict]:
    """Generates clean typography phrase entries for tracks."""
    curated = []
    for t in tracks:
        name = t["name"]
        artist_str = ", ".join(t["artists"])
        lyric = f"{name.upper()} · {artist_str.upper()}"
        curated.append({
            "title": name,
            "artist": artist_str,
            "album": t.get("album", ""),
            "lyric": lyric,
        })
    return curated


def run_spotify_pipeline(
    fetch_count: int = 150,
    save_tracks: bool = True,
    update_lyrics: bool = True,
) -> Dict:
    """End-to-end Spotify authentication, fetching, and curation runner."""
    client_id, client_secret = load_credentials()

    if not client_id or not client_secret:
        print("\n" + "=" * 65)
        print("SPOTIFY DEVELOPER CREDENTIALS NEEDED")
        print("=" * 65)
        print("Please provide your Spotify App credentials from:")
        print("https://developer.spotify.com/dashboard\n")
        client_id = input("Enter SPOTIFY_CLIENT_ID: ").strip()
        client_secret = input("Enter SPOTIFY_CLIENT_SECRET: ").strip()

        if client_id and client_secret:
            save_credentials_to_env(client_id, client_secret)
            print(f"[OK] Saved credentials to {ENV_FILE}")
        else:
            raise ValueError("Spotify Client ID and Secret are required to fetch listening data.")

    token = get_access_token(client_id, client_secret)
    print("\n[SUCCESS] Spotify Access Token acquired!")

    all_tracks = []
    seen_ids = set()

    def add_tracks(items):
        for raw in items:
            track = raw.get("track", raw)
            tid = track.get("id")
            if tid and tid not in seen_ids:
                seen_ids.add(tid)
                all_tracks.append(track)

    print("Fetching all-time top tracks...")
    top_long = fetch_paged_tracks(token, "https://api.spotify.com/v1/me/top/tracks", limit=50, offset=0)
    add_tracks(top_long.get("items", []))

    print("Fetching recent top tracks...")
    top_med = fetch_paged_tracks(token, "https://api.spotify.com/v1/me/top/tracks", limit=50, offset=0)
    add_tracks(top_med.get("items", []))

    if len(all_tracks) < fetch_count:
        print("Fetching user saved / liked songs...")
        for offset in range(0, min(fetch_count, 150), 50):
            saved = fetch_paged_tracks(token, "https://api.spotify.com/v1/me/tracks", limit=50, offset=offset)
            items = saved.get("items", [])
            if not items:
                break
            add_tracks(items)

    formatted_all = format_track_items(all_tracks)
    print(f"\n[OK] Retrieved {len(formatted_all)} unique tracks from your Spotify library.")

    english_tracks = [
        t for t in formatted_all
        if is_english_music(t["name"], t["artists"], t.get("album", ""))
    ]
    print(f"[OK] Filtered {len(english_tracks)} English tracks.")

    if save_tracks:
        os.makedirs(DEFAULT_TRACKS_FILE.parent, exist_ok=True)
        with open(DEFAULT_TRACKS_FILE, "w", encoding="utf-8") as f:
            json.dump({"all_time_top_tracks": formatted_all}, f, indent=2, ensure_ascii=False)
        with open(DEFAULT_ENGLISH_TRACKS_FILE, "w", encoding="utf-8") as f:
            json.dump({"english_tracks": english_tracks}, f, indent=2, ensure_ascii=False)
        print(f"[OK] Saved tracks to {DEFAULT_TRACKS_FILE} & {DEFAULT_ENGLISH_TRACKS_FILE}")

    if update_lyrics and english_tracks:
        curated_eng = curate_english_lyrics(english_tracks)
        lines = [
            "# Curated English Tracks & Typography Lines\n",
            "*Extracted from Spotify listening history for wallpaper rendering.*\n\n---\n",
        ]
        for i, c in enumerate(curated_eng, 1):
            lines.append(f"\n### {i}. {c['title']} — {c['artist']}\n")
            lines.append(f"> *\"{c['lyric']}\"*\n")
            lines.append(f"- **Album**: {c['album']}\n")
            lines.append(f"- **Vibe**: English Alternative / Indie\n")

        with open(DEFAULT_ENGLISH_LYRICS_FILE, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print(f"[OK] Refreshed English lyrics file: {DEFAULT_ENGLISH_LYRICS_FILE}")

    return {
        "all_tracks": formatted_all,
        "english_tracks": english_tracks,
    }
