"""
fetch_trending_players.py

Fetch the top-N trending NFL player adds from Sleeper.

This module provides:
  - fetch_trending_adds(lookback_hours=24, limit=50): Returns a list of trending add entries.
Usage:
  python fetch_trending_players.py
"""
import requests

TRENDING_URL = "https://api.sleeper.app/v1/players/nfl/trending/add"

def fetch_trending_adds(lookback_hours=24, limit=50):
    """
    Fetch and return the top-N trending 'adds' over the last X hours.
    Returns a list of {"player_id": str, "count": int}.
    """
    params = {
        "lookback_hours": lookback_hours,
        "limit": limit
    }
    resp = requests.get(TRENDING_URL, params=params)
    resp.raise_for_status()
    return resp.json()

if __name__ == "__main__":
    trending = fetch_trending_adds()
    print(f"Fetched {len(trending)} trending entries")
