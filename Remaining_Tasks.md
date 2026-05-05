# SOAR Project: Final Actionable Task List

Use this granular checklist to complete the final outstanding phases of the project.

### Phase 4: Automated Mitigation (Cortex)
- [ ] Log in to the Cortex Web UI at `http://localhost:9001` with `admin` / `secret`.
- [ ] Navigate to the **Organization** -> **Responders** tab.
- [ ] Click the **Refresh Responders** button if the list is empty.
- [ ] Locate the `SOAR_Block_IP` responder in the list.
- [ ] Click **Enable**, and enter the Wazuh Manager API credentials (`wazuh-wui` / `MyS3cr37P450r.*-`).
- [ ] Trigger the responder manually from an open case in TheHive to verify `firewall-drop` executes on the Kali VM.

### Phase 5: Self-Learning AI & Triage
- [ ] Ensure all 3 AI models (`triage_model.pkl`, `anomaly_model.pkl`, `phishing_model.pkl`) are present in the `ai/` directories.
- [ ] Verify that `feedback_loop.py` is configured to run continuously or as a cron job to parse closed cases from TheHive.
- [ ] Close 5 previously opened cases in TheHive as "True Positive" to trigger a simulated feedback loop cycle.
- [ ] Check the `ai/feedback/retrain_history.json` file to confirm the models successfully logged a retraining event.

### Phase 6: Final Review & Project Documentation
- [ ] Consolidate all project screenshots (Wazuh Dashboard, TheHive Case, Cortex Responder) into a `Final_Presentation/` folder.
- [ ] Run the `report_generator.py` (if configured) to generate the final PDF incident summary.
- [ ] Finalize the presentation slides, embedding the `SOAR_Phases.md` roadmap and the Architecture diagram.
- [ ] Double-check that all proprietary sensitive data (e.g., live `.env` passwords) is scrubbed before submitting the codebase via GitHub.
