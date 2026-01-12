# 🤖 monsterbot - AI Arena Quick Start

## 🚀 Super Fast Setup (3 Commands)

### Windows:
```cmd
prepare_monsterbot.bat
```

### Linux/Mac:
```bash
chmod +x prepare_monsterbot.sh
./prepare_monsterbot.sh
```

### Manual:
```bash
# 1. Validate
python aiarena_packager.py --validate

# 2. Package
python aiarena_packager.py --package --version v1

# 3. Upload to https://aiarena.net/
```

---

## 📦 What Gets Packaged

Your `monsterbot_v1_YYYYMMDD.zip` will contain:
- ✅ `run.py` - Entry point for AI Arena
- ✅ `__init__.py` - Ladder game runner
- ✅ `requirements.txt` - Dependencies
- ✅ `main_integrated.py` - Your bot code
- ✅ All supporting `.py` files
- ✅ Configuration files

---

## 🏆 AI Arena Submission Steps

### 1. Register Account
- Go to: https://aiarena.net/
- Click "Register"
- Verify email
- Login

### 2. Create Bot Profile
- Navigate to: **MY BOTS**
- Click: **Create New Bot**
- Fill in:
  - **Name**: `monsterbot`
  - **Race**: `Zerg`
  - **Type**: `1v1`
  - **Public**: No (keep private initially)
- Save

### 3. Upload Bot
- In your bot's page, find **Upload Bot Zip**
- Select: `monsterbot_v1_YYYYMMDD.zip`
- Click Upload
- Wait for processing (1-3 minutes)

### 4. Check Build Status
- Status shows as: **Compiling** → **Active** (success) or **Error** (failed)
- If error, click **View Logs** to see what went wrong
- Common errors:
  - Missing dependencies → Add to requirements.txt
  - Import errors → Check file names match
  - Structure errors → Re-run packager

### 5. Watch Matches
- Once **Active**, bot automatically joins match queue
- View matches in **MY BOTS** → **monsterbot** → **Matches**
- First match usually within 5-10 minutes

---

## 📊 Monitor Performance

### Live Stats
```bash
# Watch matches in real-time
python aiarena_integration.py --watch --bot-id YOUR_BOT_ID --token YOUR_TOKEN
```

### Web Dashboard
- **Matches**: https://aiarena.net/bots/YOUR_BOT_ID/matches/
- **Stats**: https://aiarena.net/bots/YOUR_BOT_ID/
- **Ranking**: https://aiarena.net/ranking/

---

## 🔄 Update Your Bot

When you improve your bot:

```bash
# 1. Test locally
python run.py

# 2. Package new version
python aiarena_packager.py --package --version v2

# 3. Upload to AI Arena (replaces old version)
```

Or use auto-update:
```bash
python aiarena_integration.py --auto-update --token YOUR_TOKEN
```

---

## 🐛 Troubleshooting

### Error: "run.py not found in zip"
**Solution:** Files were packaged incorrectly. The packager creates proper structure automatically.
```bash
python aiarena_packager.py --package
```

### Error: "ModuleNotFoundError: No module named 'X'"
**Solution:** Add missing module to requirements.txt
```bash
echo "missing-package==1.0.0" >> requirements.txt
python aiarena_packager.py --package
```

### Error: "Bot timed out"
**Solution:** Optimize bot performance
- Reduce calculations per frame
- Cache expensive operations
- Use `if iteration % 10 == 0:` for non-critical checks

### Error: "Import error: cannot import name 'X'"
**Solution:** Check file and class names in run.py match your actual files
```python
# In run.py, make sure this matches your bot file:
from main_integrated import WickedZergBot as BotClass
# Or:
from wicked_zerg_bot_pro import WickedZergBotPro as BotClass
```

---

## 🎮 Competition Info

### Current Competition
- **Name**: MonsterBot SC2 AI Arena 2026 Pre-Season 1
- **ID**: 2385
- **URL**: https://aiarena.net/competitions/stats/2385/

### How Ranking Works
- **ELO System**: Start at ~1500, gain/lose points per match
- **Matchmaking**: Matched with similar ELO bots
- **Leaderboard**: https://aiarena.net/ranking/

### Match Format
- **Time Limit**: 20 minutes per game
- **Maps**: Rotation of ladder maps
- **Game Mode**: 1v1 standard rules

---

## 📈 Performance Tips

### Optimize for AI Arena
1. **Fast early game**: AI Arena favors aggressive play
2. **Efficient code**: Minimize lag (< 100ms per frame)
3. **Robust error handling**: Crashes = instant loss
4. **Map awareness**: Adapt to different maps
5. **Scout early**: Know opponent's strategy

### Test Before Upload
```bash
# Local test
python run.py

# Test with different opponents
python run.py  # Edit to change opponent race/difficulty
```

---

## 🔗 Resources

- **AI Arena Website**: https://aiarena.net/
- **Discord**: https://discord.gg/aiarena
- **Wiki**: https://aiarena.net/wiki/
- **GitHub**: https://github.com/aiarena
- **Forum**: https://aiarena.net/forum/

---

## ✅ Pre-Upload Checklist

Before uploading, verify:
- [ ] Bot runs locally without errors
- [ ] All files included in package
- [ ] requirements.txt has all dependencies
- [ ] run.py has correct bot import
- [ ] No debugging code left in
- [ ] Package validated with packager script
- [ ] Bot name is "monsterbot"
- [ ] Race set to Zerg

---

**Ready to compete? Run the prepare script and upload!** 🏆

```bash
# Windows
prepare_monsterbot.bat

# Linux/Mac  
./prepare_monsterbot.sh
```

**Good luck in the arena!** 🤖⚔️
