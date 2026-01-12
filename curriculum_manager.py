# -*- coding: utf-8 -*-

"""

================================================================================

                    Curriculum Learning System (curriculum_manager.py)

================================================================================

?ܰ躰 ?н?(Curriculum Learning) ?ý???



?ܰ??????? ???̵??? ???????? ?н??ϴ? ?ý????Դϴ?.

AI?? ó?????? ?е??????? ?ʰ?, ???? ???̵????? ?¸? ?????? ?????? ?????????? ???˴ϴ?.



?ٽ? ???:

    1. ?ܰ躰 ???̵? ???? (VeryEasy -> Easy -> Medium -> Hard -> VeryHard -> CheatInsane)

    2. ?·? ??? ?ڵ? ???̵? ????

    3. ?н? ?ܰ? ????/?ε?

    4. ???̵??? ?ּ? ???? ?? ???? (??????)

================================================================================

"""

import json
import os
from pathlib import Path

from sc2.data import Difficulty


class CurriculumManager:
    """

    Curriculum Learning Manager



    ?ܰ躰 ?н? ?ý????? ?????ϴ? Ŭ?????Դϴ?.

    ?·??? ???? ?ڵ????? ???̵??? ?????մϴ?.

    """

    def __init__(self, stats_file: str = "training_stats.json"):
        """

        Args:

            stats_file: ??? ???? ??? (?⺻: training_stats.json)

        """

        # ?????? ???丮 ????

        self.data_dir = Path("data")

        self.data_dir.mkdir(exist_ok=True)

        # ??? ???? ??? (data/ ???丮?? ????)

        self.stats_file = (
            self.data_dir / stats_file if not os.path.isabs(stats_file) else Path(stats_file)
        )

        # ?ܰ躰 ???̵? ???? (??????)

        self.levels = [
            Difficulty.VeryEasy,  # Stage 1: ???? ??ũ??
            Difficulty.Easy,  # Stage 2: ?⺻ ????
            Difficulty.Medium,  # Stage 3: ??? ????
            Difficulty.Hard,  # Stage 4: ?й? ????
            Difficulty.VeryHard,  # Stage 5: ????ȭ ???
            Difficulty.CheatInsane,  # Stage 6: ???? ???? (ġƮ)
        ]

        # ???? ?ܰ? ?ε??? ?ε?

        self.current_idx = self.load_level()

        # ?? ???̵??? ?ּ? ???? ?? (???????? ????)

        self.min_games_per_level = {
            0: 10,  # VeryEasy: ?ּ? 10????
            1: 15,  # Easy: ?ּ? 15????
            2: 20,  # Medium: ?ּ? 20????
            3: 25,  # Hard: ?ּ? 25????
            4: 30,  # VeryHard: ?ּ? 30????
            5: 40,  # CheatInsane: ?ּ? 40????
        }

        # ?·? ?Ӱ?ġ

        self.promotion_threshold = 0.80  # 80% ?·? ?̻? ?? ?ݻ?

        self.demotion_threshold = 0.20  # 20% ?·? ?̸? ?? ????

        # ???̵??? ???? ?? ????

        self.games_at_current_level = 0

    def load_level(self) -> int:
        """

        ????? ???Ͽ??? ???? ?ܰ踦 ?ҷ??ɴϴ?.



        Returns:

            int: ???? ?ܰ? ?ε??? (?⺻??: 0)

        """

        if not self.stats_file.exists():
            return 0

        # CRITICAL: Add timeout protection to prevent silent lock during module import
        # This is the #1 cause of "silent lock" (process hangs with no error message)
        import time

        start_time = time.time()
        timeout_seconds = 3  # 3-second timeout for import-phase file operations

        # Use a helper function that can be interrupted by timeout thread
        result_box = {"value": None, "complete": False}

        def load_with_timeout():
            """Load level with internal timeout check"""
            try:
                # Add retry logic for file locking issues
                max_retries = 2
                retry_delay = 0.05  # 50ms retry (much faster than before)

                for attempt in range(max_retries):
                    try:
                        # Check overall timeout
                        elapsed = time.time() - start_time
                        if elapsed > timeout_seconds:
                            print(
                                f"[CRITICAL] File read timeout after {elapsed:.2f}s, using default level (0)"
                            )
                            result_box["value"] = 0
                            return

                        # Use non-blocking file open with timeout
                        with open(self.stats_file, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            level_idx = data.get("curriculum_level_idx", 0)

                            # Validate index
                            if 0 <= level_idx < len(self.levels):
                                self.games_at_current_level = data.get("games_at_current_level", 0)
                                result_box["value"] = level_idx
                            else:
                                result_box["value"] = 0
                            return

                    except (IOError, OSError) as file_error:
                        # File is locked or access denied - retry
                        if attempt < max_retries - 1:
                            time.sleep(retry_delay)
                            continue
                        else:
                            print(
                                f"[WARNING] File read failed after {max_retries} retries: {file_error}"
                            )
                            result_box["value"] = 0
                            return

                    except json.JSONDecodeError as json_error:
                        # JSON is corrupted
                        print(f"[WARNING] Curriculum file is corrupted: {json_error}")
                        result_box["value"] = 0
                        return

            except Exception as e:
                print(f"[WARNING] Failed to load curriculum level: {e}")
                result_box["value"] = 0

            finally:
                result_box["complete"] = True

        # Execute with timeout safeguard
        try:
            load_with_timeout()

            # If function completed normally, return result
            if result_box["complete"]:
                return result_box["value"] if result_box["value"] is not None else 0
            else:
                # Should not happen with synchronous execution, but just in case
                print("[CRITICAL] Load operation did not complete")
                return 0

        except Exception as e:
            print(f"[CRITICAL] Unexpected error in load_level: {e}")
            return 0

    def save_level(self):
        """???? ?ܰ踦 ???Ͽ? ?????մϴ?."""

        try:
            # ???? ?????? ?ε? (?ٸ? ?????? ????)

            data = {}

            if self.stats_file.exists():
                try:
                    with open(self.stats_file, "r", encoding="utf-8") as f:
                        data = json.load(f)

                except:
                    pass

            # Curriculum ?????? ??????Ʈ

            data["curriculum_level_idx"] = self.current_idx

            data["games_at_current_level"] = self.games_at_current_level

            data["current_difficulty"] = self.get_difficulty().name

            # ????

            with open(self.stats_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

        except Exception as e:
            print(f"[WARNING] Failed to save curriculum level: {e}")

    def get_difficulty(self) -> Difficulty:
        """

        ???? ?ε????? ?´? Difficulty ??ü?? ??ȯ?մϴ?.



        Returns:

            Difficulty: ???? ???̵?

        """

        if 0 <= self.current_idx < len(self.levels):
            return self.levels[self.current_idx]

        else:
            return self.levels[0]  # ??????ġ: ?⺻?? ??ȯ

    def get_level_name(self) -> str:
        """???? ?ܰ? ?̸? ??ȯ"""

        difficulty_names = [
            "???? ??ũ??",
            "?⺻ ????",
            "??? ????",
            "?й? ????",
            "????ȭ ???",
            "???? ????",
        ]

        if 0 <= self.current_idx < len(difficulty_names):
            return difficulty_names[self.current_idx]

        return "???? ??ũ??"

    def check_promotion(self, win_rate: float, total_games: int) -> bool:
        """

        ?·??? ?Ӱ?ġ ?̻??̸? ???? ???̵??? ?ݻ?



        Args:

            win_rate: ?·? (0.0 ~ 1.0)

            total_games: ??ü ???? ??



        Returns:

            bool: ?ݻ? ????

        """

        # ???? ?ܰ?? ?? ?̻? ?ݻ? ?Ұ?

        if self.current_idx >= len(self.levels) - 1:
            return False

        # ???? ???̵??? ?ּ? ???? ?? Ȯ??

        min_games = self.min_games_per_level.get(self.current_idx, 10)

        if self.games_at_current_level < min_games:
            return False  # ?ּ? ???? ?? ?̴?

        # ?·? ?Ӱ?ġ Ȯ??

        if win_rate >= self.promotion_threshold:
            # ?ݻ?

            self.current_idx += 1

            self.games_at_current_level = 0  # ?? ???̵? ???? ?? ?ʱ?ȭ

            self.save_level()

            print(f"\n{'=' * 70}")

            print(f"? [CURRICULUM LEVEL UP]")

            print(
                f"  ???? ?ܰ?: {self.levels[self.current_idx - 1].name} ({self.get_level_name_from_idx(self.current_idx - 1)})"
            )

            print(
                f"  ???ο? ?ܰ?: {self.levels[self.current_idx].name} ({self.get_level_name_from_idx(self.current_idx)})"
            )

            print(f"  ?·?: {win_rate * 100:.1f}% (?ݻ? ?Ӱ?ġ: {self.promotion_threshold * 100:.0f}%)")

            print(f"{'=' * 70}\n")

            return True

        return False

    def check_demotion(self, win_rate: float, total_games: int) -> bool:
        """

        ?·??? ?Ӱ?ġ ?̸??̸? ???? ???̵??? ????



        Args:

            win_rate: ?·? (0.0 ~ 1.0)

            total_games: ??ü ???? ??



        Returns:

            bool: ???? ????

        """

        # ù ?ܰ?? ?? ?̻? ???? ?Ұ?

        if self.current_idx <= 0:
            return False

        # ???? ???̵??? ?ּ? ???? ?? Ȯ??

        min_games = self.min_games_per_level.get(self.current_idx, 10)

        if self.games_at_current_level < min_games:
            return False  # ?ּ? ???? ?? ?̴? (???? ???? ????? ?õ??ؾ? ??)

        # ?·? ?Ӱ?ġ Ȯ?? (???? ???? ?????? ???? ?? ?????? ????)

        if win_rate < self.demotion_threshold and total_games >= 30:
            # ????

            self.current_idx -= 1

            self.games_at_current_level = 0  # ?? ???̵? ???? ?? ?ʱ?ȭ

            self.save_level()

            print(f"\n{'=' * 70}")

            print(f"?? [CURRICULUM LEVEL DOWN]")

            print(
                f"  ???? ?ܰ?: {self.levels[self.current_idx + 1].name} ({self.get_level_name_from_idx(self.current_idx + 1)})"
            )

            print(
                f"  ???ο? ?ܰ?: {self.levels[self.current_idx].name} ({self.get_level_name_from_idx(self.current_idx)})"
            )

            print(f"  ?·?: {win_rate * 100:.1f}% (???? ?Ӱ?ġ: {self.demotion_threshold * 100:.0f}%)")

            print(f"{'=' * 70}\n")

            return True

        return False

    def record_game(self):
        """???? ???̵????? ???? ?? ?? ???"""

        self.games_at_current_level += 1

        self.save_level()

    def get_level_name_from_idx(self, idx: int) -> str:
        """?ε????? ?ܰ? ?̸? ??ȯ"""

        difficulty_names = [
            "???? ??ũ??",
            "?⺻ ????",
            "??? ????",
            "?й? ????",
            "????ȭ ???",
            "???? ????",
        ]

        if 0 <= idx < len(difficulty_names):
            return difficulty_names[idx]

        return "???? ??ũ??"

    def get_progress_info(self) -> dict:
        """???? ???? ??Ȳ ???? ??ȯ"""

        current_difficulty = self.get_difficulty()

        min_games = self.min_games_per_level.get(self.current_idx, 10)

        return {
            "current_level": self.current_idx + 1,
            "total_levels": len(self.levels),
            "current_difficulty": current_difficulty.name,
            "level_name": self.get_level_name(),
            "games_at_current_level": self.games_at_current_level,
            "min_games_required": min_games,
            "promotion_threshold": self.promotion_threshold,
            "demotion_threshold": self.demotion_threshold,
        }
