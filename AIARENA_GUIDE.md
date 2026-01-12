# 🏆 AI Arena Competition Guide

Complete guide for submitting your bot to AI Arena competitions.

## 🎯 Competition URL

**MonsterBot SC2 AI Arena 2026 Pre-Season 1**
https://aiarena.net/competitions/stats/2385/monsterbot-sc2-ai-arena-2026-pre-season-1

## 🚀 Quick Start (5 Steps)

### Step 1: Register on AI Arena
```
1. Go to https://aiarena.net/
2. Create an account
3. Verify your email
4. Go to https://aiarena.net/profile/token/
5. Copy your API token
```

### Step 2: Package Your Bot
```bash
python aiarena_integration.py --package --bot-name "monsterbot"
```

**Output:**
```
✅ Bot packaged: monsterbot_20260109_235959.zip (2.45 MB)
```

### Step 3: Submit to AI Arena
```bash
# Set your token
export AIARENA_API_TOKEN="your_token_here"

# Submit
python aiarena_integration.py --submit --token $AIARENA_API_TOKEN
```

### Step 4: Watch Matches
```bash
# Get your bot ID from submission output
python aiarena_integration.py --watch --bot-id 123 --token $AIARENA_API_TOKEN
```

### Step 5: Enable Auto-Updates
```bash
python aiarena_integration.py --auto-update --token $AIARENA_API_TOKEN --interval 3600
```

## 📦 Bot Requirements

### Required Files

Your bot package must include:

1. **ladderbots.json** (auto-generated)
```json
{
  "Bots": {
    "monsterbot": {
      "Race": "Zerg",
      "Type": "Python",
      "RootPath": "./",
      "FileName": "main_integrated.py",
      "Debug": false,
      "Args": null
    }
  }
}
```

2. **requirements.txt**
```
burnysc2==6.0.0
loguru==0.7.0
numpy==1.24.0
# Add all your dependencies
```

3. **Main bot file** (`main_integrated.py`)
- Should contain your bot class
- Must inherit from `sc2.BotAI`
- Should be production-ready

4. **Supporting files**
- All `.py` files your bot needs
- Data files if any
- Configuration files

### File Structure
```
monsterbot.zip
├── ladderbots.json
├── requirements.txt
├── run.py
├── __init__.py
├── main_integrated.py
├── production_manager.py
├── combat_manager.py
├── intel_manager.py
├── strategy_hub.py
└── ... (other Python files)
```

## 🎮 Competition System

### How It Works

1. **Submission**: Upload your bot zip file
2. **Queue**: Bot enters match queue
3. **Matches**: AI Arena runs matches automatically
4. **Rankings**: ELO rating system
5. **Leaderboard**: Track your position

### Match Types

- **Ladder Matches**: Standard competitive matches
- **Competition Matches**: Official tournament games
- **Practice Matches**: Test matches (if available)

### Maps

Common AI Arena maps:
- Automaton LE
- Golden Wall LE
- Hardwire LE
- Oceanborn LE
- Site Delta LE

## 📊 Real-Time Monitoring

### Watch Matches Live
```bash
python aiarena_integration.py --watch --bot-id YOUR_BOT_ID --interval 30
```

**Output:**
```
👀 Watching matches for bot 123
   Checking every 30 seconds
   Press Ctrl+C to stop

🎮 NEW MATCH #5678
   Map: Automaton LE
   Opponent: RoachBot
   Result: Victory
   Date: 2026-01-10 00:15:30
```

### Get Stats
```python
from aiarena_integration import AIArenaBot

bot = AIArenaBot(api_token="your_token")
stats = bot.get_bot_stats(bot_id=123)

print(f"Wins: {stats['wins']}")
print(f"Losses: {stats['losses']}")
print(f"Win Rate: {stats['win_rate']}%")
print(f"ELO: {stats['elo']}")
```

### Dashboard Integration
```python
# In mobile_backend_api.py
from aiarena_integration import AIArenaBot

@app.route('/aiarena/stats')
def get_aiarena_stats():
    bot = AIArenaBot(api_token=os.getenv('AIARENA_API_TOKEN'))
    stats = bot.get_bot_stats(bot_id=request.args.get('bot_id'))
    return jsonify(stats)
```

## 🔄 Auto-Update System

### How It Works

1. **Monitor**: Check bot performance every hour
2. **Analyze**: Evaluate win rate and match results
3. **Improve**: Apply code improvements (from Vertex AI)
4. **Test**: Run local tests
5. **Submit**: Upload new version automatically
6. **Repeat**: Continuous improvement loop

### Enable Auto-Updates
```bash
# Start auto-updater
python aiarena_integration.py --auto-update --token $AIARENA_API_TOKEN

# Custom interval (check every 2 hours)
python aiarena_integration.py --auto-update --token $AIARENA_API_TOKEN --interval 7200
```

### Configuration
```python
from aiarena_integration import AIArenaBot, AIArenaAutoUpdater

bot = AIArenaBot(api_token="your_token")
updater = AIArenaAutoUpdater(
    bot_manager=bot,
    improvement_threshold=0.05  # Update if 5% improvement available
)

updater.auto_update_loop(check_interval=3600)  # Check every hour
```

## 🤖 Integration with Other Systems

### With Vertex AI Orchestrator
```python
# In vertex_ai_orchestrator.py
from aiarena_integration import AIArenaBot

# After fixes are applied
bot = AIArenaBot()
bot_zip = bot.package_bot()
result = bot.submit_bot(bot_zip)

if 'error' not in result:
    print(f"✅ Improved bot submitted to AI Arena!")
```

### With Mobile Dashboard
```html
<!-- In mobile_dashboard_ui.html -->
<div class="aiarena-stats">
  <h3>🏆 AI Arena Stats</h3>
  <div id="aiarena-data">
    <p>Wins: <span id="wins">0</span></p>
    <p>Losses: <span id="losses">0</span></p>
    <p>Win Rate: <span id="winrate">0</span>%</p>
    <p>ELO: <span id="elo">1500</span></p>
    <p>Rank: <span id="rank">-</span></p>
  </div>
</div>

<script>
// Fetch AI Arena stats
fetch('/aiarena/stats?bot_id=123')
  .then(r => r.json())
  .then(data => {
    document.getElementById('wins').textContent = data.wins;
    document.getElementById('losses').textContent = data.losses;
    document.getElementById('winrate').textContent = data.win_rate;
    document.getElementById('elo').textContent = data.elo;
    document.getElementById('rank').textContent = data.rank;
  });
</script>
```

### With Wicked Cline Bot
```python
# Automate submission with AI agent
from wicked_cline_bot import WickedClineBot

bot = WickedClineBot()
response = bot.execute_mission("""
1. Run all tests to ensure bot works
2. Package bot for AI Arena
3. Submit to competition if tests pass
4. Report results
""")
```

## 📝 Submission Checklist

Before submitting, ensure:

- [ ] Bot runs without errors locally
- [ ] All dependencies in requirements.txt
- [ ] ladderbots.json properly configured
- [ ] Bot name is unique
- [ ] No hardcoded paths
- [ ] No debugging code left in
- [ ] Handles all race matchups
- [ ] Works on all maps
- [ ] Resource efficient (< 2GB RAM)
- [ ] Doesn't timeout (< 10 min games)

## 🐛 Common Issues

### Issue 1: Bot Crashes on AI Arena
**Solution:**
```python
# Add error handling
try:
    # Your bot logic
    pass
except Exception as e:
    logger.error(f"Error: {e}")
    # Fallback behavior
```

### Issue 2: Import Errors
**Solution:**
```bash
# Ensure all imports are in requirements.txt
pip freeze > requirements.txt

# Test with clean environment
python -m venv test_env
source test_env/bin/activate
pip install -r requirements.txt
python main_integrated.py
```

### Issue 3: Timeout
**Solution:**
```python
# Optimize expensive operations
# Cache calculations
# Reduce unit checks per frame
async def on_step(self, iteration):
    if iteration % 10 == 0:  # Every 10 frames
        # Expensive logic here
        pass
```

### Issue 4: API Token Issues
**Solution:**
```bash
# Set environment variable
export AIARENA_API_TOKEN="your_token_here"

# Or use .env file
echo "AIARENA_API_TOKEN=your_token" >> .env
```

## 🏆 Competition Strategy

### Phase 1: Initial Submission
1. Submit basic working bot
2. Get baseline ELO rating
3. Watch first 10 matches
4. Collect opponent data

### Phase 2: Iteration
1. Analyze losses
2. Apply improvements
3. Test locally
4. Submit update
5. Monitor results

### Phase 3: Optimization
1. Study top bots
2. Implement counter-strategies
3. Optimize build orders
4. Fine-tune timings
5. Continuous updates

## 📈 Performance Tracking

### Key Metrics
- **Win Rate**: Target > 50%
- **ELO**: Goal > 2000
- **Rank**: Track position
- **Match Count**: More = better rating accuracy

### Improvement Indicators
- Consistent wins against lower-rated bots
- Close games against higher-rated bots
- Specific map performance
- Matchup win rates (ZvZ, ZvT, ZvP)

## 🔧 Advanced Features

### Custom Build Orders per Map
```python
# In main_integrated.py
def select_build_order(self):
    if self.game_info.map_name == "Automaton LE":
        return SERRAL_BUILD_ZVT
    elif "Golden Wall" in self.game_info.map_name:
        return REYNOR_BUILD_ZVP
    else:
        return DEFAULT_BUILD
```

### Opponent-Specific Strategies
```python
# Track opponents
opponent_history = {}

def get_strategy(self, opponent_name):
    if opponent_name in opponent_history:
        # Use learned strategy
        return opponent_history[opponent_name]
    else:
        # Use default
        return DEFAULT_STRATEGY
```

### Machine Learning Integration
```python
# Collect match data
# Train models
# Apply learned strategies
# Continuous improvement
```

## 📞 Support

- **AI Arena Discord**: https://discord.gg/aiarena
- **Documentation**: https://aiarena.net/wiki/
- **GitHub**: https://github.com/aiarena
- **Forum**: https://aiarena.net/forum/

## 🎉 Success Stories

Once your bot is ranking:
1. Share results on Discord
2. Contribute improvements
3. Help other developers
4. Climb the leaderboard!

---

**Made with 🏆 by Wicked Team**

**"From code to competition champion!"** 🚀
