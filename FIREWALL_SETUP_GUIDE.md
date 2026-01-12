# Windows Firewall Setup Guide for SC2 Dashboard

## Problem: 액세스가 거부되었습니다 (Access Denied)

When running firewall configuration commands without admin rights, you get:
```
New-NetFirewallRule : 액세스가 거부되었습니다.
(Access Denied - Permission Denied)
```

## Solution: 4 Methods to Configure Firewall

### Method 1: Automatic Script (Recommended) ⭐

**Step 1**: Right-click `setup_firewall_admin.bat`

**Step 2**: Select "관리자 권한으로 실행" (Run as Administrator)

**Step 3**: Click "예" (Yes) on the UAC prompt

**Step 4**: Script automatically configures all 4 ports

**Ports configured:**
- 8000: Main Dashboard (FastAPI)
- 5001: Bug Monitor (Flask)
- 5000: Backend API (Flask)
- 9000: OpenCode Server

---

### Method 2: PowerShell Manual

**Step 1**: Open PowerShell as Administrator
- Press `Win + X`
- Select "Windows PowerShell (관리자)" or "Windows PowerShell (Admin)"

**Step 2**: Run the script
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
cd "D:\wicked_zerg_challenger"  # Change to your project directory
.\setup_firewall_admin.ps1
```

**Step 3**: Follow the on-screen instructions

---

### Method 3: Windows Defender Firewall GUI (Manual)

**Step 1**: Open Windows Defender Firewall
- Press `Win + R`
- Type: `wf.msc`
- Press Enter

**Step 2**: Create Inbound Rule
1. Click "Inbound Rules" in left panel
2. Click "New Rule..." in right panel (Actions)

**Step 3**: Configure Port Rule
1. Select "Port" → Click "Next"
2. Select "TCP"
3. Select "Specific local ports"
4. Enter: `8000` (for Main Dashboard)
5. Click "Next"

**Step 4**: Allow Connection
1. Select "Allow the connection"
2. Click "Next"

**Step 5**: Profile Selection
1. Check all: Domain, Private, Public
2. Click "Next"

**Step 6**: Name the Rule
1. Name: `SC2 Main Dashboard`
2. Description: `Allows incoming connections for SC2 Dashboard on port 8000`
3. Click "Finish"

**Step 7**: Repeat for other ports
- Repeat steps 2-6 for ports: 5001, 5000, 9000
- Use appropriate names:
  - Port 5001: `SC2 Bug Monitor`
  - Port 5000: `SC2 Backend API`
  - Port 9000: `SC2 OpenCode Server`

---

### Method 4: Command Prompt (Admin)

**Step 1**: Open Command Prompt as Administrator
- Press `Win + X`
- Select "명령 프롬프트(관리자)" or "Command Prompt (Admin)"

**Step 2**: Run commands
```cmd
netsh advfirewall firewall add rule name="SC2 Main Dashboard" dir=in action=allow protocol=TCP localport=8000

netsh advfirewall firewall add rule name="SC2 Bug Monitor" dir=in action=allow protocol=TCP localport=5001

netsh advfirewall firewall add rule name="SC2 Backend API" dir=in action=allow protocol=TCP localport=5000

netsh advfirewall firewall add rule name="SC2 OpenCode Server" dir=in action=allow protocol=TCP localport=9000
```

**Expected output:**
```
Ok.
```

---

## Verification

### Test Firewall Rules

**PowerShell (Admin):**
```powershell
# Test if port 8000 is accessible
Test-NetConnection -ComputerName localhost -Port 8000

# List all SC2 rules
Get-NetFirewallRule -DisplayName "SC2*" | Format-Table DisplayName, Enabled, Direction, Action
```

**Expected output:**
```
TcpTestSucceeded : True
```

### Test from Mobile

1. Ensure mobile and computer are on same WiFi
2. Find computer's IP: `ipconfig`
3. Open mobile browser
4. Navigate to: `http://192.168.0.X:8000`
5. Should see the dashboard

---

## Troubleshooting

### Issue: UAC Prompt doesn't appear

**Solution:**
1. Check UAC settings
2. Go to Control Panel → User Accounts → Change User Account Control settings
3. Move slider to at least the 2nd level from bottom
4. Click OK

### Issue: Still getting "Access Denied"

**Solution:**
1. Ensure you're logged in as Administrator
2. Try Method 3 (GUI) which doesn't require scripts
3. Check if antivirus is blocking the script

### Issue: Rules created but mobile can't connect

**Possible causes:**
1. **Different WiFi networks**: Ensure both devices on same network
2. **Router firewall**: Some routers block inter-device communication
3. **Server not running**: Start the dashboard server first
4. **Wrong IP address**: Use IPv4 address from `ipconfig`, not IPv6

**Solutions:**
```bash
# Check if server is running
netstat -an | findstr "8000"

# Should show: TCP 0.0.0.0:8000 LISTENING

# Find correct IP
ipconfig | findstr "IPv4"

# Test locally first
curl http://localhost:8000
```

### Issue: Port already in use

**Solution:**
```bash
# Find what's using the port
netstat -ano | findstr "8000"

# Kill the process (replace PID)
taskkill /PID <PID> /F

# Or use different port in config
```

---

## Security Notes

### What these rules do:
- ✅ Allow **incoming** connections on specific ports
- ✅ TCP protocol only
- ✅ Ports: 8000, 5001, 5000, 9000
- ❌ Do NOT allow all traffic
- ❌ Do NOT modify outbound rules
- ❌ Do NOT open all ports

### Are these rules safe?
- ✅ Yes, they only allow connections to your dashboard
- ✅ Only devices on your local network can connect (by default)
- ✅ You can remove them anytime
- ✅ The dashboard doesn't expose sensitive data

### How to remove rules (if needed)

**PowerShell (Admin):**
```powershell
Remove-NetFirewallRule -DisplayName "SC2*"
```

**Command Prompt (Admin):**
```cmd
netsh advfirewall firewall delete rule name="SC2 Main Dashboard"
netsh advfirewall firewall delete rule name="SC2 Bug Monitor"
netsh advfirewall firewall delete rule name="SC2 Backend API"
netsh advfirewall firewall delete rule name="SC2 OpenCode Server"
```

**GUI:**
1. Open `wf.msc`
2. Click "Inbound Rules"
3. Find rules starting with "SC2"
4. Right-click → Delete

---

## Alternative: Disable Firewall (Not Recommended)

**Only for testing, not recommended for regular use:**

```powershell
# Disable (Admin PowerShell)
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled False

# Enable back
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
```

**Warning:** This disables all firewall protection. Only use temporarily for testing.

---

## Summary

✅ **Recommended Method**: Run `setup_firewall_admin.bat` as Administrator

✅ **Backup Method**: Use GUI (Method 3) if scripts don't work

✅ **Test**: Use `Test-NetConnection` to verify

✅ **Mobile Access**: http://\<your-ip\>:8000

---

## Need More Help?

See also:
- `COMPLETE_MOBILE_DASHBOARD_GUIDE.md` - Complete mobile setup guide
- `MOBILE_EXECUTION_GUIDE.md` - Detailed execution instructions
- `MOBILE_BUG_MONITORING_GUIDE.md` - Bug monitoring specific guide

If problems persist, check Windows Event Viewer for firewall errors:
- Press `Win + R`
- Type: `eventvwr.msc`
- Navigate to: Windows Logs → Security
- Look for audit failures related to firewall
