"""
map_available_trending_players.py

Module: map_available_trending_players

Description:
    Combines full NFL player data, trending add counts, and league roster
    information from the Sleeper API to identify trending players who are
    not yet on any roster in a specified league.

Features:
    - Fetches full NFL player roster (large payload) with optional local caching.
    - Retrieves trending player "adds" over a configurable lookback window.
    - Loads league rosters to filter out already drafted players.
    - Enriches each player record with metadata (name, team, position) and trending_count.

Dependencies:
    - requests

Usage:
    python map_available_trending_players.py \
        --league_id LEAGUE_ID [--lookback_hours HOURS] [--limit N]

Arguments:
    --league_id      (str, required)  Sleeper league ID to fetch rosters from.
    --lookback_hours (int, optional)  Time window in hours for trending adds (default: 24).
    --limit          (int, optional)  Maximum number of trending players to fetch (default: 50).

Example:
    python map_available_trending_players.py \
        --league_id 123456789012345678 \
        --lookback_hours 12 \
        --limit 30

Output:
    Prints to stdout a list of trending players not yet on any roster in the
    target league, formatted as:
        - First Last (POSITION @ TEAM): X adds

Functions:
    get_available_trending(league_id, lookback_hours=24, limit=50)
        Return a list of player dicts enriched with 'trending_count' for all
        trending players not rostered in the given league.

    main()
        Parses CLI arguments, invokes get_available_trending, and prints the results.

Author:
    Kevin Yi
    Date: 2025-05-17
"""


import argparse
from fetch_all_players import fetch_all_players
from fetch_trending_players import fetch_trending_adds
from fetch_league_rosters import fetch_league_rosters


def get_available_trending(league_id, lookback_hours=24, limit=50):
    """
    Return a list of full player dicts (from all_players),
    each enriched with "trending_count", but only for those
    NOT already on any roster in the specified league.
    """
    all_players = fetch_all_players()
    trending = fetch_trending_adds(lookback_hours, limit)
    rosters = fetch_league_rosters(league_id)

    # collect every drafted player_id
    drafted = set()
    for roster in rosters:
        drafted.update(roster.get("players", []))

    available = []
    for entry in trending:
        pid = entry["player_id"]
        if pid in drafted:
            continue
        player = all_players.get(pid)
        if not player:
            continue
        player_with_trend = {**player, "trending_count": entry["count"]}
        available.append(player_with_trend)

    return available


def main():
    parser = argparse.ArgumentParser(
        description="List trending available players for a Sleeper league"
    )
    parser.add_argument(
        "--league_id", required=True,
        help="Sleeper league ID"
    )
    parser.add_argument(
        "--lookback_hours", type=int, default=24,
        help="Lookback window in hours for trending adds"
    )
    parser.add_argument(
        "--limit", type=int, default=50,
        help="Number of trending players to fetch"
    )
    args = parser.parse_args()

    available = get_available_trending(
        args.league_id,
        args.lookback_hours,
        args.limit
    )

    print(f"\nTrending players NOT yet on a roster "
          f"(top {args.limit} adds) in league {args.league_id} "
          f"over last {args.lookback_hours}h:\n")
    for p in available:
        name = f"{p.get('first_name','')} {p.get('last_name','')}"
        print(f"- {name} ({p.get('position')} @ {p.get('team')}): {p['trending_count']} adds")

if __name__ == "__main__":
    main()
