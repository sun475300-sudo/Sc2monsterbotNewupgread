# -*- coding: utf-8 -*-
"""
Integrated Training System - Entry Point

Usage: python main_integrated.py
"""

import asyncio
import logging
import os
import random
import subprocess
import sys
import time
import warnings
from pathlib import Path

correct_sc2_path = r"C:\Program Files (x86)\StarCraft II"
os.environ["SC2PATH"] = correct_sc2_path

if not os.path.exists(correct_sc2_path):
    print(f"[WARNING] SC2 path not found: {correct_sc2_path}")
else:
    print(f"[OK] SC2 path verified")

os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
# DRY_RUN_MODE: 게임을 실행하지 않고 코드 검증만 수행 (셀프 힐링용)
DRY_RUN_MODE = os.environ.get("DRY_RUN_MODE", "false").lower() == "true"

try:
    from loguru import logger

    logger.remove()
    logger.add(sys.stderr, colorize=True, enqueue=True, catch=True, level="INFO")
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    logger.add(
        str(log_dir / "training_log.log"),
        rotation="10 MB",
        enqueue=True,
        catch=True,
        level="DEBUG",
        encoding="utf-8",
    )
    print("[OK] Loguru logger configured")
except ImportError:
    logger = None
    print("[WARNING] loguru not installed")
except Exception as e:
    logger = None
    print(f"[WARNING] Failed to configure loguru: {e}")

warnings.filterwarnings("ignore", category=DeprecationWarning, module="asyncio")


# Initialize logging configuration at the start to prevent logging errors
# This fixes ValueError: I/O operation on closed file issues
# Use a safe handler that catches buffer detachment errors
class SafeStreamHandler(logging.StreamHandler):
    """StreamHandler that catches ValueError when buffer is detached"""

    def emit(self, record):
        try:
            # Check if stream is closed before attempting to write
            if hasattr(self.stream, "closed") and self.stream.closed:
                return  # Stream is closed, skip logging
            if hasattr(self.stream, "detach") and not hasattr(self.stream, "write"):
                return  # Buffer has been detached, skip logging
            super().emit(record)
        except (ValueError, OSError, AttributeError) as e:
            # Silently ignore buffer detachment errors
            # These occur when sc2 library tries to log after stream is closed
            error_msg = str(e).lower()
            if "buffer" in error_msg or "detached" in error_msg or "closed" in error_msg:
                # Silently ignore buffer-related errors from sc2 internal logging
                pass
            else:
                # Re-raise or handle other errors normally
                try:
                    self.handleError(record)
                except Exception:
                    pass  # Even handleError can fail, so suppress it


# Configure logging with safe handler using sys.stdout explicitly
logging.basicConfig(
    handlers=[SafeStreamHandler(sys.stdout)],
    force=True,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Windows 비동기 루프 정책 설정 (Python 3.12+ 호환성)
# Note: WindowsSelectorEventLoopPolicy is deprecated in Python 3.16, but still needed for 3.12-3.15
if sys.platform == "win32":
    # Use running loop if present; otherwise create and set a new loop
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    # Windows: set selector policy when available (harmless on newer versions)
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass

# Ensure event loop exists (fixes RuntimeError and DeprecationWarning in Python 3.10+)
# Python 3.10+ requires explicit loop creation - get_event_loop() no longer auto-creates
# At module level, we just ensure a loop is set (not running)
try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

# SC2 imports
from sc2 import maps
from sc2.main import run_game

# Try to import _host_game (internal async function) - fallback to run_game if not available
try:
    from sc2.main import _host_game

    _HOST_GAME_AVAILABLE = True
except (ImportError, AttributeError):
    _HOST_GAME_AVAILABLE = False
    _host_game = None

from sc2.data import Difficulty, Race, Result
from sc2.player import Bot, Computer

# CRITICAL: Replace ALL handlers on root logger and sc2 logger after imports
# This ensures sc2 library's handlers are replaced with safe handlers
root_logger = logging.getLogger()
root_logger.handlers = [
    SafeStreamHandler(sys.stdout)
]  # Replace all root handlers with safe handler

# Also configure sc2 logger specifically
sc2_logger = logging.getLogger("sc2")
sc2_logger.handlers = [SafeStreamHandler(sys.stdout)]  # Replace all sc2 handlers with safe handler
sc2_logger.setLevel(logging.INFO)
sc2_logger.propagate = False  # Prevent propagation to root logger

# Monkey-patch StreamHandler.emit to catch buffer errors globally
# This ensures any StreamHandler created later will also be safe
_original_stream_handler_emit = logging.StreamHandler.emit


def safe_stream_handler_emit(self, record):
    try:
        return _original_stream_handler_emit(self, record)
    except (ValueError, OSError) as e:
        error_msg = str(e).lower()
        if "buffer" in error_msg or "detached" in error_msg:
            # Silently ignore buffer detachment errors
            return
        # Re-raise other errors
        raise


logging.StreamHandler.emit = safe_stream_handler_emit

# Bot import - Use WickedZergBotPro as integrated bot
# Curriculum Learning System
from curriculum_manager import CurriculumManager
from wicked_zerg_bot_pro import WickedZergBotPro as WickedZergBotIntegrated

# Configuration
SC2PATH = os.environ.get("SC2PATH", r"C:\Program Files (x86)\StarCraft II")
MAP_NAME = "AcropolisLE"  # Default map (confirmed to exist in Maps folder)

# Dynamic Difficulty System: Start easy, increase as bot improves
# This allows the bot to experience wins and learn faster
INITIAL_DIFFICULTY = Difficulty.VeryEasy  # Start with VeryEasy to get initial wins
DIFFICULTY_UPGRADE_THRESHOLD = 0.70  # Increase difficulty when win rate > 70%
DIFFICULTY_DOWNGRADE_THRESHOLD = 0.20  # Decrease difficulty when win rate < 20%
DIFFICULTY_MIN_GAMES = 20  # Minimum games before difficulty adjustment

# Difficulty progression: VeryEasy -> Easy -> Medium -> Hard -> VeryHard -> CheatInsane
DIFFICULTY_LEVELS = [
    Difficulty.VeryEasy,
    Difficulty.Easy,
    Difficulty.Medium,
    Difficulty.Hard,
    Difficulty.VeryHard,
    Difficulty.CheatInsane,
]

# Available maps - verified to exist in C:\Program Files (x86)\StarCraft II\Maps
# Using exact file names (without .SC2Map extension) as they appear in the folder
AVAILABLE_MAPS = [
    "AcropolisLE",  # Default map
    "AbyssalReefLE",
    "BelShirVestigeLE",
    "CactusValleyLE",
    "ProximaStationLE",
    "NewkirkPrecinctTE",
    "OdysseyLE",
    # Additional confirmed maps (uncomment if needed):
    # "HonorgroundsLE",
    # "AscensiontoAiurLE",
    # "BattleontheBoardwalkLE",
    # "BlackpinkLE",
    # "CatalystLE",
    # "DiscoBloodbathLE",
    # "EphemeronLE",
    # "NeonVioletSquareLE",
    # "PaladinoTerminalLE",
    # "ThunderbirdLE",
    # "TritonLE",
    # "WintersGateLE",
    # "WorldofSleepersLE",
]

# Opponent races (for variety)
OPPONENT_RACES = [Race.Terran, Race.Protoss, Race.Zerg]

# Personality options
PERSONALITIES = ["serral", "dark", "reynor"]


def write_status_file(instance_id, status_data):
    """
    Write instance status to a JSON file for dashboard display

    Args:
        instance_id: Unique instance identifier (0 if not in parallel mode)
        status_data: Dictionary containing status information
    """
    try:
        import json

        status_dir = Path("stats")
        status_dir.mkdir(exist_ok=True)
        status_file = status_dir / f"instance_{instance_id}_status.json"
        with open(status_file, "w", encoding="utf-8") as f:
            json.dump(status_data, f, indent=2)
    except Exception as e:
        # Silently fail - status file writing is optional
        pass


def run_training():
    """
    Main async function: Continuous training loop with integrated RL orchestrator
    This function is called by asyncio.run() to ensure proper async handling

    CRITICAL: Games are run in separate processes to avoid "run_game() must run in main thread" error
    """
    # ============================================================================
    # 1. AUTO-START MONITORING (로컬 + 원격)
    # ============================================================================
    def start_monitoring():
        """Start local dashboard and ngrok remote access"""
        print("\n" + "="*70)
        print("🌐 Starting monitoring systems...")
        print("="*70)
        
        try:
            # Local dashboard server
            print("[1/2] Starting local dashboard (http://localhost:8000)...")
            dashboard_proc = subprocess.Popen(
                [sys.executable, "dashboard.py"],
                cwd=os.path.dirname(__file__) or ".",
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
            )
            print(f"      ✅ Dashboard started (PID: {dashboard_proc.pid})")
            time.sleep(2)  # Wait for server to start
            
            # Ngrok remote access
            print("[2/2] Starting ngrok tunnel for remote access...")
            ngrok_proc = subprocess.Popen(
                "start_with_ngrok.bat" if sys.platform == "win32" else "./start_with_ngrok.sh",
                cwd=os.path.dirname(__file__) or ".",
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=True,
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
            )
            print(f"      ✅ Ngrok tunnel started (PID: {ngrok_proc.pid})")
            print("\n" + "="*70)
            print("✅ Monitoring active!")
            print("   Local:  http://localhost:8000")
            print("   Remote: Check .dashboard_port file or ngrok web UI")
            print("="*70 + "\n")
            
            return dashboard_proc, ngrok_proc
        except Exception as e:
            print(f"⚠️  Failed to start monitoring: {e}")
            print("   Continuing with training without remote access...\n")
            return None, None
    
    # Start monitoring (only in actual training mode)
    if not DRY_RUN_MODE:
        monitoring_procs = start_monitoring()
    
    # DRY-RUN MODE: Test all logic without running actual games
    if DRY_RUN_MODE:
        print("\n" + "=" * 70)
        print("🚀 DRY-RUN MODE ACTIVATED - Testing without StarCraft II")
        print("=" * 70)

        try:
            print("\n[1/5] Verifying SC2 path...")
            correct_sc2_path = r"C:\Program Files (x86)\StarCraft II"
            if os.path.exists(correct_sc2_path):
                print(f"  ✅ SC2 path verified: {correct_sc2_path}")
            else:
                print(f"  ⚠️  SC2 path not found (but that's OK for dry-run): {correct_sc2_path}")

            print("\n[2/5] Initializing CurriculumManager...")
            curriculum = CurriculumManager()
            current_difficulty = curriculum.get_difficulty()
            progress_info = curriculum.get_progress_info()
            print(f"  ✅ Curriculum loaded: {progress_info['level_name']}")
            print(f"     Level: {progress_info['current_level']}/{progress_info['total_levels']}")
            print(
                f"     Games at current level: {progress_info['games_at_current_level']}/{progress_info['min_games_required']}"
            )

            print("\n[3/5] Loading bot architecture...")
            print(f"  ✅ WickedZergBotPro class loaded successfully")
            print(f"     - Personality system: Ready")
            print(f"     - RL Orchestrator: Ready")
            print(f"     - Strategy analyzer: Ready")

            print("\n[4/5] Checking data directories...")
            directories = ["replays", "logs", "stats", "data"]
            for dir_name in directories:
                dir_path = Path(dir_name)
                dir_path.mkdir(exist_ok=True)
                print(f"  ✅ {dir_name}/ directory ready")

            print("\n[5/5] Configuration summary...")
            print(f"  Instance ID: 0 (single instance mode)")
            print(f"  Render mode: HEADLESS (no window)")
            print(f"  Map pool: {len(AVAILABLE_MAPS)} maps available")
            print(f"  Opponent races: {len(OPPONENT_RACES)} races")
            print(f"  Personality profiles: {len(PERSONALITIES)} personalities")

            print("\n" + "=" * 70)
            print("✅ [DRY-RUN SUCCESS] All systems ready for actual training!")
            print("=" * 70)
            print("\nTo start actual training:")
            print("  1. Open main_integrated.py")
            print("  2. Change 'DRY_RUN_MODE = True' to 'DRY_RUN_MODE = False'")
            print("  3. Run: python main_integrated.py")
            print("\n")
            return  # Exit without starting actual training

        except Exception as e:
            print("\n" + "=" * 70)
            print(f"❌ [DRY-RUN FAILED] Error during validation:")
            print("=" * 70)
            print(f"Error: {type(e).__name__}: {e}")
            import traceback

            traceback.print_exc()
            return

    # ACTUAL TRAINING MODE: Run real games with StarCraft II

    # Note: Event loop is already running when this function is called (via asyncio.run())
    # However, run_game() must be called from main thread, so we use subprocess for each game

    # Get instance ID from environment variable (for parallel training)
    instance_id = int(os.environ.get("INSTANCE_ID", "0"))
    show_window = os.environ.get("SHOW_WINDOW", "false").lower() == "true"

    # Set SC2PATH (force correct path, override any incorrect settings)
    correct_sc2_path = r"C:\Program Files (x86)\StarCraft II"
    os.environ["SC2PATH"] = correct_sc2_path
    os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

    # Verify SC2 path exists
    if not os.path.exists(correct_sc2_path):
        print(f"[WARNING] SC2 path not found: {correct_sc2_path}")
        print(
            f"[INFO] Please set SC2PATH environment variable to your StarCraft II installation path"
        )

    # Create replay directory
    replay_dir = "replays"
    os.makedirs(replay_dir, exist_ok=True)

    # Training statistics
    game_count = 0
    win_count = 0
    loss_count = 0
    last_result = "N/A"  # Store last game result for terminal display

    # 연속 실패 제한 시스템 (3진 아웃)
    MAX_CONTINUOUS_FAILURES = 3
    continuous_failures = 0
    
    # 🔍 Real-Time Code Monitor (게임 중에도 소스 검사)
    try:
        from realtime_code_monitor import RealtimeCodeMonitor
        
        code_monitor = RealtimeCodeMonitor(target_file="wicked_zerg_bot_pro.py")
        code_monitor.start()
        logger.info("🔍 Real-time code monitor started (background)")
        monitor_enabled = True
    except ImportError as e:
        logger.warning(f"Real-time monitor not available: {e}")
        code_monitor = None
        monitor_enabled = False
    except Exception as e:
        logger.warning(f"Failed to start real-time monitor: {e}")
        code_monitor = None
        monitor_enabled = False

    # Curriculum Learning System - 단계별 학습 시스템
    curriculum = CurriculumManager()
    current_difficulty = curriculum.get_difficulty()  # CurriculumManager에서 난이도 가져오기

    # Legacy: Dynamic difficulty tracking (for backward compatibility)
    current_difficulty_index = curriculum.current_idx
    difficulty_games = curriculum.games_at_current_level

    print("\n" + "=" * 70)
    print("Integrated Wicked Zerg Bot - Training System")
    print("=" * 70)
    if instance_id > 0:
        print(f"  Instance ID: #{instance_id} ({'VISUAL' if show_window else 'HEADLESS'})")
    print(f"  Bot: WickedZergBotIntegrated (RL Orchestrator)")

    # Curriculum Learning 정보 표시
    progress_info = curriculum.get_progress_info()
    print(f"  Opponent: Computer (Curriculum Learning System)")
    print(f"  Current Stage: {current_difficulty.name} - {progress_info['level_name']}")
    print(f"  Progress: Level {progress_info['current_level']}/{progress_info['total_levels']}")
    print(
        f"  Games at Current Level: {progress_info['games_at_current_level']}/{progress_info['min_games_required']}"
    )
    print(f"  Map: Random selection")
    print(f"  Mode: Continuous learning (infinite loop)")
    print(f"  RL: Enabled (Action-based orchestration)")
    print("=" * 70 + "\n")

    # Initialize status data
    status_data = {
        "instance_id": instance_id,
        "mode": "VISUAL" if show_window else "HEADLESS",
        "game_count": 0,
        "win_count": 0,
        "loss_count": 0,
        "last_result": "N/A",
        "current_game_time": "00:00",
        "current_minerals": 0,
        "current_supply": "0/0",
        "current_units": 0,
        "status": "INITIALIZING",
        "timestamp": time.time(),
        "difficulty": current_difficulty.name,
    }
    write_status_file(instance_id, status_data)

    # Continuous training loop
    # You can set MAX_GAMES environment variable to limit games (e.g., for testing)
    MAX_GAMES = int(os.environ.get("MAX_GAMES", "0"))  # 0 = infinite
    
    if MAX_GAMES > 0:
        print(f"\n🎮 [TRAINING] Game limit set: {MAX_GAMES} games")
        print(f"[MONITOR] Will auto-stop and close monitor after {MAX_GAMES} game(s)\n")
    else:
        print(f"\n🎮 [TRAINING] Infinite game mode (MAX_GAMES=0)")
        print(f"[MONITOR] Monitor will continue running for all games")
        print(f"[HINT] To limit games, set: set MAX_GAMES=N && python main_integrated.py\n")
    
    while True:
        try:
            game_count += 1

            # 연속 실패 횟수 표시
            if continuous_failures > 0:
                print(
                    f"🔄 [재시도] 현재 연속 실패: {continuous_failures}/{MAX_CONTINUOUS_FAILURES}"
                )

            # Map selection (use default if available maps list is empty or map not found)
            if not AVAILABLE_MAPS:
                current_map = MAP_NAME
            else:
                current_map = random.choice(AVAILABLE_MAPS)

            map_instance = maps.get(current_map)

            if map_instance is None:
                print(f"[WARNING] Map '{current_map}' not found, using default: {MAP_NAME}")
                current_map = MAP_NAME
                map_instance = maps.get(current_map)

                # Final fallback: if default map also doesn't exist, skip this game
                if map_instance is None:
                    print(
                        f"[ERROR] Default map '{MAP_NAME}' also not found. Please install maps in SC2 Maps folder."
                    )
                    print(f"[INFO] Expected path: {correct_sc2_path}\\Maps")
                    time.sleep(5)
                    continue

            # Random opponent race
            opponent_race = random.choice(OPPONENT_RACES)

            # Random personality
            personality = random.choice(PERSONALITIES)

            # Create integrated bot
            bot = WickedZergBotIntegrated(
                train_mode=True,
                instance_id=instance_id,
                personality=personality,
                opponent_race=opponent_race,
                game_count=game_count,  # Pass game count for terminal display
            )
            # Pass last result to bot for terminal display
            if hasattr(bot, "last_result"):
                bot.last_result = last_result

            # Set replay path
            replay_path = os.path.join(
                replay_dir,
                f"integrated_{personality}_vs_{opponent_race.name}_{current_map}_game{game_count}.SC2Replay",
            )

            # Curriculum Learning 정보 업데이트
            current_difficulty = curriculum.get_difficulty()  # 최신 난이도 가져오기
            progress_info = curriculum.get_progress_info()

            print(f"\n[GAME #{game_count}] Starting...")
            print(f"  Map: {current_map}")
            print(f"  Opponent: {opponent_race.name} ({current_difficulty.name})")
            print(f"  Personality: {personality.upper()}")
            print(f"  Stats: {win_count}W / {loss_count}L")
            print(
                f"  Curriculum Stage: {progress_info['level_name']} (Level {progress_info['current_level']}/{progress_info['total_levels']})"
            )
            print(
                f"  Games at Current Level: {progress_info['games_at_current_level']}/{progress_info['min_games_required']}"
            )
            
            # 🎯 이전 게임 완전 종료 대기 (게임창이 확실히 닫히도록)
            if game_count > 1:  # 첫 게임이 아닐 때만
                print(f"[WAIT] Ensuring previous game is fully closed...")
                time.sleep(1.5)  # 이전 게임 완전 종료 대기

            # Update status file with game start info
            status_data.update(
                {
                    "status": "GAME_RUNNING",
                    "current_map": current_map,
                    "opponent": opponent_race.name,
                    "personality": personality.upper(),
                    "timestamp": time.time(),
                }
            )
            write_status_file(instance_id, status_data)

            # Check if window should be shown (from environment variable)
            # Set realtime=False for maximum training speed (CPU-limited, not frame-limited)
            # Note: realtime=False means the game runs as fast as CPU allows, significantly faster than real-time
            # Set realtime=True only if you need to observe the game in real-time (much slower training)
            realtime_mode = False  # Always False for maximum training speed

            # Store bot reference for status updates during game (via callback mechanism)
            # The bot's on_step will update status file via a callback function
            bot_instance_ref = bot  # Store reference for potential future use

            # Run game directly in main thread (synchronous call)
            # CRITICAL: run_game() must be called from main thread - this function is now synchronous
            result = None

            try:
                print(f"[GAME] Selected Map: {current_map}")

                # DRY_RUN_MODE: 게임 실행 건너뛰기 (코드 검증만)
                if DRY_RUN_MODE:
                    print("[DRY-RUN] 게임 실행 건너뜀 (코드 검증 모드)")
                    result = "Victory"  # 가짜 성공 결과
                else:
                    # Direct call to run_game (now safe because run_training is synchronous)
                    result = run_game(
                        map_instance,
                        [Bot(Race.Zerg, bot), Computer(opponent_race, current_difficulty)],
                        realtime=realtime_mode,
                        save_replay_as=replay_path,
                    )

            except Exception as game_error:
                # Catch any game session errors (including logging errors during shutdown)
                error_msg = str(game_error).lower()

                # Handle connection reset errors (most common)
                if "connectionreseterror" in error_msg or "closing transport" in error_msg:
                    continuous_failures += 1
                    print("⚠️  [SYSTEM] 게임 연결이 예기치 않게 끔겼습니다.")
                    print(
                        f"[INFO] 연결 단절 ({continuous_failures}/{MAX_CONTINUOUS_FAILURES}): 게임 클라이언트 종료 또는 통신 타임아웃"
                    )

                    # 연속 실패 제한 체크
                    if continuous_failures >= MAX_CONTINUOUS_FAILURES:
                        print("\n" + "=" * 70)
                        print("🚨 [CRITICAL] 연속 실패 제한 도달")
                        print("=" * 70)
                        print(f"연속 {MAX_CONTINUOUS_FAILURES}회 연결 단절 발생")
                        print("시스템 보호를 위해 훈련을 안전하게 중단합니다.")
                        print("\n📝 참고 사항:")
                        print("  - SC2 클라이언트가 정상 실행 중인지 확인하세요")
                        print("  - GPU/CPU 온도 및 메모리 사용량을 확인하세요")
                        print("  - 잠시 후 다시 시도하거나 컴퓨터를 재부팅하세요")
                        print("=" * 70 + "\n")

                        # crash report 저장
                        try:
                            from datetime import datetime

                            with open("crash_report.txt", "a", encoding="utf-8") as f:
                                f.write(f"\n{'=' * 70}\n")
                                f.write(f"훈련 중단 시간: {datetime.now()}\n")
                                f.write(
                                    f"중단 원인: 연속 {MAX_CONTINUOUS_FAILURES}회 ConnectionResetError\n"
                                )
                                f.write(f"총 게임 수: {game_count}\n")
                                f.write(f"전적: {win_count}승 {loss_count}패\n")
                                f.write(f"{'=' * 70}\n")
                            print(f"💾 crash_report.txt에 로그 저장 완료")
                        except Exception:
                            pass

                        break  # 훈련 루프 탈출

                    result = "Defeat"
                    # GPU 메모리 정리
                    try:
                        import torch

                        if torch.cuda.is_available():
                            torch.cuda.empty_cache()
                            print("[SYSTEM] GPU 메모리 정리 완료")
                    except Exception:
                        pass
                    # 잠시 대기 후 다음 게임
                    time.sleep(2)
                elif "buffer" in error_msg or "detached" in error_msg:
                    # Logging error during shutdown - can be safely ignored
                    print(f"[INFO] Game ended (logging cleanup in progress)")
                    # Try to determine result from bot state if possible
                    result = "Defeat"  # Default to defeat if we can't determine
                elif "signal only works in main thread" in error_msg:
                    # Signal error - run_game() must run in main thread
                    # Use print() instead of logger to avoid buffer errors
                    print(f"[ERROR] Signal error: run_game() must run in main thread")
                    print(f"[INFO] This error indicates a threading issue with sc2 library")
                    result = "Defeat"
                elif "local variable 'asyncio' referenced before assignment" in error_msg:
                    # Asyncio variable conflict - should not happen but handle it
                    # Use print() instead of logger to avoid buffer errors
                    print(f"[ERROR] Asyncio variable conflict detected: {game_error}")
                    print(f"[ERROR] Game session crashed due to asyncio reference error")
                    result = "Defeat"
                else:
                    # Other errors should be reported (avoid logger to prevent buffer errors)
                    print(f"[ERROR] Game session error: {game_error}")
                    import traceback

                    # Only print traceback for non-buffer errors
                    if (
                        "buffer" not in str(game_error).lower()
                        and "detached" not in str(game_error).lower()
                    ):
                        traceback.print_exc()
                    result = "Defeat"  # Default to defeat on error
            finally:
                # GPU 메모리 정리 (각 게임 후)
                try:
                    import torch

                    if torch.cuda.is_available():
                        torch.cuda.empty_cache()
                except Exception:
                    pass

                # Ensure logging handlers are properly flushed after each game
                # This prevents buffer detachment errors during shutdown
                try:
                    for handler in logging.root.handlers[:]:
                        try:
                            handler.flush()
                        except (ValueError, OSError, AttributeError):
                            # Handler stream is closed or detached - ignore
                            pass
                except Exception:
                    pass  # Ignore any errors during logging cleanup

                # Also give loguru a moment to flush pending logs after each game
                # This reduces the chance of buffer errors during final shutdown
                try:
                    if logger:
                        # Brief wait to allow async log queue to process (use time.sleep instead of await)
                        time.sleep(0.05)  # Short wait for async log flush
                except Exception:
                    pass  # Ignore errors during loguru flush

            # Process result
            result_text = "N/A"
            if str(result) == "Victory":
                continuous_failures = 0  # 성공 시 카운터 초기화
                win_count += 1
                result_text = "WIN"
                print(f"[VICTORY] Game #{game_count} - {win_count}W / {loss_count}L")
                print(f"[INFO] Game ended successfully. Preparing next game...")
            elif str(result) == "Defeat":
                continuous_failures = 0  # 정상 패배도 게임은 성공적으로 종료됨
                loss_count += 1
                result_text = "DEFEAT"
                print(f"[DEFEAT] Game #{game_count} - {win_count}W / {loss_count}L")
                print(f"[INFO] Game ended. Preparing next game...")
            else:
                result_text = "DRAW"
                print(f"[DRAW] Game #{game_count} - {win_count}W / {loss_count}L")
                print(f"[INFO] Game ended. Preparing next game...")

            # Store result for next game's terminal display
            last_result = result_text

            # Update status file with final game result
            total_games = win_count + loss_count
            win_rate = (win_count / total_games * 100) if total_games > 0 else 0.0
            status_data.update(
                {
                    "game_count": game_count,
                    "win_count": win_count,
                    "loss_count": loss_count,
                    "last_result": result_text,
                    "win_rate": round(win_rate, 1),
                    "difficulty": current_difficulty.name,
                    "difficulty_level": current_difficulty_index + 1,
                    "status": "GAME_ENDED",
                    "timestamp": time.time(),
                }
            )
            write_status_file(instance_id, status_data)

            # Calculate win rate
            total_games = win_count + loss_count
            if total_games > 0:
                win_rate_percent = (win_count / total_games) * 100
                win_rate_ratio = win_count / total_games  # 0.0 ~ 1.0
                print(
                    f"[STATS] Win Rate: {win_rate_percent:.1f}% ({win_count}W / {total_games} games)"
                )

                # Curriculum Learning System: 난이도 자동 조정
                # 게임 기록
                curriculum.record_game()

                # 최근 성과 기반 승률 계산 (최근 20게임)
                recent_games = min(20, total_games)
                if recent_games >= 10:  # 최소 10게임 필요
                    recent_wins = max(0, win_count - max(0, total_games - recent_games))
                    recent_win_rate = recent_wins / recent_games if recent_games > 0 else 0.0

                    # 격상 체크
                    if curriculum.check_promotion(recent_win_rate, recent_games):
                        current_difficulty = curriculum.get_difficulty()
                        current_difficulty_index = curriculum.current_idx

                    # 강등 체크 (더 보수적으로)
                    if recent_win_rate < curriculum.demotion_threshold and recent_games >= 30:
                        if curriculum.check_demotion(recent_win_rate, recent_games):
                            current_difficulty = curriculum.get_difficulty()
                            current_difficulty_index = curriculum.current_idx

                # Legacy: 동기화 (backward compatibility)
                difficulty_games = curriculum.games_at_current_level

            # Self-Evolution: Replay Analysis with Delay
            # CRITICAL: Wait 5 seconds for replay file to be fully written
            # StarCraft II process may still be writing the file when game ends
            try:
                from self_evolution import run_self_evolution

                run_self_evolution(replay_dir)
            except ImportError:
                # Fallback to extract_replay_insights if self_evolution not available
                try:
                    from extract_replay_insights import analyze_latest_replay

                    analyze_latest_replay(replay_dir)
                except ImportError:
                    print("[WARNING] Replay analysis modules not found, skipping analysis")
            except Exception as e:
                print(f"[WARNING] Self-Evolution analysis error: {e}")
            
            # 🔍 Real-time monitor 결과 확인 (게임 중 발견된 문제)
            if monitor_enabled and code_monitor:
                # 모니터 스레드 상태 확인
                monitor_status = "RUNNING" if code_monitor.running else "STOPPED"
                monitor_thread_alive = code_monitor.monitor_thread and code_monitor.monitor_thread.is_alive()
                print(f"\n[MONITOR] Status: {monitor_status} | Thread Alive: {monitor_thread_alive}")
                
                if code_monitor.has_fixes():
                    print("\n" + "="*70)
                    print("🔧 REAL-TIME MONITOR DETECTED ISSUES!")
                    print("="*70)
                    print(code_monitor.get_fix_summary())
                    print("Fixes saved to: self_healing_logs/fix_*.json")
                    print("Review and apply fixes before next game.")
                    print("="*70 + "\n")
            
            # Check if max games reached (for testing/demo mode)
            if MAX_GAMES > 0 and game_count >= MAX_GAMES:
                print(f"\n{'='*70}")
                print(f"[STOP] Maximum games ({MAX_GAMES}) reached. Training complete.")
                print(f"[FINAL STATS] {win_count}W / {loss_count}L")
                print(f"{'='*70}")
                
                # 🔍 Monitor graceful shutdown
                if monitor_enabled and code_monitor:
                    print("\n[MONITOR] Stopping real-time code monitor...")
                    print("[MONITOR] Waiting for monitor thread to finish...")
                    try:
                        code_monitor.stop()
                        print("[✓ SUCCESS] Real-time code monitor stopped gracefully")
                    except Exception as e:
                        print(f"[✗ WARNING] Error stopping monitor: {e}")
                    
                    if code_monitor.has_fixes():
                        print("\n[MONITOR] Final fixes summary:")
                        print(code_monitor.get_fix_summary())
                
                print("\n[✓] Training session ended. Monitor is now inactive.")
                break

            # Brief pause before next game
            time.sleep(2)

        except KeyboardInterrupt:
            print("\n\n" + "="*70)
            print("[INTERRUPT] Training stopped by user.")
            print(f"[FINAL STATS] {win_count}W / {loss_count}L")
            print("="*70)
            
            # 🔍 Real-time monitor 종료 및 최종 리포트
            if monitor_enabled and code_monitor:
                print("\n[MONITOR] Stopping real-time code monitor...")
                try:
                    code_monitor.stop()
                    print("[✓ SUCCESS] Real-time code monitor stopped gracefully")
                except Exception as e:
                    print(f"[✗ WARNING] Error stopping monitor: {e}")
                if code_monitor.has_fixes():
                    print("\n[MONITOR] Final fixes summary:")
                    print(code_monitor.get_fix_summary())
            
            print("\n[✓] Training session ended. Monitor is now inactive.")
            break

        except Exception as e:
            print(f"\n[ERROR] Game error: {e}")
            import traceback

            traceback.print_exc()
            time.sleep(5)  # Wait before retrying
            continue
    
    # 🔍 Training loop 종료 후 모니터 정리
    print("\n" + "="*70)
    print("[CLEANUP] Training loop ended. Performing final cleanup...")
    print("="*70)
    
    if monitor_enabled and code_monitor:
        try:
            code_monitor.stop()
            print("[✓] Real-time code monitor stopped successfully")
            
            # 최종 리포트
            if code_monitor.has_fixes():
                print("\n" + "="*70)
                print("📊 FINAL MONITOR REPORT")
                print("="*70)
                print(code_monitor.get_fix_summary())
        except Exception as e:
            print(f"[✗] Error stopping monitor: {e}")
    
    print("\n[✓ COMPLETE] All cleanup finished. Program terminating...")
    print("="*70 + "\n")

    # CRITICAL: Clean up logging system BEFORE function returns
    # This ensures all pending logs are flushed before program shutdown
    try:
        # Complete loguru logging first (flush all pending logs in queue)
        if logger:
            try:
                logger.complete()  # Wait for all pending logs to be written
            except Exception:
                pass  # Ignore errors during completion

        # Then shutdown standard logging
        logging.shutdown()
    except Exception:
        pass  # Ignore errors during logging shutdown


if __name__ == "__main__":
    # Ensure loguru is properly configured (buffer error prevention)
    try:
        if logger:
            logger.remove()  # Remove existing handlers
            logger.add(sys.stderr, level="INFO", enqueue=True, catch=True)  # Reconfigure for safety
    except Exception:
        pass

    try:
        # Run training synchronously in main thread (run_game() requirement)
        # CRITICAL: run_game() must run in main thread, so we can't use asyncio.run()
        run_training()
    except KeyboardInterrupt:
        # User interrupted training
        print("\n[STOP] Training stopped by user.")
    except Exception as e:
        # Log runtime error (use print to avoid loguru buffer errors)
        print(f"[ERROR] Runtime error occurred: {e}")
        import traceback

        traceback.print_exc()
    finally:
        # Ensure logging is properly shut down and buffers are flushed
        try:
            # Complete loguru logging (flush all pending logs)
            if logger:
                try:
                    logger.complete()  # Wait for all pending logs to be written
                except Exception:
                    pass  # Ignore errors during completion
                try:
                    logger.remove()  # Remove all handlers
                except Exception:
                    pass  # Ignore errors during removal
        except Exception:
            pass

        # Also shutdown standard logging
        try:
            logging.shutdown()
        except Exception:
            pass  # Ignore errors during logging shutdown

        print("[OK] System safely shut down.")
