#!/usr/bin/env python3
"""
Module 3.1: ML Triage Analyzer
===============================
Uses XGBoost to score incoming Wazuh alerts with a confidence level.
  - Score > 90%  → Auto-block (zero-touch)
  - Score 50-89% → Human review in TheHive
  - Score < 50%  → Auto-close as noise

Includes:
  - Synthetic training data generator
  - Model training pipeline
  - Prediction function for live alerts
"""

import json
import os
import pickle
import numpy as np
import pandas as pd
from datetime import datetime

try:
    from xgboost import XGBClassifier
except ImportError:
    print("Installing xgboost...")
    os.system("pip install xgboost")
    from xgboost import XGBClassifier

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score

MODEL_PATH = os.path.join(os.path.dirname(__file__), "triage_model.pkl")


def generate_synthetic_data(n_samples=5000) -> pd.DataFrame:
    """
    Generate comprehensive synthetic Wazuh alert data for training.
    Covers 12 attack types + normal operations with realistic distributions.
    """
    np.random.seed(42)
    data = []

    # --- ATTACK SCENARIOS (labeled as 1 = malicious) ---
    attack_types = {
        # 1. SSH Brute Force
        "brute_force": {
            "rule_level": (10, 14), "hour_of_day": (0, 6), "day_of_week": (0, 7),
            "failed_logins": (20, 150), "src_ip_is_internal": 0,
            "src_ip_reputation": (60, 100), "agent_os": [0, 1],
            "event_count_1h": (50, 300), "is_fim_event": 0, "has_mitre_tag": 1,
        },
        # 2. Ransomware
        "ransomware": {
            "rule_level": (13, 15), "hour_of_day": (0, 24), "day_of_week": (0, 7),
            "failed_logins": (0, 3), "src_ip_is_internal": 0,
            "src_ip_reputation": (80, 100), "agent_os": [1],  # Mostly Windows
            "event_count_1h": (100, 500), "is_fim_event": 1, "has_mitre_tag": 1,
        },
        # 3. C2 Beacon (Command & Control)
        "c2_beacon": {
            "rule_level": (8, 12), "hour_of_day": (0, 24), "day_of_week": (0, 7),
            "failed_logins": (0, 1), "src_ip_is_internal": 0,
            "src_ip_reputation": (70, 100), "agent_os": [0, 1, 2],
            "event_count_1h": (10, 60), "is_fim_event": 0, "has_mitre_tag": 1,
        },
        # 4. Data Exfiltration
        "data_exfil": {
            "rule_level": (10, 14), "hour_of_day": (0, 6), "day_of_week": (5, 7),
            "failed_logins": (0, 2), "src_ip_is_internal": 0,
            "src_ip_reputation": (30, 80), "agent_os": [0, 1],
            "event_count_1h": (20, 100), "is_fim_event": 1, "has_mitre_tag": 1,
        },
        # 5. Privilege Escalation
        "priv_esc": {
            "rule_level": (11, 15), "hour_of_day": (0, 24), "day_of_week": (0, 7),
            "failed_logins": (3, 15), "src_ip_is_internal": 1,
            "src_ip_reputation": (0, 10), "agent_os": [0],  # Linux
            "event_count_1h": (5, 40), "is_fim_event": 1, "has_mitre_tag": 1,
        },
        # 6. Web Application Attack (SQLi, XSS, RFI)
        "web_attack": {
            "rule_level": (9, 13), "hour_of_day": (0, 24), "day_of_week": (0, 7),
            "failed_logins": (0, 2), "src_ip_is_internal": 0,
            "src_ip_reputation": (40, 95), "agent_os": [0],  # Linux web servers
            "event_count_1h": (30, 200), "is_fim_event": 0, "has_mitre_tag": 1,
        },
        # 7. Lateral Movement
        "lateral_movement": {
            "rule_level": (10, 14), "hour_of_day": (0, 6), "day_of_week": (0, 7),
            "failed_logins": (5, 30), "src_ip_is_internal": 1,
            "src_ip_reputation": (0, 10), "agent_os": [0, 1],
            "event_count_1h": (20, 80), "is_fim_event": 0, "has_mitre_tag": 1,
        },
        # 8. Rootkit / Persistence
        "rootkit": {
            "rule_level": (12, 15), "hour_of_day": (0, 24), "day_of_week": (0, 7),
            "failed_logins": (0, 1), "src_ip_is_internal": 0,
            "src_ip_reputation": (50, 100), "agent_os": [0],
            "event_count_1h": (5, 30), "is_fim_event": 1, "has_mitre_tag": 1,
        },
        # 9. Cryptomining
        "cryptomining": {
            "rule_level": (7, 11), "hour_of_day": (0, 24), "day_of_week": (0, 7),
            "failed_logins": (0, 1), "src_ip_is_internal": 0,
            "src_ip_reputation": (40, 80), "agent_os": [0],
            "event_count_1h": (50, 300), "is_fim_event": 0, "has_mitre_tag": 1,
        },
        # 10. Phishing Click (user clicked malicious link)
        "phishing_click": {
            "rule_level": (8, 12), "hour_of_day": (8, 18), "day_of_week": (0, 5),
            "failed_logins": (0, 3), "src_ip_is_internal": 1,
            "src_ip_reputation": (0, 20), "agent_os": [1, 2],  # Windows/Mac workstations
            "event_count_1h": (5, 30), "is_fim_event": 0, "has_mitre_tag": 1,
        },
        # 11. Insider Threat (unusual data access)
        "insider_threat": {
            "rule_level": (7, 11), "hour_of_day": (22, 24), "day_of_week": (5, 7),
            "failed_logins": (1, 5), "src_ip_is_internal": 1,
            "src_ip_reputation": (0, 5), "agent_os": [0, 1, 2],
            "event_count_1h": (10, 50), "is_fim_event": 1, "has_mitre_tag": 0,
        },
        # 12. DDoS / Flood Attack
        "ddos": {
            "rule_level": (10, 14), "hour_of_day": (0, 24), "day_of_week": (0, 7),
            "failed_logins": (0, 5), "src_ip_is_internal": 0,
            "src_ip_reputation": (50, 100), "agent_os": [0],
            "event_count_1h": (200, 500), "is_fim_event": 0, "has_mitre_tag": 1,
        },
    }

    # Generate attack samples (~250 per type = 3000 total)
    samples_per_attack = n_samples // 5 // len(attack_types)
    for attack_name, profile in attack_types.items():
        for _ in range(max(samples_per_attack, 50)):
            rl = profile["rule_level"]
            hod = profile["hour_of_day"]
            fl = profile["failed_logins"]
            srep = profile["src_ip_reputation"]

            row = {
                "rule_level": np.random.randint(rl[0], rl[1] + 1),
                "hour_of_day": np.random.randint(hod[0], min(hod[1], 24)),
                "day_of_week": np.random.randint(profile["day_of_week"][0], profile["day_of_week"][1]),
                "failed_logins": np.random.randint(fl[0], fl[1] + 1),
                "src_ip_is_internal": profile["src_ip_is_internal"],
                "src_ip_reputation": np.random.randint(srep[0], srep[1] + 1) if isinstance(srep, tuple) else srep,
                "agent_os": int(np.random.choice(profile["agent_os"])),
                "event_count_1h": np.random.randint(profile["event_count_1h"][0], profile["event_count_1h"][1] + 1),
                "is_fim_event": profile["is_fim_event"],
                "has_mitre_tag": profile["has_mitre_tag"],
                "label": 1,  # Malicious
            }
            data.append(row)

    # --- NORMAL OPERATIONS (labeled as 0 = benign) ---
    normal_scenarios = {
        "routine_login": {
            "rule_level": (1, 5), "hour_of_day": (7, 19), "failed_logins": (0, 2),
            "src_ip_is_internal": 1, "src_ip_reputation": (0, 5),
            "event_count_1h": (1, 30), "is_fim_event": 0, "has_mitre_tag": 0,
        },
        "system_update": {
            "rule_level": (3, 7), "hour_of_day": (2, 5), "failed_logins": (0, 0),
            "src_ip_is_internal": 1, "src_ip_reputation": (0, 0),
            "event_count_1h": (10, 80), "is_fim_event": 1, "has_mitre_tag": 0,
        },
        "developer_activity": {
            "rule_level": (2, 6), "hour_of_day": (9, 20), "failed_logins": (0, 3),
            "src_ip_is_internal": 1, "src_ip_reputation": (0, 5),
            "event_count_1h": (5, 60), "is_fim_event": 1, "has_mitre_tag": 0,
        },
        "admin_tasks": {
            "rule_level": (3, 8), "hour_of_day": (8, 18), "failed_logins": (0, 2),
            "src_ip_is_internal": 1, "src_ip_reputation": (0, 5),
            "event_count_1h": (3, 40), "is_fim_event": 0, "has_mitre_tag": 0,
        },
        "monitoring_noise": {
            "rule_level": (1, 4), "hour_of_day": (0, 24), "failed_logins": (0, 1),
            "src_ip_is_internal": 1, "src_ip_reputation": (0, 0),
            "event_count_1h": (1, 15), "is_fim_event": 0, "has_mitre_tag": 0,
        },
        "vpn_login": {
            "rule_level": (3, 6), "hour_of_day": (6, 22), "failed_logins": (0, 3),
            "src_ip_is_internal": 0, "src_ip_reputation": (0, 15),
            "event_count_1h": (1, 10), "is_fim_event": 0, "has_mitre_tag": 0,
        },
        "backup_job": {
            "rule_level": (2, 5), "hour_of_day": (1, 5), "failed_logins": (0, 0),
            "src_ip_is_internal": 1, "src_ip_reputation": (0, 0),
            "event_count_1h": (20, 100), "is_fim_event": 1, "has_mitre_tag": 0,
        },
        "ci_cd_pipeline": {
            "rule_level": (2, 6), "hour_of_day": (0, 24), "failed_logins": (0, 1),
            "src_ip_is_internal": 1, "src_ip_reputation": (0, 5),
            "event_count_1h": (10, 120), "is_fim_event": 1, "has_mitre_tag": 0,
        },
    }

    # Generate normal samples to balance the dataset
    normal_per_type = (n_samples - len(data)) // len(normal_scenarios)
    for scenario_name, profile in normal_scenarios.items():
        for _ in range(max(normal_per_type, 100)):
            rl = profile["rule_level"]
            hod = profile["hour_of_day"]
            fl = profile["failed_logins"]
            srep = profile["src_ip_reputation"]

            row = {
                "rule_level": np.random.randint(rl[0], rl[1] + 1),
                "hour_of_day": np.random.randint(hod[0], min(hod[1], 24)),
                "day_of_week": np.random.randint(0, 7),
                "failed_logins": np.random.randint(fl[0], fl[1] + 1),
                "src_ip_is_internal": profile["src_ip_is_internal"],
                "src_ip_reputation": np.random.randint(srep[0], srep[1] + 1),
                "agent_os": int(np.random.choice([0, 1, 2])),
                "event_count_1h": np.random.randint(profile["event_count_1h"][0], profile["event_count_1h"][1] + 1),
                "is_fim_event": profile["is_fim_event"],
                "has_mitre_tag": profile["has_mitre_tag"],
                "label": 0,  # Benign
            }
            data.append(row)

    return pd.DataFrame(data)


def train_model():
    """Train an XGBoost classifier on synthetic alert data."""
    print("[*] Generating synthetic training data...")
    df = generate_synthetic_data(2000)

    features = [
        "rule_level", "hour_of_day", "day_of_week",
        "failed_logins", "src_ip_is_internal", "src_ip_reputation",
        "agent_os", "event_count_1h", "is_fim_event", "has_mitre_tag"
    ]

    X = df[features]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("[*] Training XGBoost classifier...")
    model = XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        use_label_encoder=False,
        eval_metric='logloss',
        random_state=42
    )
    model.fit(X_train, y_train)

    # Evaluate
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    print("\n[+] === Model Evaluation ===")
    print(classification_report(y_test, y_pred, target_names=["Benign", "Malicious"]))
    print(f"ROC AUC Score: {roc_auc_score(y_test, y_proba):.4f}")

    # Save model
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
    print(f"[+] Model saved to {MODEL_PATH}")

    return model


def predict_threat(alert_data: dict) -> dict:
    """
    Predict the threat confidence score for a Wazuh alert.

    Args:
        alert_data: Dict with keys matching the feature names.

    Returns:
        Dict with confidence_score, decision, and details.
    """
    if not os.path.exists(MODEL_PATH):
        print("[!] No trained model found. Training now...")
        train_model()

    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)

    features = pd.DataFrame([{
        "rule_level": alert_data.get("rule_level", 5),
        "hour_of_day": alert_data.get("hour_of_day", datetime.now().hour),
        "day_of_week": alert_data.get("day_of_week", datetime.now().weekday()),
        "failed_logins": alert_data.get("failed_logins", 0),
        "src_ip_is_internal": alert_data.get("src_ip_is_internal", 1),
        "src_ip_reputation": alert_data.get("src_ip_reputation", 0),
        "agent_os": alert_data.get("agent_os", 0),
        "event_count_1h": alert_data.get("event_count_1h", 1),
        "is_fim_event": alert_data.get("is_fim_event", 0),
        "has_mitre_tag": alert_data.get("has_mitre_tag", 0),
    }])

    confidence = float(model.predict_proba(features)[0][1]) * 100

    # Decision logic
    if confidence >= 90:
        decision = "AUTO_BLOCK"
        action = "Automatically blocked. Zero-touch response triggered."
    elif confidence >= 50:
        decision = "HUMAN_REVIEW"
        action = "Escalated to SOC analyst for manual review in TheHive."
    else:
        decision = "AUTO_CLOSE"
        action = "Closed as noise. No action required."

    return {
        "confidence_score": round(confidence, 2),
        "decision": decision,
        "action": action,
        "features_used": features.to_dict(orient='records')[0]
    }


# --- Cortex Analyzer Interface ---
def run_as_cortex_analyzer():
    """Run as a Cortex analyzer (reads from stdin)."""
    import sys
    input_data = sys.stdin.read()
    if not input_data:
        print(json.dumps({"success": False, "errorMessage": "No input"}))
        sys.exit(1)

    job = json.loads(input_data)
    observable = job.get("observable", {}).get("data", "")

    # Parse the alert data from the observable or job config
    alert_features = job.get("parameters", {}).get("alert_features", {})
    if not alert_features:
        alert_features = {"rule_level": 10, "failed_logins": 5}

    result = predict_threat(alert_features)

    level = "malicious" if result["decision"] == "AUTO_BLOCK" else \
            "suspicious" if result["decision"] == "HUMAN_REVIEW" else "safe"

    output = {
        "success": True,
        "summary": {
            "taxonomies": [{
                "level": level,
                "namespace": "MLTriage",
                "predicate": "Confidence",
                "value": f"{result['confidence_score']}%"
            }]
        },
        "full": result
    }
    print(json.dumps(output))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--train":
        train_model()
    elif len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_alert = {
            "rule_level": 12,
            "hour_of_day": 3,
            "failed_logins": 50,
            "src_ip_is_internal": 0,
            "src_ip_reputation": 85,
            "agent_os": 0,
            "event_count_1h": 120,
            "is_fim_event": 0,
            "has_mitre_tag": 1
        }
        result = predict_threat(test_alert)
        print(json.dumps(result, indent=2))
    else:
        run_as_cortex_analyzer()
