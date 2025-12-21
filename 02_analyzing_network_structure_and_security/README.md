# Network Defense & Incident Response Analysis

## Project Description

This project demonstrates the identification, analysis, and mitigation of Denial of Service (DoS) attacks. It showcases the ability to analyze network traffic logs to diagnose specific attack vectors (TCP SYN Floods) and apply the **NIST Cybersecurity Framework (CSF)** to manage the incident lifecycle for Distributed Denial of Service (DDoS) events.

## Scenario 1: Technical Traffic Analysis (TCP SYN Flood)

**Incident:** Users reported connection timeout errors when attempting to access the company web server.
**Investigation:** Analyzed network logs and identified a massive influx of TCP connection requests on Port 443 (HTTPS) from a single unknown IP address (`203.0.113.0`).

### Technical Diagnosis

- **Attack Vector:** **SYN Flood**. The attacker exploited the TCP "Three-Way Handshake" process.
- **Mechanism:**

1. The attacker sent high volumes of **SYN** (Synchronize) packets.
2. The server responded with **SYN-ACK** and reserved memory/resources for the connection.
3. The attacker intentionally failed to send the final **ACK** (Acknowledge).

- **Impact:** The server's resources were exhausted keeping these "half-open" connections alive, causing it to drop legitimate traffic and time out.

## Scenario 2: Incident Response Lifecycle (NIST Framework)

**Incident:** A complete stoppage of network services indicated a potential Distributed Denial of Service (DDoS) attack utilizing ICMP packets.
**Framework Application:** I utilized the NIST CSF (Identify, Protect, Detect, Respond, Recover) to manage the incident.

### 1. Identify

- **Tooling:** Deployed `tcpdump` to capture and analyze live network traffic.
- **Finding:** Logs revealed a flood of incoming **ICMP** (Ping) packets from multiple spoofed source IPs, confirming a DDoS attack targeting network bandwidth.

### 2. Protect & Detect

- **Hardening:** Configured firewall rules to limit the rate of incoming ICMP packets.
- **Validation:** Implemented **Source IP Verification** on the firewall to reject spoofed traffic.
- **Monitoring:** Deployed an Intrusion Detection System (IDS) to flag abnormal traffic patterns in real-time.

### 3. Respond & Recover

- **Containment:** The Incident Response team blocked the malicious ICMP traffic and temporarily took non-critical services offline to preserve bandwidth for essential functions.
- **Restoration:** Critical services were systematically brought back online once traffic normalized.
- **Governance:** Post-incident reporting reinforced the need for stronger edge defenses to stakeholders.

## Summary

This project highlights a dual-competency in cybersecurity:

1. **Forensic Depth:** Understanding the TCP/IP stack to diagnose how a SYN flood exhausts server resources.
2. **Operational Breadth:** Using the NIST framework to coordinate a structured response to a distributed attack, moving from identification to full recovery.
