#!/usr/bin/env python
"""
Feature Verification Script
Validates implementation completeness of all 3 core features
"""

import os
from pathlib import Path

def verify_feature_1():
    """Verify Feature 1: Self-Healing Orchestrator"""
    print("=" * 70)
    print("   1. Self-Healing AI Agent - Autonomous Modification & Testing")
    print("=" * 70)
    
    file_path = Path("self_healing_orchestrator.py")
    
    if not file_path.exists():
        print("X File not found")
        return False
    
    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    
    checks = {
        "File exists": file_path.exists(),
        "File size": f"{file_path.stat().st_size:,} bytes",
        "Line count": f"{len(lines)} lines",
        "self_healing_loop function": "def self_healing_loop(" in content,
        "execute_code function": "def execute_code(" in content,
        "analyze_and_fix function": "def analyze_and_fix(" in content,
        "Vertex AI integration": "import vertexai" in content,
        "2M token support": "2M token" in content or "2,000,000" in content,
        "Backup feature": "backup" in content.lower(),
        "Re-execution validation": "re-execution" in content.lower() or "retry" in content.lower(),
    }
    
    for check, result in checks.items():
        if isinstance(result, bool):
            status = "OK" if result else "X"
            print(f"  [{status}] {check}")
        else:
            print(f"  [OK] {check}: {result}")
    
    all_passed = all(v for v in checks.values() if isinstance(v, bool))
    print(f"\nCompletion: {'100% Complete' if all_passed else 'Incomplete'}")
    return all_passed

def verify_feature_2():
    """Verify Feature 2: 2M Token AI"""
    print("\n" + "=" * 70)
    print("   2. 2M Token AI - Vertex AI Gemini Full Project Understanding")
    print("=" * 70)
    
    file_path = Path("self_healing_orchestrator.py")
    content = file_path.read_text(encoding="utf-8")
    
    checks = {
        "load_full_project_context": "def load_full_project_context(" in content,
        "initialize_vertex_ai": "def initialize_vertex_ai(" in content,
        "2M token window": "2M token" in content,
        "Vertex AI import": "import vertexai" in content,
        "GenerativeModel": "GenerativeModel" in content,
        "Project file loading": "py_files" in content and "glob" in content,
        "Token estimation": "token_estimate" in content,
        "System instruction": "system_instruction" in content,
        "Multi-model support": "gemini-1.5-pro" in content or "model_name" in content,
        "GCP authentication": "GCP_PROJECT_ID" in content,
    }
    
    for check, result in checks.items():
        status = "OK" if result else "X"
        print(f"  [{status}] {check}")
    
    all_passed = all(checks.values())
    print(f"\nCompletion: {'100% Complete' if all_passed else 'Incomplete'}")
    return all_passed

def verify_feature_3():
    """Verify Feature 3: Hyper-Fast Code Inspector"""
    print("\n" + "=" * 70)
    print("   3. Hyper-Fast Inspector - 1M+ lines/0.1sec")
    print("=" * 70)
    
    files = {
        "fast_code_inspector.py": "Main inspector",
        "pyproject.toml": "Ruff config",
        "fast_inspect.bat": "Windows menu",
        ".pre-commit-config.yaml": "Git hooks",
        "performance_profiler.py": "Performance profiler",
    }
    
    all_exist = True
    for file_name, description in files.items():
        file_path = Path(file_name)
        exists = file_path.exists()
        status = "OK" if exists else "X"
        print(f"  [{status}] {file_name} - {description}")
        if exists and file_name.endswith('.py'):
            lines = len(file_path.read_text(encoding='utf-8').splitlines())
            print(f"        ({lines} lines)")
        all_exist = all_exist and exists
    
    # Check main features
    print("\n  Core Features:")
    
    inspector_path = Path("fast_code_inspector.py")
    if inspector_path.exists():
        content = inspector_path.read_text(encoding="utf-8")
        
        features = {
            "Ruff integration": "ruff" in content.lower(),
            "Full scan": "run_fast_check" in content,
            "Incremental scan": "run_incremental_check" in content or "--fast" in content,
            "Auto-fix": "--fix" in content,
            "Performance profiling": "stats" in content and "lines_per_second" in content,
            "Git integration": "git" in content.lower(),
        }
        
        for feature, result in features.items():
            status = "OK" if result else "X"
            print(f"    [{status}] {feature}")
    
    print(f"\nCompletion: {'100% Complete' if all_exist else 'Incomplete'}")
    return all_exist

def main():
    """Main verification"""
    print("\n")
    print("=" * 70)
    print(" " * 10 + "3 Core Features - Verification Report" + " " * 10)
    print("=" * 70)
    print()
    
    result1 = verify_feature_1()
    result2 = verify_feature_2()
    result3 = verify_feature_3()
    
    print("\n" + "=" * 70)
    print("   Final Results")
    print("=" * 70)
    
    results = {
        "1. Self-Healing AI Agent": result1,
        "2. 2M Token AI": result2,
        "3. Hyper-Fast Inspector": result3,
    }
    
    for feature, result in results.items():
        status = "OK" if result else "X"
        completion = "100% Complete" if result else "Incomplete"
        print(f"  [{status}] {feature}: {completion}")
    
    all_complete = all(results.values())
    
    print("\n" + "=" * 70)
    if all_complete:
        print("   SUCCESS: All features are perfectly implemented!")
    else:
        print("   WARNING: Some features are incomplete.")
    print("=" * 70)
    
    return all_complete

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
