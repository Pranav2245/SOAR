# SOAR Project: Final System Documentation

## Executive Summary
This project delivers a comprehensive, state-of-the-art Security Orchestration, Automation, and Response (SOAR) platform. It successfully bridges traditional SIEM capabilities with advanced, self-learning Artificial Intelligence, providing a fully automated pipeline from initial threat detection to autonomous active response and PDF report generation.

## 1. Infrastructure Architecture
The backend is entirely containerized using Docker, ensuring portability and isolated dependency management. The core services communicate over a secure virtual network (`soar-network`):

*   **Wazuh Manager (SIEM):** The core ingestion engine receiving telemetry from endpoint agents.
*   **Wazuh Indexer & Dashboard:** OpenSearch-based storage and raw data visualization.
*   **TheHive:** Centralized incident response and case management system.
*   **Cortex:** The analysis engine responsible for executing Active Responders (e.g., firewall blocks).
*   **MISP:** Threat Intelligence platform used to cross-reference IPs and file hashes against known global IOCs (Indicator of Compromise).
*   **Redis & Cassandra & Elasticsearch:** The underlying high-performance databases supporting the stack.

## 2. Endpoint Deployment (Kali Linux)
A Kali Linux virtual machine acts as the monitored endpoint. It runs the **Wazuh Agent (v4.9.0)**, which actively streams system logs, authentication attempts, file integrity checks, and network traffic to the Wazuh Manager. The infrastructure successfully detects simulated attacks (such as SSH Brute Force and MITRE ATT&CK techniques) executed on this VM.

## 3. AI Intelligence Suite
The cornerstone of this SOAR platform is the 8-module AI suite designed to reduce alert fatigue and automate Level-1 SOC triage:

1.  **ML Triage Analyzer:** Uses an XGBoost classifier to assign an exact severity score (0-100%) to incoming alerts based on 10+ telemetry features (Rule Level, Time of Day, MITRE tags).
2.  **Anomaly Detection:** Employs the Isolation Forest algorithm to establish a baseline of "normal" behavior and flag deviations.
3.  **Phishing NLP Parser:** Uses TF-IDF vectorization and Logistic Regression to analyze raw email text and detect social engineering attempts.
4.  **Blast Radius Calculator:** Uses network topology mapping (NetworkX) to determine how many other systems are exposed if a specific host is compromised.
5.  **Alert Clustering:** Uses DBSCAN to group thousands of similar, noisy alerts into a single cohesive "Campaign" for the analyst.
6.  **Automated Mitigator:** Maps high-severity attacks to immediate physical responses (e.g., dropping packets via `iptables`).
7.  **PDF Report Generator:** Automatically compiles forensic data into a clean, management-ready PDF incident report.
8.  **Self-Learning Feedback Loop:** Automatically retraining models based on real-time human decisions made in the dashboard.

## 4. Evaluation Methodology
To ensure academic and technical rigor, the AI models strictly adhere to a **Cross-Dataset Evaluation Protocol**:
*   **Training:** Models are trained entirely on algorithmically generated synthetic data mimicking typical network patterns.
*   **Testing:** Models are evaluated against the real-world **KDD Cup '99** dataset. This proves the models generalize to real-world threats rather than simply memorizing the synthetic data, resulting in highly accurate real-time predictions.

## 5. Security Operations Dashboard
The user interface is a custom-built, React/Node.js web application featuring a premium, dark-themed glassmorphic design. It features:
*   **Role-Based Access:** Segregated views for SOC Analysts (Full Control) and standard Users (Read-Only).
*   **Command Center:** Real-time threat gauges, MTTR (Mean Time to Respond) metrics, and severity heatmaps.
*   **Incident Response:** A ticketing queue allowing analysts to investigate, isolate, or mark alerts as false positives with a single click.

## Conclusion
This project successfully demonstrates the design, deployment, and operational efficacy of a localized Security Orchestration, Automation, and Response (SOAR) architecture. By strategically integrating Wazuh, TheHive, Cortex, and MISP, the system establishes a highly automated, zero-touch mitigation pipeline. 

The successful execution of adversarial simulations (such as SSH brute-force) proved the platform's capability to detect and autonomously mitigate threats in a matter of seconds. Furthermore, the integration of a custom AI suite allows the architecture to adapt to specific environments based on continuous analyst feedback. Ultimately, this deployment proves that enterprise-grade, automated defense systems can be effectively synthesized using open-source tools, dramatically reducing the "Time to Mitigate" (TTM) and providing a scalable foundation for modern Security Operations Centers.
