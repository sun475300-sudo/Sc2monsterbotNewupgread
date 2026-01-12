# 📱 Mobile Bug Monitoring Guide
# 모바일 버그 모니터링 가이드

## 🎯 Overview

Real-time bug monitoring system accessible from mobile devices. Provides comprehensive bug scanning with mobile-friendly UI and real-time updates.

실시간 버그 모니터링 시스템을 모바일 기기에서 사용 가능합니다. 모바일 친화적인 UI와 실시간 업데이트를 제공합니다.

## 🚀 Quick Start

### Start Server

**Windows:**
```bash
start_mobile_bug_monitor.bat
```

**Linux/Mac:**
```bash
chmod +x start_mobile_bug_monitor.sh
./start_mobile_bug_monitor.sh
```

**Direct Python:**
```bash
# Auto-start monitoring (30s interval)
python mobile_bug_monitoring.py --auto-start --interval 30

# Manual control
python mobile_bug_monitoring.py

# Custom port
python mobile_bug_monitoring.py --port 5001
```

### Access Dashboard

**Desktop:**
```
http://localhost:5001
```

**Mobile (same network):**
```
http://<your-computer-ip>:5001
```

**Example:**
```
http://192.168.1.100:5001
```

## 📊 Features

### ✅ Real-time Bug Scanning
- Automatic periodic scanning (configurable interval)
- Manual scan trigger
- WebSocket real-time updates
- No page refresh needed

### 🎯 Bug Detection
Detects 8 types of bugs:
1. **SYNTAX_ERROR** - Python syntax errors
2. **IMPORT_ERROR** - Missing modules
3. **NAME_ERROR** - Undefined variables
4. **TYPE_ERROR** - Type mismatches  
5. **VALUE_ERROR** - Invalid values
6. **ASYNC_ERROR** - Async/await issues
7. **CODE_SMELL** - Code quality issues
8. **PROTOBUF_ERROR** - Protobuf conflicts

### 📈 Statistics & Visualization
- Total bugs count
- Severity breakdown (Critical/High/Warning)
- Bug type distribution
- Top files with most bugs
- Historical tracking

### 📱 Mobile-Optimized UI
- Responsive design
- Touch-friendly controls
- Eye-friendly dark theme
- Minimal data usage
- Background monitoring support

### 🔄 Control Options
- **Start** - Begin continuous monitoring
- **Stop** - Pause monitoring
- **Scan** - Manual single scan

### 🎨 Severity Levels
- 🔴 **CRITICAL** - Requires immediate attention
- 🟡 **HIGH** - Should be fixed soon
- 🟢 **WARNING** - Code smell or minor issue

## 📋 API Endpoints

### Health Check
```
GET /api/health
```

### Bug Data
```
GET /api/bugs/latest?limit=50&severity=high
GET /api/bugs/summary
GET /api/bugs/by-file
GET /api/bugs/by-type
```

### Monitoring Control
```
POST /api/monitoring/start
POST /api/monitoring/stop
GET  /api/monitoring/status
POST /api/scan/trigger
```

### WebSocket Events
```javascript
// Connect
socket = io('http://localhost:5001');

// Listen for updates
socket.on('bug_update', (data) => {
    console.log('Bugs:', data);
});

socket.on('scan_status', (data) => {
    console.log('Status:', data.status);
});
```

## ⚙️ Configuration

### Scan Interval
```bash
# Fast scanning (10 seconds)
python mobile_bug_monitoring.py --auto-start --interval 10

# Normal (30 seconds)
python mobile_bug_monitoring.py --auto-start --interval 30

# Slow (60 seconds)
python mobile_bug_monitoring.py --auto-start --interval 60
```

### Custom Port
```bash
python mobile_bug_monitoring.py --port 5001
```

### Debug Mode
```bash
python mobile_bug_monitoring.py --debug
```

## 🔌 Integration

### With AI Arena Bot (monsterbot)
```bash
# Terminal 1: Start bug monitor
python mobile_bug_monitoring.py --auto-start

# Terminal 2: Watch AI Arena matches
python aiarena_integration.py --watch --bot-id 990

# Terminal 3: Run bot
python main_integrated.py
```

### With Wicked Cline Bot
```bash
# Terminal 1: Bug monitoring
python mobile_bug_monitoring.py --auto-start

# Terminal 2: Auto-fix bugs with Cline
python wicked_cline_bot.py --mission "Fix bugs found by monitor"
```

### With Mobile Dashboard
```bash
# Terminal 1: Bug monitor (port 5001)
python mobile_bug_monitoring.py --auto-start

# Terminal 2: Main dashboard (port 5000)
python mobile_backend_api.py

# Access both from mobile:
# http://<ip>:5000 - Main dashboard
# http://<ip>:5001 - Bug monitor
```

## 📊 Current Bug Status (Example)

```
Total Issues: 2,023
├── Critical: 0 ✅
├── High: 750 ⚠️
└── Warning: 1,273 ⚠️

By Type:
├── CODE_SMELL: 1,273
├── ASYNC_ERROR: 557
├── TYPE_ERROR: 78
├── IMPORT_ERROR: 43
├── VALUE_ERROR: 38
├── PROTOBUF_ERROR: 24
├── SYNTAX_ERROR: 6
└── NAME_ERROR: 4

Top Files:
1. wicked_zerg_bot_pro.py (565)
2. production_manager.py (225)
3. economy_manager.py (173)
4. main_integrated.py (162)
5. parallel_train_integrated.py (95)
```

## 🎮 Usage Scenarios

### 1. Development Mode
Monitor bugs while coding:
```bash
# Terminal 1: Edit code
code .

# Terminal 2: Real-time bug monitor
python mobile_bug_monitoring.py --auto-start --interval 10

# See bugs instantly as you save files
```

### 2. Pre-Commit Check
```bash
# Run single scan before commit
python mobile_bug_monitoring.py --scan-only

# Check bug_report.json
cat bug_report.json | python -m json.tool
```

### 3. CI/CD Integration
```yaml
- name: Bug Scan
  run: |
    pip install -r requirements.txt
    python mobile_bug_monitoring.py --scan-only --output bugs.json
    
- name: Check Critical Bugs
  run: |
    python -c "
    import json
    with open('bugs.json') as f:
        data = json.load(f)
        if data['summary']['critical'] > 0:
            exit(1)
    "
```

### 4. Remote Monitoring
Monitor your codebase from phone while away:
```bash
# On development machine
python mobile_bug_monitoring.py --auto-start --host 0.0.0.0 --port 5001

# On mobile browser
http://<public-ip>:5001

# Use port forwarding or VPN for security
```

## 🔒 Security Notes

### Local Network Only
By default, server binds to `0.0.0.0` (all interfaces) for mobile access. Use firewall rules to restrict access:

```bash
# Windows Firewall
netsh advfirewall firewall add rule name="Bug Monitor" dir=in action=allow protocol=TCP localport=5001

# Linux iptables
sudo iptables -A INPUT -p tcp --dport 5001 -s 192.168.1.0/24 -j ACCEPT
```

### Port Forwarding
For remote access, use secure tunneling:
```bash
# SSH tunnel
ssh -L 5001:localhost:5001 user@remote-server

# ngrok
ngrok http 5001
```

## 📱 Mobile Experience

### Features
- ✅ One-tap scan trigger
- ✅ Auto-refresh bug list
- ✅ Severity filters (All/Critical/High/Warning)
- ✅ Swipe-friendly navigation
- ✅ Low bandwidth usage
- ✅ Works in background

### Tips
- Enable "Keep Screen On" in settings for continuous monitoring
- Use landscape mode for better view
- Bookmark for quick access
- Add to home screen (iOS/Android)

## 🐛 Troubleshooting

### Server Won't Start
```bash
# Check if port is in use
lsof -i :5001  # Linux/Mac
netstat -ano | findstr :5001  # Windows

# Use different port
python mobile_bug_monitoring.py --port 5002
```

### Can't Connect from Mobile
1. Check firewall settings
2. Verify same network connection
3. Find correct IP address:
```bash
# Windows
ipconfig

# Linux/Mac
ifconfig
ip addr show
```

### No Bugs Detected
1. Ensure `realtime_bug_monitor.py` is present
2. Check file permissions
3. Verify Python files exist in project
4. Try manual scan: `POST /api/scan/trigger`

### Slow Performance
1. Increase scan interval: `--interval 60`
2. Reduce bug limit: `?limit=20`
3. Filter by severity: `?severity=critical`

## 🔗 Related Systems

- **Main Dashboard**: Port 5000 (mobile_backend_api.py)
- **Bug Monitor**: Port 5001 (mobile_bug_monitoring.py)
- **Dashboard Backend**: Port 8000 (mobile_dashboard_backend.py)
- **OpenCode Server**: Port 9000 (opencode_integration.py)

## 📚 Additional Resources

- `REALTIME_BUG_MONITORING_GUIDE.md` - Desktop bug monitoring
- `MOBILE_MONITORING_README.md` - Main mobile dashboard
- `WICKED_CLINE_GUIDE.md` - AI agent for auto-fixing
- `README.md` - Complete system overview

## 💡 Pro Tips

1. **Combine with AI Auto-Fix**
   ```bash
   # Watch bugs and auto-fix
   python mobile_bug_monitoring.py --auto-start &
   python wicked_cline_bot.py --watch-bugs
   ```

2. **Export Reports**
   ```bash
   # Generate JSON report
   curl http://localhost:5001/api/bugs/latest?limit=1000 > bugs.json
   ```

3. **Custom Filters**
   ```javascript
   // In mobile browser console
   fetch('/api/bugs/latest?type=ASYNC_ERROR&severity=high')
     .then(r => r.json())
     .then(data => console.log(data));
   ```

4. **Background Monitoring**
   - Enable Wake Lock in mobile browser
   - Use "Add to Home Screen" for app-like experience
   - Enable notifications (if supported)

---

**Need Help?**
- Check system logs
- Review API responses
- Test with Postman/curl
- Verify network connectivity

**Enjoy real-time bug monitoring on the go! 🐛📱✨**
