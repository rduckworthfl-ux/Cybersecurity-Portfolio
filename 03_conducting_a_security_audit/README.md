# Security Control & Compliance Audit (Botium Toys)

## Project Description

This project involved a comprehensive internal security audit for Botium Toys to assess their adherence to industry standards and regulatory frameworks. The objective was to perform a **Gap Analysis**—identifying where current security controls fell short of best practices and legal requirements, specifically regarding **PCI DSS**, **GDPR**, and **SOC 2**.

## Scenario & Scope

Botium Toys is growing, and with growth comes scrutiny. The audit examined the current state of administrative, technical, and physical controls to determine readiness for international data handling and secure payment processing.

- **Audit Target:** Internal IT Infrastructure and Policy Framework.
- **Compliance Standards:**
- **PCI DSS:** Payment Card Industry Data Security Standard (Credit Card Security).
- **GDPR:** General Data Protection Regulation (EU Privacy).
- **SOC 2:** Service Organization Control (Trust Services Criteria).

## Audit Findings: The "Gap Analysis"

### 1. Control Assessment (Current State)

I reviewed the existing implementation of critical security controls. While the organization had strong physical security and basic backups, significant gaps were identified in identity management and network monitoring.

- **Effective Controls:** Antivirus software, Firewalls, Backups, and Physical Security (Locks, CCTV).
- **Critical Gaps (High Risk):**
- **Least Privilege:** Not implemented. Users likely have excessive permissions.
- **Separation of Duties:** No policy exists to prevent fraud/error by dividing tasks.
- **Encryption:** Data at rest and in transit is not adequately encrypted (Major PCI DSS violation).
- **Intrusion Detection (IDS):** No visibility into active network threats.

### 2. Compliance Verification

**PCI DSS (Payment Security):**

- **Status:** **Non-Compliant**.
- **Finding:** While credit card info is stored internally, it is **not encrypted**, and there are gaps in password management policies.

**GDPR (EU Privacy):**

- **Status:** **Non-Compliant**.
- **Finding:** No procedures exist for notifying EU customers within 72 hours of a breach, and privacy policies for data handling are absent.

## Strategic Recommendations

To move from a vulnerable state to a compliant posture, I proposed the following remediations:

### Administrative Controls (Policy & Process)

- **Least Privilege & Separation of Duties:** Immediately restructure user roles to ensure employees only have access necessary for their job functions. This limits the "blast radius" of a compromised account.
- **Disaster Recovery Plan:** Develop a formal plan to ensure business continuity and timely data recovery during an incident.
- **Password Policies:** Enforce complexity requirements and rotation schedules to mitigate brute-force and dictionary attacks.

### Technical Controls (Hardware & Software)

- **Encryption:** Implement robust encryption for all customer credit card data to satisfy PCI DSS requirements and protect against data theft.
- **IDS/IPS Implementation:** Deploy Intrusion Detection/Prevention Systems to monitor traffic patterns and identify anomalies in real-time.
- **Legacy Management:** Replace or strictly monitor legacy systems that can no longer receive security updates.

### Physical Controls

- **Deterrence:** Install clear signage regarding alarm systems and surveillance to act as a psychological deterrent to physical intrusion.

## Summary

This audit served as a reality check for the organization. By highlighting critical deficiencies in **Encryption**, **Access Control**, and **Breach Notification**, the report provides a clear roadmap for the IT team to secure the budget and resources needed to achieve regulatory compliance and protect customer trust.
