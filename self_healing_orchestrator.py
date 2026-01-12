#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Self-Healing Orchestrator with Vertex AI (Enterprise Edition)

Automated bug detection and fixing loop using Google Cloud Vertex AI:
1. Code execution attempt
2. Error detection via stderr
3. Analysis and fixing via Vertex AI Gemini API (Pro/Ultra models)
4. Automatic file update with backup
5. Re-execution for validation
6. Repeat until success or max attempts reached

Advantages over free tier:
- 2M token context window (full project analysis)
- Pro/Ultra models for complex reasoning
- Enterprise security and data privacy
- No rate limiting issues
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path

# Load .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # If python-dotenv not installed, load manually
    env_path = Path(".env")
    if env_path.exists():
        for line in env_path.read_text().strip().split("\n"):
            if line and not line.startswith("#"):
                key, val = line.split("=", 1)
                os.environ[key.strip()] = val.strip()

from typing import Optional, Tuple

# Fix protobuf compatibility issue (must be before vertexai import)
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting
from loguru import logger

# Configuration
MAX_FIX_ATTEMPTS = 5
EXECUTION_TIMEOUT = 300  # Increased to 5 minutes for game execution
LOG_DIR = Path("self_healing_logs")
LOG_DIR.mkdir(exist_ok=True)

# GCP Configuration (Vertex AI)
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", None)
GCP_LOCATION = os.getenv("GCP_LOCATION", "us-central1")

# Fallback: Try to auto-detect project ID
if not GCP_PROJECT_ID:
    try:
        import google.auth
        _, GCP_PROJECT_ID = google.auth.default()
    except:
        pass

# Logging setup
logger.remove()
logger.add(
    sink=sys.stderr,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>",
    level="INFO"
)
logger.add(
    sink=LOG_DIR / f"healing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
    level="DEBUG"
)


def load_full_project_context(project_dir: Path, max_files: int = 50) -> str:
    """Load full project context for enterprise-grade analysis

    Vertex AI supports 2M tokens, so we can include:
    - All manager files (economy, production, combat, etc.)
    - Tech advancement and unit factory
    - Intel/scouting systems
    - Config and utilities

    Args:
        project_dir: Project root directory
        max_files: Maximum number of Python files to include (Vertex AI: can use 50+)

    Returns:
        Concatenated project context as string with file boundaries
    """
    context_parts = [
        "# ============================================",
        "# FULL PROJECT CONTEXT (Vertex AI Enterprise)",
        "# ============================================",
        f"# Generated: {datetime.now().isoformat()}",
        "# This context includes the entire codebase for comprehensive analysis",
        "",
    ]

    py_files = sorted(project_dir.glob("*.py"))[:max_files]

    logger.info(f"[VERTEX AI] Loading context from {len(py_files)} Python files...")

    for py_file in py_files:
        try:
            content = py_file.read_text(encoding="utf-8")
            context_parts.append(f"\n{'='*60}")
            context_parts.append(f"FILE: {py_file.name}")
            context_parts.append(f"SIZE: {len(content)} characters")
            context_parts.append(f"{'='*60}\n")
            context_parts.append(content)  # Include FULL file for enterprise analysis
        except Exception as e:
            logger.warning(f"Failed to load {py_file.name}: {e}")
            continue

    full_context = "\n".join(context_parts)
    token_estimate = len(full_context) / 4  # Rough estimate: 1 token ? 4 chars
    logger.info(f"[VERTEX AI] Context loaded: ~{int(token_estimate):,} tokens ({len(py_files)} files)")

    return full_context


def initialize_vertex_ai(model_name: str = "gemini-1.5-pro-002"):
    """Initialize Vertex AI with enterprise system instruction

    Args:
        model_name: Vertex AI model to use
                   - "gemini-1.5-pro-002" (default, fastest with 2M tokens)
                   - "gemini-2.0-pro-exp-02-05" (latest experimental)
                   - "gemini-1.5-flash-002" (cheaper, still supports 1M tokens)

    Returns:
        GenerativeModel instance configured for code analysis
    """
    if not GCP_PROJECT_ID:
        logger.error("ERROR: GCP_PROJECT_ID environment variable not set")
        logger.error("   Windows PowerShell: $env:GCP_PROJECT_ID = 'your-project-id'")
        logger.error("   Or set in .env: GCP_PROJECT_ID=your-project-id")
        logger.error("   Or authenticate with: gcloud auth application-default login")
        sys.exit(1)

    logger.info(f"[VERTEX AI] Initializing with project: {GCP_PROJECT_ID} (region: {GCP_LOCATION})")

    # Initialize Vertex AI SDK
    vertexai.init(project=GCP_PROJECT_ID, location=GCP_LOCATION)

    logger.info(f"[VERTEX AI] Using model: {model_name}")

    # Create model instance with enterprise-grade system instruction
    model = GenerativeModel(
        model_name,
        system_instruction="""You are an expert Python and StarCraft 2 AI specialist.

PROJECT CONTEXT: Analyzing a StarCraft 2 AI bot (Wicked Zerg Challenger) using BurnySC2 library.
Manager-based architecture:
- EconomyManager: resource management, worker distribution, building construction
- ProductionManager: unit spawning, tech tree progression, upgrades
- CombatManager: micro control, targeting, unit positioning
- QueenManager: larva injection, creep spread, transfusion healing
- IntelManager: enemy tracking, threat assessment, strategy mode
- TechAdvancer: tech tree progression

YOUR TASKS:
1. Analyze errors in context of entire codebase (2M token window available)
2. Identify root causes by tracing manager dependencies
3. Provide complete, working fixes maintaining code consistency
4. Consider async/await, SC2 API patterns, state management
5. Return ONLY valid JSON with fixed code

OUTPUT REQUIRED:
{
    "cause": "One-sentence root cause",
    "affected_systems": ["Manager1", "Manager2"],
    "fix_explanation": "2-3 lines why this works",
    "fixed_code": "Complete fixed Python code",
    "testing_notes": "How to verify fix"
}

CRITICAL RULES:
- All SC2 API calls MUST use 'await'
- Never directly mutate bot.intel (use update methods)
- Check tech prerequisites before unit production
- Use iteration % N == 0 for performance
- All comments/logs in English only"""
    )

    logger.info(f"[VERTEX AI] Model initialized (2M token context window)")

    return model


def execute_code(file_path: str, timeout: int = EXECUTION_TIMEOUT, no_game: bool = False) -> Tuple[bool, str, str]:
    """Execute Python file and capture result
    Returns: (success: bool, stdout: str, stderr: str)

    Args:
        file_path: Python file to execute
        timeout: Execution timeout in seconds
        no_game: If True, set DRY_RUN_MODE=true to skip game execution
    """
    logger.info(f"RUN Code execution: {file_path}")
    if no_game:
        logger.info("[NO-GAME] Game execution will be skipped (DRY_RUN_MODE)")

    # Prepare environment variables
    env = os.environ.copy()
    if no_game:
        env["DRY_RUN_MODE"] = "true"  # Signal to main_integrated.py to skip game execution

    try:
        result = subprocess.run(
            [sys.executable, file_path],
            capture_output=True,
            text=True,
            encoding="utf-8",  # Force UTF-8 encoding for log output
            errors="replace",   # Replace undecodable bytes with '?'
            timeout=timeout,
            cwd=Path(file_path).parent,
            env=env  # Pass modified environment
        )

        success = result.returncode == 0

        if success:
            logger.info(f"OK Execution success! (return code: 0)")
        else:
            logger.error(f"ERROR Execution failed! (return code: {result.returncode})")

        return success, result.stdout, result.stderr

    except subprocess.TimeoutExpired:
        logger.error(f"TIMEOUT Timeout ({timeout}s): code execution took too long")
        return False, "", f"Timeout after {timeout} seconds"

    except Exception as e:
        logger.error(f"ERROR Execution failed: {e}")
        return False, "", str(e)


def read_source_code(file_path: str) -> str:
    """Read source code from file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"ERROR Failed to read code: {e}")
        raise


def analyze_and_fix(
    model: GenerativeModel,
    source_code: str,
    error_output: str,
    file_name: str,
    attempt: int = 1,
    full_context: str = None
) -> Optional[str]:
    """Analyze error and generate fix via Vertex AI

    Args:
        model: Vertex AI GenerativeModel instance
        source_code: Current file source code
        error_output: Error message from stderr
        file_name: Name of the file being fixed
        attempt: Current attempt number (1-5)
        full_context: Optional full project context (uses 2M token window)

    Returns:
        Fixed code string if successful, None otherwise
    """
    logger.info(f"[VERTEX AI] Analyzing error... (attempt {attempt}/{MAX_FIX_ATTEMPTS})")

    # Extract last N lines of error for clarity
    error_lines = error_output.split('\n')[-20:]
    error_summary = '\n'.join(error_lines)

    # Build context-aware prompt leveraging enterprise token window
    if full_context:
        prompt = f"""TASK: Fix the error in '{file_name}' using full project context.

=== FULL PROJECT CONTEXT (2M tokens available) ===
{full_context}

=== ERROR IN FILE: {file_name} ===
Current problematic code:
```python
{source_code}
```

Error output:
```
{error_summary}
```

=== INSTRUCTIONS ===
1. Analyze the error considering the entire codebase (manager dependencies, async patterns)
2. Find the root cause (check if it's a missing await, wrong parameter, etc.)
3. Provide COMPLETE fixed code that maintains project conventions
4. Return ONLY valid JSON (no markdown, no explanation outside JSON)

CRITICAL: Your response MUST be valid JSON only."""
    else:
        prompt = f"""TASK: Fix the error in '{file_name}'.

Current problematic code:
```python
{source_code}
```

Error output:
```
{error_summary}
```

Analyze the error and provide COMPLETE fixed code.
Return ONLY valid JSON with 'fixed_code' field."""

    try:
        logger.debug(f"[VERTEX AI] Sending request to model...")

        # Generate content using Vertex AI API
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.1,  # Low temp for deterministic code fixes
                "max_output_tokens": 8000,
                "top_p": 0.95,
            },
            safety_settings=[
                SafetySetting(
                    category="HARM_CATEGORY_DANGEROUS_CONTENT",
                    threshold="BLOCK_ONLY_HIGH",
                )
            ]
        )

        response_text = response.text
        logger.debug(f"[VERTEX AI] Response received ({len(response_text)} chars)")
        logger.debug(f"Response:\n{response_text[:500]}...")  # Log first 500 chars

        fixed_code = extract_code_block(response_text)

        if fixed_code:
            logger.info(f"[VERTEX AI] Fix proposal generated successfully")
            return fixed_code
        else:
            logger.warning("[VERTEX AI] Code block not found in response")
            logger.debug(f"Full response:\n{response_text}")
            return None

    except Exception as e:
        logger.error(f"[VERTEX AI] API call failed: {e}")
        logger.debug(traceback.format_exc())
        return None


def extract_code_block(response_text: str) -> Optional[str]:
    """Extract Python code from JSON or markdown response

    Vertex AI responses can be in multiple formats:
    1. Valid JSON with 'fixed_code' field (preferred)
    2. Markdown code blocks
    3. Raw code with explanation
    """
    # Strategy 1: Try to parse as JSON (enterprise preferred format)
    try:
        import json as json_module
        response_data = json_module.loads(response_text)

        if isinstance(response_data, dict):
            if "fixed_code" in response_data:
                logger.info(f"[EXTRACT] JSON response parsed (fixed_code field found)")
                if "cause" in response_data:
                    logger.info(f"   Root cause: {response_data.get('cause', 'N/A')}")
                if "affected_systems" in response_data:
                    logger.info(f"   Affected: {response_data.get('affected_systems', [])}")
                return response_data["fixed_code"].strip()
            elif "code" in response_data:
                logger.info(f"[EXTRACT] JSON response parsed (code field found)")
                return response_data["code"].strip()
    except (ValueError, json_module.JSONDecodeError):
        pass

    # Strategy 2: Try markdown code block format
    pattern = r'```(?:python)?\s*(.*?)\s*```'
    matches = re.findall(pattern, response_text, re.DOTALL)

    if matches:
        logger.info(f"[EXTRACT] Markdown code block found")
        return matches[0].strip()

    # Strategy 3: Look for code between triple backticks (fallback)
    if '```' in response_text:
        parts = response_text.split('```')
        for i, part in enumerate(parts):
            if i % 2 == 1 and part.strip():  # Odd indices = code blocks
                logger.info(f"[EXTRACT] Fallback code block found")
                return part.strip()

    logger.warning("[EXTRACT] No code block found in response")
    return None


def save_code(file_path: str, code: str, backup: bool = True) -> bool:
    """Save code to file with optional backup"""
    try:
        if backup:
            backup_path = f"{file_path}.bak_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            with open(file_path, 'r', encoding='utf-8') as f:
                with open(backup_path, 'w', encoding='utf-8') as bf:
                    bf.write(f.read())
            logger.info(f"BACKUP Created: {backup_path}")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code)

        logger.info(f"SAVE Fixed code saved: {file_path}")
        return True

    except Exception as e:
        logger.error(f"ERROR Failed to save code: {e}")
        return False


def self_healing_loop(
    file_path: str,
    max_attempts: int = MAX_FIX_ATTEMPTS,
    timeout: int = EXECUTION_TIMEOUT,
    use_full_context: bool = False,
    model_name: str = "gemini-1.5-pro",
    no_game: bool = False
) -> bool:
    """Automated fixing loop

    Args:
        file_path: Python file to fix
        max_attempts: Maximum number of fix attempts
        timeout: Execution timeout in seconds
        use_full_context: If True, analyzes full project context (requires more tokens)
        model_name: Gemini model to use (1.5-pro for large context, 2.0-flash for speed)
        no_game: If True, skip game execution (code validation only)
    """

    if not Path(file_path).exists():
        logger.error(f"ERROR File not found: {file_path}")
        return False

    # Load full project context if requested
    full_context = None
    if use_full_context:
        logger.info("CONTEXT Loading full project context...")
        full_context = load_full_project_context(Path(file_path).parent)

    logger.info(f"START Auto-fix loop starting (Vertex AI Enterprise Edition)")
    logger.info(f"   File: {file_path}")
    logger.info(f"   Max attempts: {max_attempts}")
    logger.info(f"   Timeout: {timeout}s")
    logger.info(f"   Model: {model_name} (2M token context window)")
    if use_full_context:
        logger.info(f"   Context: Full project ({len(full_context) if full_context else 0} chars)")
    logger.info("=" * 70)

    model = initialize_vertex_ai(model_name=model_name)

    for attempt in range(1, max_attempts + 1):
        logger.info(f"\n[Attempt {attempt}/{max_attempts}]")
        logger.info("-" * 70)

        # Step 1: Execute code
        success, stdout, stderr = execute_code(file_path, timeout, no_game)

        if success:
            logger.info(f"SUCCESS Code executed successfully!")
            logger.info("=" * 70)
            return True

        # Step 2: Detect error
        logger.warning(f"ERROR Detected:")
        logger.warning(stderr[-500:] if len(stderr) > 500 else stderr)

        if attempt == max_attempts:
            logger.error(f"ERROR Max attempts ({max_attempts}) reached. Failed.")
            logger.info("=" * 70)
            return False

        # Step 3: Read source code
        try:
            source_code = read_source_code(file_path)
        except:
            return False

        # Step 4: Analyze and fix via Gemini
        fixed_code = analyze_and_fix(
            model,
            source_code,
            stderr,
            Path(file_path).name,
            attempt,
            full_context=full_context
        )

        if not fixed_code:
            logger.warning("WARNING Gemini analysis failed. Retrying...")
            time.sleep(2)
            continue

        # Step 5: Save fixed code
        if not save_code(file_path, fixed_code, backup=True):
            return False

        logger.info("WAIT Waiting 2 seconds before retry...")
        time.sleep(2)

    logger.error(f"ERROR Max attempts reached")
    logger.info("=" * 70)
    return False


def save_session_report(file_path: str, success: bool, duration: float):
    """Save session report"""
    report = {
        "timestamp": datetime.now().isoformat(),
        "file": file_path,
        "success": success,
        "duration_seconds": duration,
        "gemini_api_used": True
    }

    report_path = LOG_DIR / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    logger.info(f"REPORT Saved: {report_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Automatic Python bug fixing with Gemini API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python self_healing_orchestrator.py --file main.py
  python self_healing_orchestrator.py --file test.py --max-fixes 3
  python self_healing_orchestrator.py --file script.py --timeout 60
        """
    )

    parser.add_argument(
        "--file", "-f",
        required=True,
        help="Python file to execute"
    )
    parser.add_argument(
        "--max-fixes", "-m",
        type=int,
        default=MAX_FIX_ATTEMPTS,
        help=f"Max fix attempts (default: {MAX_FIX_ATTEMPTS})"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=EXECUTION_TIMEOUT,
        help=f"Execution timeout in seconds (default: {EXECUTION_TIMEOUT})"
    )
    parser.add_argument(
        "--full-context",
        action="store_true",
        help="Analyze full project context (Vertex AI: 2M token window supported)"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gemini-1.5-pro-002",
        choices=[
            "gemini-1.5-pro-002",      # Recommended: fastest Pro model, 2M tokens
            "gemini-2.0-pro-exp-02-05", # Latest experimental
            "gemini-1.5-flash-002",     # Cheaper, 1M tokens
            "gemini-1.5-pro",           # Alias for pro-002
        ],
        help="Vertex AI model to use (default: gemini-1.5-pro-002 - Enterprise grade)"
    )
    parser.add_argument(
        "--no-game",
        action="store_true",
        help="Skip game execution (code validation only)"
    )

    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.is_absolute():
        file_path = Path.cwd() / file_path

    file_path_str = str(file_path)

    start_time = time.time()

    try:
        success = self_healing_loop(
            file_path_str,
            max_attempts=args.max_fixes,
            timeout=args.timeout,
            use_full_context=args.full_context,
            model_name=args.model,
            no_game=args.no_game
        )

        duration = time.time() - start_time
        save_session_report(file_path_str, success, duration)

        if success:
            logger.info(f"OK Completed! Time: {duration:.1f}s")
            sys.exit(0)
        else:
            logger.error(f"ERROR Failed! Time: {duration:.1f}s")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.warning("\nWARNING User interrupted")
        sys.exit(130)
    except Exception as e:
        logger.error(f"ERROR Unexpected error: {e}")
        logger.debug(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
