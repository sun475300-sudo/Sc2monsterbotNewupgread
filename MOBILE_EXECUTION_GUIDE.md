# 📱 Mobile Execution Guide

Complete guide for running and monitoring the SC2 AI system from mobile devices.

## 📋 Table of Contents

1. [Network Setup](#network-setup)
2. [Starting Services](#starting-services)
3. [Mobile Access](#mobile-access)
4. [Available Dashboards](#available-dashboards)
5. [Control & Monitoring](#control--monitoring)
6. [Troubleshooting](#troubleshooting)

---

## 🌐 Network Setup

### Step 1: Find Your Computer's IP Address

**Windows:**
```cmd
ipconfig
```
Look for "IPv4 Address" under your active network adapter.

**Linux/Mac:**
```bash
ifconfig
# or
ip addr show
```

**Example IP:** `192.168.1.100`

### Step 2: Configure Firewall

**Windows Firewall:**
```powershell
# Allow required ports
netsh advfirewall firewall add rule name="SC2AI-Mobile" dir=in action=allow protocol=TCP localport=5000,5001,8000,9000
```

**Linux (ufw):**
```bash
sudo ufw allow 5000,5001,8000,9000/tcp
```

**Mac (pfctl):**
```bash
# Firewall usually allows local network by default
# If needed, allow ports in System Preferences → Security & Privacy → Firewall
```

### Step 3: Verify Connectivity

From mobile device, open browser and test:
```
http://<your-computer-ip>:8000
```

If it loads, you're ready! ✅

---

## 🚀 Starting Services

### Option 1: All-in-One Startup (Recommended)

**Windows:**
```cmd
start_mobile_monitoring.bat
```

**Linux/Mac:**
```bash
./start_mobile_monitoring.sh
```

This starts all services automatically:
- Mobile Dashboard (port 8000)
- Backend API (port 5000)
- Bug Monitoring (port 5001)

### Option 2: Individual Services

**1. Mobile Dashboard:**
```bash
python mobile_dashboard_backend.py
# Access: http://<ip>:8000
```

**2. Backend API:**
```bash
python mobile_backend_api.py
# Access: http://<ip>:5000
```

**3. Mobile Bug Monitoring:**
```bash
python mobile_bug_monitoring.py --auto-start
# Access: http://<ip>:5001
```

**4. Continuous Improvement (with auto-upload):**
```bash
python continuous_improvement_system.py --hours 2.0
```

**5. OpenCode Server (Remote control):**
```bash
python opencode_integration.py --server --port 9000
# Access: http://<ip>:9000
```

---

## 📱 Mobile Access

### Dashboard URLs

Replace `<ip>` with your computer's IP address:

| Dashboard | URL | Description |
|-----------|-----|-------------|
| **Main Dashboard** | `http://<ip>:8000` | Game stats, resources, units, tech |
| **Backend API** | `http://<ip>:5000/api/game-state` | Raw API access |
| **Bug Monitor** | `http://<ip>:5001` | Real-time bug tracking |
| **OpenCode Server** | `http://<ip>:9000` | Remote code control |

### Example (Computer IP: 192.168.1.100)

```
Main Dashboard:  http://192.168.1.100:8000
Bug Monitor:     http://192.168.1.100:5001
OpenCode:        http://192.168.1.100:9000
```

### Quick Access Setup

**iPhone/iPad:**
1. Open Safari
2. Navigate to dashboard URL
3. Tap Share button
4. Select "Add to Home Screen"
5. Icon appears on home screen!

**Android:**
1. Open Chrome
2. Navigate to dashboard URL
3. Tap Menu (⋮)
4. Select "Add to Home screen"
5. Icon appears on home screen!

---

## 📊 Available Dashboards

### 1. Main Mobile Dashboard (Port 8000)

**Features:**
- ✅ Real-time game statistics
- ✅ Resource tracking (minerals, vespene gas)
- ✅ Supply counter (current/max)
- ✅ Army size
- ✅ Game time
- ✅ Unit composition (Zerglings, Roaches, Hydras, Queens, Workers)
- ✅ Tech progress (Spawning Pool, Roach Warren, Hydralisk Den, etc.)
- ✅ Building phases (Pre/Under Construction/Complete with %)

**Tabs:**
- **Units**: View army composition
- **Tech**: Track technology progress
- **Buildings**: Monitor construction phases
- **Stats**: Game statistics

**Controls:**
- Auto-refresh every 3 seconds
- Touch-friendly interface
- Dark gaming theme
- Responsive design

### 2. Mobile Bug Monitor (Port 5001)

**Features:**
- ✅ Real-time bug detection (8 types)
- ✅ Severity filtering (Critical/High/Warning)
- ✅ Bug type distribution chart
- ✅ Start/Stop/Scan controls
- ✅ Configurable scan interval
- ✅ Bug list with details

**Bug Types:**
1. SYNTAX_ERROR - Python syntax errors
2. IMPORT_ERROR - Missing imports
3. NAME_ERROR - Undefined variables
4. TYPE_ERROR - Type mismatches
5. VALUE_ERROR - Invalid values
6. ASYNC_ERROR - Async/await issues
7. CODE_SMELL - Code quality issues
8. PROTOBUF_ERROR - Protobuf conflicts

**Controls:**
- **Start Monitoring**: Begin automatic scanning
- **Stop Monitoring**: Pause scanning
- **Scan Now**: Trigger immediate scan
- **Interval**: Set scan frequency (10-300s)

### 3. Backend API (Port 5000)

**Endpoints:**

```bash
# Game State
GET /api/game-state

# Units
GET /api/units

# Tech Progress
GET /api/tech

# Building Phases
GET /api/buildings/phases

# Bugs
GET /api/bugs

# WebSocket (Real-time)
WS /ws/game-status
```

**Example Usage:**
```javascript
// Fetch game state from mobile
fetch('http://192.168.1.100:5000/api/game-state')
  .then(response => response.json())
  .then(data => console.log(data));
```

### 4. OpenCode Server (Port 9000)

**Remote Code Control:**
- Run Python scripts remotely
- Execute commands
- Read/write files
- Monitor system

**Usage from mobile:**
```bash
# Send command via API
curl -X POST http://192.168.1.100:9000/execute \
  -H "Content-Type: application/json" \
  -d '{"command": "python main_integrated.py"}'
```

---

## 🎮 Control & Monitoring

### Monitoring from Mobile

**1. Live Game Monitoring:**
```
1. Open main dashboard (port 8000)
2. Watch real-time stats update
3. Switch between tabs (Units/Tech/Buildings)
4. Monitor supply, resources, army size
```

**2. Bug Monitoring:**
```
1. Open bug monitor (port 5001)
2. Click "Start Monitoring"
3. Set scan interval (e.g., 30 seconds)
4. Watch bugs appear in real-time
5. Filter by severity if needed
```

**3. Building Progress:**
```
1. Main dashboard → Buildings tab
2. See pre-construction (planned)
3. See under construction (with %)
4. See completed buildings
5. Phase distribution chart
```

### Remote Control from Mobile

**Using Mobile Browser:**

1. **Stop/Start Services:**
   - Navigate to dashboard
   - Use Start/Stop buttons
   - Monitor status indicators

2. **Trigger Manual Scans:**
   - Bug monitor → "Scan Now"
   - Immediate bug detection
   - View results instantly

3. **Configure Settings:**
   - Adjust scan intervals
   - Filter bug types
   - Enable/disable features

**Using Mobile SSH:**

```bash
# Connect via SSH (if configured)
ssh user@192.168.1.100

# Start services
cd /path/to/sc2AIagent
python continuous_improvement_system.py --hours 2.0 &

# Check status
ps aux | grep python

# View logs
tail -f *.log
```

### Background Execution on Mobile

**iOS (Safari):**
- Dashboards use Wake Lock API
- Keep screen on while monitoring
- Or use screen stays awake setting

**Android (Chrome):**
- Supports background tabs
- Dashboard continues updating
- Enable "Desktop site" for best experience

**Both Platforms:**
- Add to home screen for app-like experience
- Receive visual notifications (if implemented)
- Check periodically for updates

---

## 🔧 Troubleshooting

### Can't Connect from Mobile

**Check 1: Same Network**
```
✅ Computer and mobile on same WiFi
✅ Not using guest network
✅ Not using VPN
```

**Check 2: Firewall**
```bash
# Windows - Verify firewall rule
netsh advfirewall firewall show rule name="SC2AI-Mobile"

# Linux - Check ufw
sudo ufw status
```

**Check 3: Services Running**
```bash
# Check if ports are listening
netstat -an | find "8000"
netstat -an | find "5000"
netstat -an | find "5001"
```

**Check 4: IP Address**
```bash
# Verify you have correct IP
ping <your-computer-ip>
```

### Dashboard Not Updating

**Solution 1: Clear Cache**
- Mobile browser → Settings → Clear cache
- Reload dashboard

**Solution 2: Check Backend**
```bash
# Verify backend is running
curl http://localhost:5000/api/health

# Check logs
tail -f mobile_backend_api.log
```

**Solution 3: Restart Services**
```bash
# Stop all
pkill -f "mobile_"

# Start again
python mobile_dashboard_backend.py &
python mobile_backend_api.py &
```

### Slow Performance

**Optimization 1: Reduce Update Frequency**
```javascript
// In dashboard, change refresh interval
setInterval(updateData, 5000); // 5 seconds instead of 3
```

**Optimization 2: Limit Data**
```bash
# Start with lower scan frequency
python mobile_bug_monitoring.py --auto-start --interval 60
```

**Optimization 3: Close Other Apps**
- Close unused browser tabs
- Free up mobile RAM
- Restart mobile device

### Connection Lost

**Auto-Reconnect:**
- Dashboards have auto-reconnect (up to 5 attempts)
- WebSocket reconnects automatically
- Just wait or refresh page

**Manual Reconnect:**
```
1. Refresh browser page
2. Check computer is awake
3. Verify network connection
4. Restart services if needed
```

---

## 🎯 Best Practices

### For Best Mobile Experience

1. **Use WiFi**: Avoid cellular data (local network only)
2. **Keep Screen On**: Enable stay-awake in settings
3. **Add to Home Screen**: App-like experience
4. **Use Landscape Mode**: Better dashboard visibility
5. **Close Other Apps**: Free up resources
6. **Check Regularly**: Monitor for issues
7. **Bookmark URLs**: Quick access

### For Continuous Monitoring

1. **Start Continuous Improvement**:
   ```bash
   python continuous_improvement_system.py --hours 2.0
   ```

2. **Enable GitHub Auto-Upload**:
   - Already integrated in continuous improvement
   - Uploads every 5 minutes automatically

3. **Monitor from Mobile**:
   - Check progress periodically
   - View bug fixes in real-time
   - See building construction live

4. **Background Operation**:
   - Let continuous improvement run on computer
   - Monitor progress from mobile
   - Check final reports when complete

---

## 📱 Mobile App Alternative (Future)

While current system uses web dashboards, you can create a native app:

**React Native:**
```bash
# Setup React Native
npx react-native init SC2AIMonitor

# Connect to backend API
const API_URL = 'http://192.168.1.100:5000';

# Implement real-time updates
import io from 'socket.io-client';
const socket = io(API_URL);
```

**Progressive Web App (PWA):**
```html
<!-- Add to dashboard -->
<link rel="manifest" href="/manifest.json">
<meta name="apple-mobile-web-app-capable" content="yes">
```

---

## 💡 Pro Tips

### Tip 1: Create QR Codes
```python
import qrcode

# Generate QR code for dashboard
qr = qrcode.make('http://192.168.1.100:8000')
qr.save('dashboard_qr.png')

# Scan from mobile for instant access
```

### Tip 2: Use Bookmarklet
```javascript
// Add to mobile bookmarks
javascript:(function(){location.href='http://192.168.1.100:8000'})();
```

### Tip 3: Setup DDNS (For Remote Access)
```bash
# Use service like No-IP or DuckDNS
# Access from anywhere: http://mysc2ai.ddns.net:8000
```

### Tip 4: Enable HTTPS (For Security)
```bash
# Use mkcert for local HTTPS
mkcert -install
mkcert 192.168.1.100

# Access via: https://192.168.1.100:8000
```

---

## 🎉 You're Ready!

Your SC2 AI system is now fully accessible from mobile devices!

**Quick Start Checklist:**
- ✅ Computer IP address noted
- ✅ Firewall configured
- ✅ Services started
- ✅ Mobile connected to same network
- ✅ Dashboards bookmarked
- ✅ Monitoring active

**Next Steps:**
1. Start continuous improvement system
2. Monitor from mobile
3. Watch bug fixes in real-time
4. Check building construction
5. View final reports

Happy monitoring! 🚀📱

---

**Support:**
- Check logs: `*.log` files
- GitHub Issues: [sc2AIagent/issues](https://github.com/sun475300-sudo/sc2AIagent/issues)
- Documentation: All `*_GUIDE.md` files
