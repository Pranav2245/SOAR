# SOAR Project: Automated Security Operations Architecture

This project implements a complete Security Orchestration, Automation, and Response (SOAR) architecture using open-source tools: **Wazuh**, **TheHive**, **Cortex**, **MISP**, and the **ELK Stack**.
It is designed to be deployed on a Mac host using Docker, with agents installed on a Kali Linux Virtual Machine.

---

## 1. Architecture Overview

### Components
- **Wazuh (SIEM & XDR):** Collects logs from agents, analyzes them using rules, and triggers alerts.
- **TheHive (Case Management):** Receives alerts from Wazuh via a custom webhook and organizes them into cases for analysts.
- **Cortex (Analysis & Response Engine):** Acts as the automation brain behind TheHive. Analyzes observables (IPs, domains, hashes) and executes automated response scripts.
- **MISP (Threat Intelligence):** A shared database of Threat Intelligence. Cortex uses MISP to enrich alerts with known malicious indicators.
- **Kali Linux VM (Target Endpoint):** Simulates an endpoint in the network where attacks happen and the Wazuh Agent is installed.

### Data Flow Pipeline
1. **Detection:** An attacker scans/exploits the Kali VM. The Wazuh Agent relays logs to the Wazuh Manager.
2. **Analysis:** Wazuh Manager matches logs against `custom_rules.xml`. If the severity level is > 7, it triggers the `wazuh_to_thehive.py` integration script.
3. **Escalation:** The script creates an Alert (or Case) in TheHive via its REST API, attaching the source IP as an "observable".
4. **Enrichment:** TheHive runs a Cortex Analyzer (e.g., `mock_ip_reputation.py` or MISP integration) against the IP. 
5. **Response:** If the IP is confirmed malicious, Cortex executes a Responder (`wazuh_block_ip.py`). The responder sends an API call back to Wazuh to trigger an Active Response (e.g., `firewall-drop`).
6. **Mitigation:** Wazuh pushes the block command to the Kali VM agent, effectively cutting off the attacker.
   
---

## 2. Setup Guide (Mac Host + Kali VM)

### Prerequisites
- **Mac Host:** Docker Engine (Docker Desktop or Colima), Docker Compose.
- **Kali VM:** Installed via VMware Fusion, Parallels, or UTM.

### A. Environment Configuration
1. **Networking:** In your Hypervisor settings, your VM is currently using the default **Shared Network** (which assigns IPs like `192.168.64.x`). This is perfect! The Mac and VM can communicate bidirectionally.
2. The VM's IP address is `192.168.64.9`. The Mac's IP address on this VM network is `192.168.64.1`.

### B. Launching the SOAR Stack (on Mac)
1. Clone / Navigate to this project directory: `cd SOAR`
2. Start the Docker infrastructure:
   ```bash
   docker-compose up -d
   ```
   *Note: This will deploy Wazuh, Elasticsearch, TheHive, Cassandra, Cortex, MISP, and MariaDB. It requires at least 8-12GB of RAM allocated to Docker.*
3. Verify containers are running: `docker ps`

### C. Agent Installation (on Kali VM)
1. Transfer the `scripts/agent_install.sh` to the Kali VM using `scp` (Secure Copy). Run this on your Mac terminal:
   ```bash
   scp scripts/agent_install.sh kali@192.168.64.9:/home/kali/
   ```
2. Connect to the Kali VM via SSH:
   ```bash
   ssh kali@192.168.64.9
   ```
3. Inside the Kali VM, make the script executable: `chmod +x agent_install.sh`
4. Run the installer pointing to your Mac's IP address (where Wazuh Manager is hosted):
   ```bash
   sudo ./agent_install.sh 192.168.64.1
   ```
5. Verify the agent connects successfully in the Wazuh Dashboard (`https://localhost:5601` on Mac).

---

## 3. Custom Configurations & Playbooks

- **Wazuh Integrations:** The `integrations/wazuh_to_thehive.py` script must be copied into the `/var/ossec/integrations/` directory of the `wazuh.manager` container. It allows automated forwarding of high-severity alerts.
- **Cortex Analyzers:** Located in `cortex/analyzers/`. These Python scripts analyze observables against threat databases.
- **Cortex Responders:** Located in `cortex/responders/`. These scripts take automated action (e.g., interacting with Wazuh's API to ban an IP).

### Running a Test End-to-End Workflow
1. On the Kali VM, trigger a custom rule. For example, use netcat: `nc -e /bin/bash 127.0.0.1 4444` (simulating a reverse shell).
2. Wazuh detects this (Rule ID `100002` from `custom_rules.xml`).
3. View TheHive dashboard (`http://localhost:9000`). A new case/alert should automatically appear.
4. Run the Cortex IP Analyzer on the associated Source IP.
5. If malicious, run the Cortex Responder to block the IP. Verify on the Kali VM by checking iptables (`sudo iptables -L`).
