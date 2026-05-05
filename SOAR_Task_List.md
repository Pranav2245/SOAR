# SOAR Project — Complete Task Breakdown

---

## Phase 1: Environment Setup ✅
- [x] Docker Compose (Wazuh 4.9 + TheHive 5 + Cortex + MISP)
- [x] Kali Linux VM agent install script
- [x] TLS certificate generation files

## Phase 2: Core Integration Pipeline ✅
- [x] Wazuh → TheHive webhook (TheHive 5.x API)
- [x] Custom Wazuh detection rules
- [x] Cortex IP analyzer + IP block responder

## Phase 3: AI-Powered Modules (8 Modules) ✅
- [x] 3.1 ML Triage Analyzer — XGBoost confidence scoring
- [x] 3.2 LLM Incident Commander — Gemini case summarization
- [x] 3.3 NLP Phishing Parser — email intent BEC detection
- [x] 3.4 Anomaly Detection — Isolation Forest
- [x] 3.5 Semantic Log Clustering — TF-IDF + K-Means
- [x] 3.6 Blast Radius Predictor — graph-based lateral movement
- [x] 3.7 Playbook Optimizer — self-learning feedback loop
- [x] 3.8 Incident Report Generator — detailed PDF (10 sections + glossary)

## Phase 3B: AI Training & Data Expansion ✅
- [x] ML Triage — 15,000 samples, 50 attack types + 12 normal scenarios
- [x] Phishing Parser — 100 emails (50 phishing/6 categories + 50 legit)
- [x] Anomaly Detection — 1080 samples, 8 attack patterns + 3 normal modes
- [x] All 3 models retrained (Triage: 100%, Phishing: 85%)

### 50 Attack Types Covered:
| #  | Category              | Attack Type              |
|----|-----------------------|--------------------------|
| 1  | Brute Force           | SSH Brute Force          |
| 2  | Malware               | Ransomware               |
| 3  | Command & Control     | C2 Beacon                |
| 4  | Data Theft            | Data Exfiltration        |
| 5  | Privilege             | Privilege Escalation     |
| 6  | Web                   | SQLi / XSS / RFI         |
| 7  | Movement              | Lateral Movement         |
| 8  | Persistence           | Rootkit                  |
| 9  | Resource Abuse        | Cryptomining             |
| 10 | Social Engineering    | Phishing Click           |
| 11 | Insider               | Insider Threat           |
| 12 | Network Flood         | DDoS                     |
| 13 | Password Cracking     | Dictionary Attack        |
| 14 | Password Cracking     | Credential Stuffing      |
| 15 | Password Cracking     | Password Spraying        |
| 16 | Password Cracking     | Kerberoasting            |
| 17 | Password Cracking     | Pass-the-Hash            |
| 18 | Password Cracking     | Rainbow Table Cracking   |
| 19 | Password Cracking     | Keylogging               |
| 20 | Password Cracking     | RDP Brute Force          |
| 21 | Network               | DNS Tunneling            |
| 22 | Network               | ARP Spoofing             |
| 23 | Network               | Man-in-the-Middle        |
| 24 | Recon                 | Port Scanning            |
| 25 | Application           | Supply Chain Attack      |
| 26 | Application           | Zero-Day Exploit         |
| 27 | Application           | API Abuse                |
| 28 | APT                   | Fileless Malware         |
| 29 | APT                   | Watering Hole            |
| 30 | APT                   | Reverse Shell            |
| 31 | Cloud Configuration   | S3 Bucket Exposure       |
| 32 | Cloud Identity        | IAM Role Hijacking       |
| 33 | Endpoint Evasion      | Process Hollowing        |
| 34 | Endpoint Evasion      | DLL Hijacking            |
| 35 | Web Vulnerability     | CSRF (Cross-Site)        |
| 36 | Web Vulnerability     | Directory Traversal      |
| 37 | Advanced Malware      | Polymorphic Virus        |
| 38 | Network Protocol      | BGP Hijacking            |
| 39 | Authentication        | Session Hijacking        |
| 40 | Authentication        | MFA Fatigue / Bombing    |
| 41 | Cloud / Web           | SSRF (Server-Side)       |
| 42 | Email Threat          | BEC (Business Email)     |
| 43 | Threat Intelligence   | Known Malicious IP Comm. |
| 44 | Execution             | PowerShell Downgrade     |
| 45 | Access Credential     | Golden Ticket Attack     |
| 46 | Defense Evasion       | Log Tampering / Clearing |
| 47 | Email Threat          | Spear Phishing Link      |
| 48 | Network Flood         | SYN Flood Attack         |
| 49 | Data Parsing          | XXE Injection            |
| 50 | Hardware Evasion      | Rogue USB Insertion      |

## Phase 3C: Human-in-the-Loop Decision Engine ✅
- [x] Minor incidents (score ≥ 90%) → auto-blocked
- [x] Noise (score < 50%) → auto-closed
- [x] Major incidents (50-89%, blast ≥ 3, rule ≥ 13) → human analyst asked
- [x] 5 action options (Block, Investigate, Monitor, False Positive, Lockdown)

## Phase 3D: Self-Learning Feedback Loop ✅
- [x] `ai/feedback_loop.py` — logs every incident for model retraining
- [x] Auto-retrain after 50 incidents, only saves if accuracy improves

## Phase 3E: Report Generator Enhancement ✅
- [x] 10-section PDF + 18-term glossary + plain-English explanations

## GitHub Repository ✅
- [x] Pushed to [github.com/Pranav2245/SOAR](https://github.com/Pranav2245/SOAR)
- [x] Single contributor (Pranav2245)

## SRS Document ✅
- [x] SOFTWARE_REQUIREMENT_SPECIFICATION.txt created
- [x] Architecture Diagram (Mermaid) in project_diagrams.md
- [x] PERT Chart (Mermaid) in project_diagrams.md
- [x] Workflow Sequence Diagram in project_diagrams.md
- [x] Use Case Diagram description
- [x] Data Flow Diagram description

---

## Phase 4: AI Dashboard (MERN Stack) 🔲
- [ ] 4.0 MongoDB Database (users, login_history, incident_actions)
- [ ] 4.1 Login Page (React, dark theme, bcrypt via Node.js, role-based: analyst/user)
- [ ] 4.2 Frontend Architecture (React Router, Context API, Navbar + Sidebar components, role badges)
- [ ] 4.2b Express.js & Node.js Backend API (Auth, Incident Endpoints, AI Integrations)
- [ ] 4.3 Command Center (threat gauge, stat cards, live feed, map)
- [ ] 4.4 Incident Response — human-in-the-loop in browser (SOC only)
- [ ] 4.5 Vulnerability Scanner (client check, CVE table, port scan)
- [ ] 4.6 AI Intelligence (accuracy charts, self-learning progress)
- [ ] 4.7 Network Topology — interactive graph (SOC only)
- [ ] 4.8 Phishing Analyzer (paste email → score)
- [ ] 4.9 Reports & Analytics (MTTR, heatmap, PDF downloads)
- [ ] 4.10 System Health (container status, log volume)
- [ ] 4.11 Audit Log + Settings (SOC only)

## Phase 5: Docker Infrastructure Fix 🔲
- [ ] Generate Wazuh TLS certs and verify all containers

## Phase 6: Documentation & Finalization 🔲
- [ ] Update README with full project documentation
- [ ] Add LICENSE file + copyright headers
