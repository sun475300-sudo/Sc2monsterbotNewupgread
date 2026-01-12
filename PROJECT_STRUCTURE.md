# Project Structure and Development Guidelines

## Overview

This document describes the canonical structure of the Wicked Zerg AI project and guidelines to prevent code duplication and version drift issues.

## Core Principle: Single Source of Truth (SSOT)

**All source code files should exist in ONE canonical location only.** 

### ✅ Correct Approach
- Keep all `.py` source files in the root directory
- Use deployment scripts to copy files when needed
- Never manually duplicate code files

### ❌ Incorrect Approach (What Was Fixed)
- Having multiple copies of `wicked_zerg_bot_pro.py` in different folders
- Manually copying files to deployment directories
- Editing copies instead of the canonical source

## Directory Structure

```
sc2AIagent/                    # Root directory (working directory)
├── .git/                      # Git repository data (do not modify)
├── .github/                   # GitHub configuration
├── .env.example               # Template for environment configuration
├── .gitignore                 # Git ignore patterns (CRITICAL for security)
├── SECURITY_CLEANUP.md        # Security incident report and guidelines
├── README.md                  # Main project documentation
├── requirements.txt           # Python dependencies
│
├── wicked_zerg_bot_pro.py    # 🎯 MAIN BOT FILE (canonical source)
├── run.py                     # AI Arena entry point
├── main_integrated.py         # Training entry point
├── parallel_train_integrated.py  # Parallel training
│
├── *_manager.py               # Manager modules (economy, combat, intel, etc.)
├── config.py                  # Configuration constants
├── zerg_net.py               # Neural network model
│
├── self_healing_*.py         # Self-healing system files
├── fix_errors*.py            # Error fixing scripts
├── realtime_code_monitor.py  # Code monitoring (use with caution)
│
└── *.bat, *.sh               # Utility scripts (Windows/Linux)
```

## Files That Should NEVER Be in Git

The following files are automatically generated at runtime or contain sensitive data. They are excluded via `.gitignore`:

### 🔒 Security - NEVER Commit These
- `gcp-key.json` - Google Cloud credentials
- `.env` - Environment configuration with secrets
- `*.key`, `*.pem` - Any credential files

### 📊 Runtime Generated - Do Not Commit
- `*.log` - Log files
- `monitor_log.txt`, `training_log.txt` - Specific log files
- `telemetry_*.csv`, `telemetry_*.json` - Game telemetry
- `training_stats.json` - Training statistics
- `cleanup_report_*.txt` - Automated cleanup reports
- `self_healing_logs/` - Self-healing system logs

### 🗃️ Build Artifacts - Do Not Commit
- `__pycache__/` - Python bytecode cache
- `*.pyc`, `*.pyo` - Compiled Python files
- `*.zip` - Package archives (except release builds)
- `dist/`, `build/` - Distribution directories

## Development Workflow

### Setting Up a New Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sun475300-sudo/sc2AIagent.git
   cd sc2AIagent
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials - NEVER commit this file
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run training:**
   ```bash
   python main_integrated.py
   ```

### Making Code Changes

1. **Edit source files directly in the root directory**
   - Do NOT create copies in other directories
   - All changes should be to the canonical source

2. **Test your changes:**
   ```bash
   python main_integrated.py  # For training
   python run.py --LadderServer ... # For AI Arena
   ```

3. **Commit your changes:**
   ```bash
   git status  # Verify only source files are changed
   git add <modified_files>
   git commit -m "Description of changes"
   git push
   ```

### Deploying for AI Arena

**DO NOT manually copy files.** Instead, use the provided packaging script:

```bash
python aiarena_packager.py
```

This script:
- Copies necessary files from the canonical source
- Creates the deployment package
- Cleans up after itself
- Ensures consistency

## Common Mistakes to Avoid

### 1. ❌ Duplicate Files
**Problem:** Multiple versions of the same file exist:
- Root: `wicked_zerg_bot_pro.py`
- AI_Arena_Deploy: `wicked_zerg_bot_pro.py`
- aiarena_submission: `wicked_zerg_bot_pro.py`

**Result:** You fix a bug in one location but it persists in deployment because you're using an old copy.

**Solution:** Keep only ONE copy in root. Use deployment scripts to package.

### 2. ❌ Committing Generated Files
**Problem:** Committing `monitor_log.txt`, `telemetry_0.csv`, etc.

**Result:** 
- Git history becomes bloated
- Merge conflicts on data files
- Hard to see actual code changes

**Solution:** Ensure `.gitignore` is working. Use `git status` before commits.

### 3. ❌ Committing Credentials
**Problem:** Committing `gcp-key.json` or `.env` with real credentials.

**Result:** 
- **SECURITY BREACH** - Credentials exposed to public
- Potential unauthorized access
- Possible billing fraud

**Solution:** 
- Always check `.gitignore` includes security patterns
- Use `git check-ignore <file>` to verify
- Use `.env.example` for templates
- See SECURITY_CLEANUP.md for full guidelines

### 4. ❌ Self-Healing Infinite Loops
**Problem:** `realtime_code_monitor.py` or `fix_errors.py` continuously modifying code.

**Result:**
- Code breaks unexpectedly
- Logic gets corrupted
- Endless healing logs accumulate

**Solution:**
- Use self-healing sparingly and monitor it
- Disable during active development
- Always review auto-generated changes
- Keep backups before running

## File Modification Guidelines

### When to Edit
✅ Edit files directly when:
- Fixing bugs in the core logic
- Adding new features
- Improving performance
- Updating documentation

### When to Be Careful
⚠️ Be cautious with:
- `self_healing_orchestrator.py` - Can modify code automatically
- `realtime_code_monitor.py` - Watches and modifies code
- `fix_errors*.py` - Automated error fixing
- Any script that writes to Python files

### When to Create New Files
🆕 Create new files for:
- New manager modules (follow naming: `*_manager.py`)
- New utility scripts (descriptive names)
- Documentation (`.md` files)
- Configuration templates (`.example` suffix)

## Deployment Checklist

Before deploying to AI Arena or sharing your bot:

- [ ] All changes committed to git
- [ ] No sensitive files in the commit
- [ ] Tested locally with multiple opponents
- [ ] No runtime errors in logs
- [ ] Bot doesn't crash or surrender unexpectedly
- [ ] Used official packaging script (not manual copying)
- [ ] Version number updated (if applicable)

## Troubleshooting Common Issues

### "I fixed a bug but it's still happening"
**Likely cause:** You edited a copy, not the canonical source.

**Solution:** 
```bash
find . -name "wicked_zerg_bot_pro.py"
# Should only show: ./wicked_zerg_bot_pro.py
# If multiple results, you have duplicates - remove them
```

### "Git says I have changes but I didn't modify anything"
**Likely cause:** Self-healing script or logger modified files.

**Solution:**
```bash
git diff  # See what changed
git checkout <file>  # Revert unwanted changes
# Or disable self-healing during development
```

### "I accidentally committed sensitive files"
**Solution:** See SECURITY_CLEANUP.md for complete instructions.

Quick fix:
```bash
git rm --cached gcp-key.json .env
git commit -m "Remove sensitive files"
# Then follow credential rotation steps in SECURITY_CLEANUP.md
```

## Summary

**Golden Rules:**
1. **One canonical source** - No duplicates
2. **Never commit secrets** - Use .gitignore
3. **Use deployment scripts** - No manual copying
4. **Test before committing** - Run `git status` first
5. **Monitor self-healing** - It can cause issues

Following these guidelines will prevent the structural issues identified in the security audit and keep your development workflow smooth and secure.

## Additional Resources

- `SECURITY_CLEANUP.md` - Security incident report and remediation
- `README.md` - Project overview and usage
- `.env.example` - Configuration template
- `.gitignore` - File exclusion patterns
