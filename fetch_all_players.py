"""
fetch_all_players.py

Module: fetch_all_players

Description:
    Retrieves the full NFL player roster from the Sleeper API as a JSON mapping.

Features:
    - Sends a GET request to the public Sleeper endpoint for all NFL players.
    - Returns a dict keyed by player_id, with detailed player data (name, team, position, etc.).
    - Can be used as a standalone script or imported as a module.

Dependencies:
    - requests

Usage (imported):
    from fetch_all_players import fetch_all_players
    players = fetch_all_players()

Usage (CLI):
    python fetch_all_players.py

Output (CLI):
    Prints the total count of players fetched.

Functions:
    fetch_all_players():
        Fetches and returns the full player roster as a dict.

Author:
    Kevin Yi
    Date: 2025-05-17
"""
# fetch_all_players.py

import requests, os, json, time

ALL_PLAYERS_URL = "https://api.sleeper.app/v1/players/nfl"
CACHE_FILE    = "all_players_cache.json"
CACHE_TTL     = 24 * 60 * 60   # seconds

def fetch_all_players(force_refresh=False):
    """
    Fetch and return the full NFL player roster from Sleeper.
    Caches to disk for CACHE_TTL seconds by default.
    """
    # if cache exists and is fresh, load it
    if not force_refresh and os.path.exists(CACHE_FILE):
        age = time.time() - os.path.getmtime(CACHE_FILE)
        if age < CACHE_TTL:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)

    # otherwise fetch from API and write cache
    resp = requests.get(ALL_PLAYERS_URL)
    resp.raise_for_status()
    data = resp.json()
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f)
    return data

if __name__ == "__main__":
    players = fetch_all_players()
    print(f"Fetched {len(players)} players (cached to {CACHE_FILE})")
