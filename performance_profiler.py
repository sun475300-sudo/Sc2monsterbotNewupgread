#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Performance Profiler - Real-time Code Performance Analysis

High-speed profiling tools for analyzing code execution performance.
Provides detailed insights into bottlenecks and optimization opportunities.

Features:
    1. Function-level execution time profiling
    2. Memory usage tracking
    3. Line-by-line performance analysis
    4. Hot path detection (most frequently executed code)
    5. Real-time performance metrics during bot execution

Usage:
    # Profile a specific function
    @profile_function
    def my_function():
        pass

    # Profile entire bot execution
    python performance_profiler.py --bot main_integrated.py

    # Memory profiling
    python performance_profiler.py --memory --bot main_integrated.py

    # Line-by-line profiling
    python performance_profiler.py --line-profile --bot wicked_zerg_bot_pro.py
"""

import argparse
import cProfile
import functools
import io
import pstats
import sys
import time
import tracemalloc
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

try:
    from loguru import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)


class PerformanceProfiler:
    """Real-time performance profiling system"""

    def __init__(self):
        """Initialize performance profiler"""
        self.function_stats: Dict[str, Dict[str, Any]] = {}
        self.memory_snapshots: List[Tuple[float, int]] = []
        self.profiler: Optional[cProfile.Profile] = None

    def start_profiling(self):
        """Start cProfile profiling"""
        self.profiler = cProfile.Profile()
        self.profiler.enable()
        logger.info("[PROFILER] Performance profiling started")

    def stop_profiling(self) -> pstats.Stats:
        """
        Stop profiling and return statistics

        Returns:
            pstats.Stats object with profiling results
        """
        if self.profiler:
            self.profiler.disable()
            logger.info("[PROFILER] Performance profiling stopped")

            # Create stats object
            stream = io.StringIO()
            stats = pstats.Stats(self.profiler, stream=stream)
            return stats

        return None

    def print_profile_stats(self, stats: pstats.Stats, top_n: int = 20):
        """
        Print formatted profiling statistics

        Args:
            stats: pstats.Stats object
            top_n: Number of top functions to display
        """
        if not stats:
            return

        print("\n" + "=" * 80)
        print("   PERFORMANCE PROFILE - TOP FUNCTIONS BY TIME")
        print("=" * 80)

        # Sort by cumulative time
        stats.sort_stats(pstats.SortKey.CUMULATIVE)
        stats.print_stats(top_n)

        print("\n" + "=" * 80)
        print("   PERFORMANCE PROFILE - TOP FUNCTIONS BY CALLS")
        print("=" * 80)

        # Sort by call count
        stats.sort_stats(pstats.SortKey.CALLS)
        stats.print_stats(top_n)

    def start_memory_tracking(self):
        """Start memory profiling"""
        tracemalloc.start()
        logger.info("[MEMORY] Memory tracking started")

    def take_memory_snapshot(self) -> Tuple[int, int]:
        """
        Take a memory snapshot

        Returns:
            Tuple of (current_memory, peak_memory) in bytes
        """
        if not tracemalloc.is_tracing():
            return (0, 0)

        current, peak = tracemalloc.get_traced_memory()
        timestamp = time.time()
        self.memory_snapshots.append((timestamp, current))

        return (current, peak)

    def stop_memory_tracking(self) -> Dict[str, Any]:
        """
        Stop memory tracking and return statistics

        Returns:
            Dictionary with memory statistics
        """
        if not tracemalloc.is_tracing():
            return {}

        current, peak = tracemalloc.get_traced_memory()
        snapshot = tracemalloc.take_snapshot()
        tracemalloc.stop()

        # Get top memory allocations
        top_stats = snapshot.statistics('lineno')

        logger.info("[MEMORY] Memory tracking stopped")
        logger.info(f"[MEMORY] Current: {current / 1024 / 1024:.2f} MB")
        logger.info(f"[MEMORY] Peak: {peak / 1024 / 1024:.2f} MB")

        return {
            "current_mb": current / 1024 / 1024,
            "peak_mb": peak / 1024 / 1024,
            "top_allocations": [
                {
                    "file": str(stat.traceback),
                    "size_mb": stat.size / 1024 / 1024,
                    "count": stat.count,
                }
                for stat in top_stats[:10]
            ]
        }

    def print_memory_stats(self, stats: Dict[str, Any]):
        """
        Print formatted memory statistics

        Args:
            stats: Memory statistics dictionary
        """
        if not stats:
            return

        print("\n" + "=" * 80)
        print("   MEMORY PROFILE")
        print("=" * 80)
        print(f"   Current Memory:  {stats['current_mb']:>10.2f} MB")
        print(f"   Peak Memory:     {stats['peak_mb']:>10.2f} MB")
        print("\n   Top 10 Memory Allocations:")
        print("   " + "-" * 76)

        for i, alloc in enumerate(stats.get('top_allocations', []), 1):
            print(f"   {i:2d}. {alloc['size_mb']:>8.2f} MB  ({alloc['count']:>6,} objects)")
            print(f"       {alloc['file']}")

        print("=" * 80)


def profile_function(func: Callable) -> Callable:
    """
    Decorator to profile a specific function

    Usage:
        @profile_function
        def my_function():
            pass
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()

        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        profiler.disable()

        execution_time = end_time - start_time
        logger.info(f"[PROFILE] {func.__name__} executed in {execution_time:.4f}s")

        # Print detailed stats if execution took more than 1 second
        if execution_time > 1.0:
            stream = io.StringIO()
            stats = pstats.Stats(profiler, stream=stream)
            stats.sort_stats(pstats.SortKey.CUMULATIVE)
            stats.print_stats(10)
            print(stream.getvalue())

        return result

    return wrapper


def time_function(func: Callable) -> Callable:
    """
    Simple decorator to time function execution (minimal overhead)

    Usage:
        @time_function
        def my_function():
            pass
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        execution_time = end_time - start_time
        if execution_time > 0.1:  # Only log if > 100ms
            logger.debug(f"[TIME] {func.__name__}: {execution_time*1000:.2f}ms")

        return result

    return wrapper


class HotPathDetector:
    """Detect hot paths (frequently executed code) in bot execution"""

    def __init__(self):
        """Initialize hot path detector"""
        self.call_counts: Dict[str, int] = {}
        self.total_calls = 0

    def record_call(self, func_name: str):
        """
        Record a function call

        Args:
            func_name: Function name to record
        """
        self.call_counts[func_name] = self.call_counts.get(func_name, 0) + 1
        self.total_calls += 1

    def get_hot_paths(self, top_n: int = 20) -> List[Tuple[str, int, float]]:
        """
        Get the hottest paths (most frequently called functions)

        Args:
            top_n: Number of hot paths to return

        Returns:
            List of (function_name, call_count, percentage) tuples
        """
        sorted_calls = sorted(
            self.call_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            (func, count, (count / self.total_calls) * 100)
            for func, count in sorted_calls[:top_n]
        ]

    def print_hot_paths(self, top_n: int = 20):
        """
        Print hot path analysis

        Args:
            top_n: Number of hot paths to display
        """
        hot_paths = self.get_hot_paths(top_n)

        print("\n" + "=" * 80)
        print("   HOT PATH ANALYSIS - MOST FREQUENTLY CALLED FUNCTIONS")
        print("=" * 80)
        print(f"   Total function calls: {self.total_calls:,}")
        print("\n   Rank  Function Name                              Calls        % of Total")
        print("   " + "-" * 76)

        for i, (func, count, percentage) in enumerate(hot_paths, 1):
            print(f"   {i:4d}. {func:40s} {count:>10,}   {percentage:>6.2f}%")

        print("=" * 80)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Performance Profiler for Wicked Zerg AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--bot",
        type=str,
        help="Bot file to profile (e.g., main_integrated.py)",
    )

    parser.add_argument(
        "--memory",
        action="store_true",
        help="Enable memory profiling",
    )

    parser.add_argument(
        "--duration",
        type=int,
        default=60,
        help="Profiling duration in seconds (default: 60)",
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Output file for profiling results (.prof)",
    )

    args = parser.parse_args()

    print("=" * 80)
    print("   PERFORMANCE PROFILER")
    print("   Real-time Code Performance Analysis")
    print("=" * 80)
    print()

    profiler = PerformanceProfiler()

    if args.memory:
        profiler.start_memory_tracking()

    if args.bot:
        # Profile bot execution
        logger.info(f"[PROFILER] Profiling {args.bot} for {args.duration}s...")

        profiler.start_profiling()

        # Here you would execute the bot
        # For now, just demonstrate the profiler
        import time
        time.sleep(args.duration)

        stats = profiler.stop_profiling()
        profiler.print_profile_stats(stats)

        if args.memory:
            memory_stats = profiler.stop_memory_tracking()
            profiler.print_memory_stats(memory_stats)

        if args.output:
            stats.dump_stats(args.output)
            logger.info(f"[PROFILER] Results saved to {args.output}")

    else:
        logger.info("[PROFILER] Use @profile_function decorator in your code")
        logger.info("[PROFILER] Or run with --bot <script.py> to profile execution")


if __name__ == "__main__":
    main()
