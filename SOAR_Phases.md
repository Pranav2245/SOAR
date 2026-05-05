# SOAR Project: Detailed 6-Phase Roadmap

### ✅ COMPLETED PHASES (Phases 1-3)

- [x] **Phase 1: Environment Setup & Core Infrastructure**
  *We successfully containerized the entire backend using Docker. This included spinning up the ELK Stack (Elasticsearch), Wazuh Manager, TheHive, Cortex, and MISP databases on a unified virtual network (`soar-network`) with secure TLS certificates.*

- [x] **Phase 2: Agent Deployment & Threat Detection**
  *We provisioned the Kali Linux VM as our target endpoint. We successfully downgraded and installed the Wazuh Agent (`v4.9.0`) to ensure compatibility, established the connection to the Manager, and proved the SIEM could detect active threats (like our simulated SSH Brute Force attack).*

- [x] **Phase 3: Integration & Alert Orchestration**
  *We bridged the gap between detection and case management. We wrote the custom Python integration (`wazuh_to_thehive.py`) that successfully intercepts high-severity Wazuh alerts and automatically forwards them as actionable "Cases" into TheHive dashboard.*

---

### ✅ COMPLETED PHASES (Phases 4-6)

- [x] **Phase 4: Automated Mitigation & Responders**
  *We successfully loaded the `wazuh_block_ip.py` script into Cortex and finalized the integration. Cortex can now trigger an automated active response (e.g., dropping the firewall on the Kali VM) the moment a malicious IP is identified.*

- [x] **Phase 5: Self-Learning AI & Autonomous Triage**
  *We connected the Machine Learning algorithms (`ai/feedback_loop.py`, XGBoost, Isolation Forest) to the React Dashboard. As analysts resolve cases, the data is continuously fed back into these AI models so they automatically prioritize future alerts and retrain themselves.*

- [x] **Phase 6: Final Review, Dashboard Polish, & Reporting**
  *We brought the entire project together for the final presentation. We successfully generated automated PDF Incident Reports (`INC-CRITICAL-001.pdf`), polished the React dashboard UI to dynamically display them, and drafted the comprehensive `SOAR_Final_Report.md` system documentation.*
