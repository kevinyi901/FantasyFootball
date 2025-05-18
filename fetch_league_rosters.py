"""
fetch_league_rosters.py

Fetch all rosters for a given Sleeper league.

This module provides:
  - fetch_league_rosters(league_id): Retrieves a list of roster dicts for the league.
Usage:
  python fetch_league_rosters.py
"""
import requests

LEAGUE_ROSTERS_URL = "https://api.sleeper.app/v1/league/{league_id}/rosters"

def fetch_league_rosters(league_id):
    """
    Fetch and return the roster list for the given Sleeper league.
    Each item is a dict:
      {
        "roster_id": int,
        "owners": [<user_id>, …],
        "players": [<player_id>, …]
      }
    """
    url = LEAGUE_ROSTERS_URL.format(league_id=league_id)
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

if __name__ == "__main__":
    # Replace with your actual league ID
    league_id = "123456789012345678"
    rosters = fetch_league_rosters(league_id)
    print(f"Found {len(rosters)} rosters in league {league_id}")
