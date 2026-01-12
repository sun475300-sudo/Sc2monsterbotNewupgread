"""
AI Arena Ladder Game Runner

This module handles the connection to AI Arena's ladder server.
Required for proper ladder game execution.
"""

import sys
import json
import asyncio
from typing import Optional
from sc2 import run_game
from sc2.sc2process import SC2Process
from sc2.portconfig import Portconfig


def run_ladder_game(bot):
    """
    Run a ladder game by connecting to AI Arena's game server.

    Args:
        bot: sc2.player.Bot instance
    """

    # Parse command line arguments
    game_port = None
    start_port = None
    opponent_id = None

    for i, arg in enumerate(sys.argv):
        if arg == "--GamePort":
            game_port = int(sys.argv[i + 1])
        elif arg == "--StartPort":
            start_port = int(sys.argv[i + 1])
        elif arg == "--OpponentId":
            opponent_id = sys.argv[i + 1]

    if game_port is None or start_port is None:
        raise ValueError("Missing required ladder arguments: --GamePort and --StartPort")

    print(f"🔌 Connecting to ladder server:")
    print(f"   Game Port: {game_port}")
    print(f"   Start Port: {start_port}")
    if opponent_id:
        print(f"   Opponent ID: {opponent_id}")

    # Set up port configuration
    portconfig = Portconfig()
    portconfig.shared = game_port - 1
    portconfig.server = [game_port, game_port + 1]
    portconfig.players = [[start_port, start_port + 1]]

    # Run the game
    try:
        run_game(
            None,  # Map is provided by ladder server
            [bot],
            realtime=False,
            portconfig=portconfig,
            save_replay_as=None,
            game_time_limit=(60 * 20),  # 20 minute time limit
            rgb_render_config=None
        )
        print("✅ Ladder game completed")

    except Exception as e:
        print(f"❌ Ladder game error: {e}")
        import traceback
        traceback.print_exc()
        raise


def test_connection():
    """Test connection to AI Arena (for debugging)."""
    print("Testing AI Arena connection...")
    print(f"Python version: {sys.version}")

    try:
        import sc2
        print(f"✅ sc2 library version: {sc2.__version__}")
    except:
        print("❌ sc2 library not found")

    try:
        import aiohttp
        print(f"✅ aiohttp library available")
    except:
        print("⚠️ aiohttp library not found (optional)")

    print("Command line arguments:", sys.argv)


if __name__ == "__main__":
    test_connection()
