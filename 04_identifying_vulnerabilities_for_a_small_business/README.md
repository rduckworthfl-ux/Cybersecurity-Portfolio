# NIST-Based Vulnerability Assessment & Hardening

## Project Description

This project involved a comprehensive vulnerability assessment of a critical database server hosting Personally Identifiable Information (PII) and Sensitive PII (SPII). The objective was to evaluate the current security posture against the **NIST SP 800-30 Rev. 1** framework and provide actionable remediation strategies to mitigate risks associated with data exfiltration and denial of service (DoS).

## Scenario & Scope

The target system was a high-performance Linux server running a MySQL database management system. This asset is critical to business operations as it serves as the primary repository for customer and employee data.

- **Assessment Period:** June 2024 – August 2024
- **Asset Value:** High (Contains Customer PII, Employee SPII, and IP addresses)
- **Threat Landscape:** Unauthorized access, Data Exfiltration, Denial of Service (DoS)

## Methodology

The assessment followed the NIST risk analysis guidelines to identify vulnerabilities across three control layers: **Technical**, **Operational**, and **Managerial**. The focus was not just on patching software, but on implementing a defense-in-depth architecture.

## Risk Analysis & Remediation Strategy

### 1. Technical Controls (Hardening)

**Objective:** Reduce the attack surface and enforce strict access control.

- **Network Filtering:** Implemented firewall rules to restrict traffic on Port 3306 (MySQL). Only authorized internal IP addresses are permitted; all public traffic is dropped to mitigate DoS attacks.
- **Access Control:** Mandated **IP Whitelisting** for workstations and enforced **Multi-Factor Authentication (MFA)** for all database access.
- **Encryption:** Deployed **Public Key Infrastructure (PKI)** to secure data in transit and prevent exfiltration via man-in-the-middle attacks.

### 2. Operational Controls (Monitoring)

**Objective:** Detect anomalies before they become breaches.

- **Auditing:** Established a schedule for regular security audits of MySQL logs. This ensures that suspicious behavior—such as repeated failed login attempts or unusual query patterns—is identified immediately.

### 3. Managerial Controls (Human Factor)

**Objective:** Mitigate insider threats and negligence.

- **Security Awareness:** Developed a comprehensive training program for all employees with database access. The curriculum focuses on data protection best practices to prevent accidental deletion or unauthorized disclosure of critical data.

## Summary

This assessment demonstrates the transition from theoretical risk to practical hardening. By layering firewall rules, strong authentication, and human-centric training, the organization significantly improved its resilience against both external attackers and internal errors. The result is a secure environment where PII/SPII is protected according to industry standards.
