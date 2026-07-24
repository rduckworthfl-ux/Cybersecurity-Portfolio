# Incident Handler's Journal

## Entry Template Reference

| Field                 | Purpose                                            |
| --------------------- | -------------------------------------------------- |
| **Date**              | When the incident/investigation occurred           |
| **Entry**             | Sequential entry number                            |
| **Description**       | Brief summary of the incident or investigation     |
| **Tool(s) used**      | Cybersecurity/investigative tools employed         |
| **The 5 W's**         | Who, What, When, Where, Why analysis               |
| **Additional notes**  | Findings, recommendations, questions for follow-up |
| **Reflections/Notes** | Personal observations and learning points          |

---

## Entry 1: Healthcare Clinic Ransomware Incident

**Date:** 06/27/2025  
**Entry:** 1

### Description

A small U.S. healthcare clinic experienced a critical ransomware security incident that severely disrupted business operations.

### Tool(s) used

- Event log analysis
- Incident timeline reconstruction
- Network forensics (implied)

### The 5 W's

- **Who caused the incident?** An organized group of unethical hackers (Advanced Persistent Threat actor)
- **What happened?** Ransomware deployment and data encryption on critical systems
- **When did the incident occur?** Tuesday at 9:00 A.M.
- **Where did the incident happen?** At a small U.S. healthcare clinic
- **Why did the incident happen?** Attackers gained unauthorized access through phishing attack, deployed ransomware, encrypted sensitive files, and demanded payment for decryption key. Financial motivation evident.

### Attack Chain Analysis

1. **Initial Access:** Phishing email (unknown vector)
2. **Credential Compromise:** User fell for phishing, provided credentials
3. **Network Reconnaissance:** Attackers mapped network and identified critical systems
4. **Lateral Movement:** Expanded access across hospital systems
5. **Deployment:** Ransomware distributed to encrypt files
6. **Extortion:** Ransom demand issued with decryption key held hostage

### Remediation Recommendations

1. **Email Security:** Implement IP allowlisting on email server
2. **User Training:** Conduct phishing awareness training
3. **Network Segmentation:** Isolate critical healthcare systems
4. **Backup Strategy:** Implement 3-2-1 backup protocol
5. **Incident Response Plan:** Develop formal IR procedures
6. **Access Controls:** Implement MFA and principle of least privilege

### Additional Notes

- **Unanswered Questions:**
  1. How else can the healthcare clinic improve their security posture?
  2. Should the clinic pay the ransom? (Answer: NO - enables criminals, no guarantee decryption)
  3. Will these attackers become an APT? (Answer: Potentially - persistence is their business model)
- **Key Lessons:**
  - Healthcare is high-value target (patient data valuable)
  - Phishing remains most effective attack vector
  - Backups are critical defense against ransomware
  - Incident response time is critical (minimize dwell time)

### Reflections/Notes

This incident highlights the critical need for robust cybersecurity in healthcare. The financial motivation of organized attackers makes them particularly dangerous. Recommend implementing defense-in-depth strategy with emphasis on email security, user training, and backup redundancy.

---

## Entry 2: E-commerce Data Exfiltration via Forced Browsing

**Date:** 7/24/2025  
**Entry:** 2

### Description

Malicious actor exploited vulnerability in e-commerce website's purchase confirmation page to exfiltrate sensitive customer data through forced browsing attack.

### Tool(s) used

- Web application testing tools
- URL parameter analysis
- Data flow analysis
- Packet analysis (likely)

### The 5 W's

- **Who caused the incident?** Individual malicious actor (opportunistic)
- **What happened?** Data exfiltration via forced browsing (URL parameter manipulation)
- **When did the incident occur?** December 28, 2022 at 7:20 p.m., PT
- **Where did the incident happen?** On the organization's e-commerce website purchase confirmation page
- **Why did the incident happen?** Attacker exploited insecure direct object reference (IDOR) vulnerability in purchase confirmation URL to modify order numbers and access other customers' purchase data

### Vulnerability Details

**Attack Vector:**

```

Original URL: www.ecommerce.com/order?order_id=12345
Attacker URL: www.ecommerce.com/order?order_id=12346
www.ecommerce.com/order?order_id=12347
... (sequential enumeration)

```

**Impact:**

- Thousands of purchase confirmation pages accessed
- Customer personal information exposed
- Payment information potentially visible
- Delivery addresses compromised
- Privacy violation

**Severity:** CRITICAL (Confidentiality breach, PII exposure)

### Root Cause Analysis

1. **Missing Authentication:** No verification user owns order
2. **Predictable Identifiers:** Sequential order IDs enable enumeration
3. **Insufficient Authorization:** No access control checks
4. **Lack of Validation:** Server trusts user-supplied parameters

### Remediation Recommendations

1. **Authentication & Authorization:**
   - Verify user is authenticated before displaying order data
   - Verify user owns the requested order
   - Implement session validation on every request

2. **Input Validation:**
   - Randomize order IDs (UUID instead of sequential)
   - Implement GUID/UUID for order identification
   - Validate all user inputs server-side

3. **Access Control:**
   - Implement access control list (ACL) per user
   - Use allowlisting: only allow authenticated users to access their own orders
   - Deny all other access attempts

4. **Security Testing:**
   - Perform routine vulnerability scans (OWASP ZAP, Burp Suite)
   - Conduct regular penetration testing
   - Implement DAST (Dynamic Application Security Testing)

5. **Monitoring:**
   - Log all order access attempts
   - Alert on multiple failed access attempts
   - Monitor for sequential parameter guessing

### Additional Notes

**OWASP Top 10 Classification:**

- A01:2021 – Broken Access Control (most dangerous)
- A02:2021 – Cryptographic Failures (if payment data exposed)
- A04:2021 – Insecure Design

**Similar Vulnerabilities:**

- IDOR (Insecure Direct Object Reference)
- Parameter Tampering
- Privilege Escalation
- Horizontal Access Control Bypass

### Reflections/Notes

This is a common yet critical vulnerability class. Many developers overlook authentication/authorization checks, assuming that if users can see a URL, they should be able to access it. The sequential order ID pattern is a security anti-pattern. This incident emphasizes the importance of secure-by-design principles in web application development.

---

## Entry 3: Splunk Cloud Log Analysis & Investigation

**Date:** 7/30/2025  
**Entry:** 3

### Description

Practical exercise using Splunk Cloud to perform security investigation, focusing on threat detection and log analysis for unauthorized access attempts.

### Tool(s) used

- **Splunk Cloud** (SIEM platform)
- Splunk Query Language (SPL)
- Dashboard creation
- Alert configuration

### The 5 W's (Investigation Scope)

- **Who:** Identify failed authentication attempts (target: root account)
- **What:** Locate SSH authentication failures in indexed logs
- **When:** Timeframe: All indexed log data
- **Where:** Search across all data sources for authentication logs
- **Why:** Identify attack patterns and unauthorized access attempts

### Investigation Procedures

**Step 1: Upload Sample Log Data**

- Imported security log files into Splunk
- Configured log parsing and field extraction
- Verified data ingestion and indexing

**Step 2: Search Through Indexed Data**

- Built SPL queries to search indexed data
- Used wildcards and field matching
- Filtered by data source and time range

**Step 3: Evaluate Search Results**

- Analyzed query output for patterns
- Identified anomalies in authentication logs
- Correlated multiple events

**Step 4: Identify Different Data Sources**

- Categorized logs by source (syslog, Windows Event Log, etc.)
- Mapped data sources to security events
- Built multi-source correlation searches

**Step 5: Locate Failed SSH Login Attempts (Root Account)**

```

SPL Query (Example):
index=main sourcetype=syslog source=/var/log/auth.log user=root action=failed
| stats count by src_ip, src_user
| where count > 5

```

**Key Findings:**

- Identified failed SSH attempts for root account
- Located source IP addresses of attacks
- Tracked authentication attempt frequency
- Discovered brute force patterns

### Tools & Techniques

**Splunk Features Used:**

- Search and Reporting
- Field Extraction
- Statistical Analysis
- Alert Creation
- Dashboard Building

**Security Analysis Methods:**

- Pattern Recognition
- Statistical Anomaly Detection
- Timeline Analysis
- Correlation Search

### Recommendations

1. **Access Control:**
   - Disable root SSH login
   - Implement key-based authentication
   - Use jump hosts/bastion servers

2. **Monitoring:**
   - Set alerts for multiple failed login attempts
   - Configure alerts for successful root logins
   - Monitor from unusual locations/times

3. **Detection Rules:**
   - Alert on >3 failed SSH attempts in 5 minutes
   - Alert on successful login after multiple failures
   - Alert on root account activity after-hours

### Additional Notes

**Splunk Best Practices:**

- Normalize field names across data sources
- Create reusable saved searches
- Build dashboards for operational visibility
- Configure timely alerts for security events

**Lessons Learned:**

- Splunk is powerful for multi-source log analysis
- Query optimization is critical for performance
- Statistical analysis reveals patterns humans might miss
- Real-time alerting requires proper threshold tuning

### Reflections/Notes

This exercise demonstrated the power of SIEM platforms in threat detection. Splunk's ability to correlate events across multiple data sources provides deep visibility into security posture. The key challenge is proper alert tuning to avoid alert fatigue while maintaining detection sensitivity.

---

## Entry 4: Suricata IDS Configuration & Alert Testing

**Date:** 7/30/2025  
**Entry:** 4

### Description

Configured Suricata Intrusion Detection System, created custom detection rules, monitored network traffic in packet capture file, and analyzed alert outputs.

### Tool(s) used

- **Suricata** (Network IDS/IPS)
- Custom Rule Engine
- fast.log (alert log)
- eve.json (structured alerting)
- Packet capture files (.pcap)

### The 5 W's (Investigation Scope)

- **Who:** Suricata engine, analyzing network traffic
- **What:** Create rules, detect patterns, generate alerts
- **When:** Real-time monitoring of captured traffic
- **Where:** Analysis of packet capture file containing network flow
- **Why:** Identify malicious traffic patterns, protocol anomalies, attack signatures

### Procedures

**Step 1: Create Custom Rules**

```


# Example Suricata Rule Syntax

alert http \$HOME_NET any -> \$EXTERNAL_NET any (
msg:"Suspicious SQL Injection Attempt";
flow:established,to_server;
content:"union"; http_uri;
content:"select"; http_uri;
distance:0;
sid:1000001;
rev:1;
)

```

**Rule Components:**

- **Rule header:** Action, protocols, CIDR ranges
- **Rule body:** Content matching, flow analysis, metadata
- **Threshold:** Alert once per connection, per time period
- **SID:** Unique rule identifier

**Step 2: Run Rules on Packet Capture**

- Loaded .pcap file into Suricata
- Executed rule engine against captured traffic
- Generated alert outputs in multiple formats

**Step 3: Monitor Captured Traffic**

- Analyzed HTTP/HTTPS traffic patterns
- Examined DNS queries and responses
- Reviewed suspicious connection attempts

**Step 4: Examine Alert Output Formats**

**fast.log Format (High-Speed Alert Log):**

```

01/30/2025-14:23:45.123456 [**] [1:2013632:8] ET MALWARE Win32/Dridex.gen!C Checkin [**] [Classification: Probable Trojan Infection] [Priority: 1] {TCP} 192.168.1.100:54321 -> 203.0.113.44:443

```

**eve.json Format (Structured JSON Alerting):**

```

{
"timestamp": "2025-01-30T14:23:45.123456+0000",
"flow_id": 123456789,
"event_type": "alert",
"src_ip": "192.168.1.100",
"src_port": 54321,
"dest_ip": "203.0.113.44",
"dest_port": 443,
"proto": "TCP",
"alert": {
"action": "allowed",
"gid": 1,
"signature_id": 2013632,
"signature": "ET MALWARE Win32/Dridex.gen!C Checkin",
"category": "Probable Trojan Infection",
"severity": 1
}
}

```

### Analysis Findings

**Detection Capabilities:**

- Protocol anomaly detection
- Content-based pattern matching
- Exploit signature detection
- Botnet C&C communication identification

**Rule Tuning:**

- Balanced sensitivity vs. false positives
- Prioritized high-confidence detections
- Created custom rules for environment-specific threats

### Recommendations

1. **Rule Management:**
   - Subscribe to ET (Emerging Threats) threat feeds
   - Regularly update rule sets
   - Create organization-specific custom rules

2. **Alert Response:**
   - Establish alert review process
   - Prioritize alerts by severity
   - Correlate Suricata alerts with log data

3. **Performance Optimization:**
   - Load balance traffic across multiple sensors
   - Optimize rule execution order
   - Monitor CPU/memory usage

### Additional Notes

**Suricata Advantages Over Snort:**

- Multi-threaded for better performance
- Native Lua scripting support
- Improved JSON output format
- Active development community

**Alert Correlation:**

- Combine Suricata alerts with Splunk logs
- Create dashboards showing network threats
- Use alerts to trigger automated response

### Reflections/Notes

Suricata demonstrates the power of signature-based detection for known threats. The eve.json output format is superior to fast.log for SIEM integration. Real-world implementation requires careful rule tuning to maintain high detection rate while minimizing false positives.

---

## Entry 5: Wireshark Packet Capture Analysis

**Date:** 7/30/2025  
**Entry:** 5

### Description

Opened and analyzed network packet capture file using Wireshark, examined packet-level details, applied display filters to isolate specific traffic patterns.

### Tool(s) used

- **Wireshark** (Network Protocol Analyzer)
- tcpdump (implied for capture generation)
- Display filters
- Packet inspection tools
- Statistics and analysis features

### The 5 W's (Investigation Scope)

- **Who:** Packet analysis engineer, investigating network traffic
- **What:** Open PCAP file, examine protocols, apply filters
- **When:** Historical traffic analysis (replay of captured packets)
- **Where:** Network communication between hosts (source/dest IP/port)
- **Why:** Understand traffic patterns, identify anomalies, detect malicious communication

### Procedures

**Step 1: Open Packet Capture File in Wireshark**

- Launched Wireshark application
- Opened .pcap file containing network traffic
- Verified packet loading and indexing
- Reviewed packet count and capture duration

**Step 2: Examine Packet Information**

**Packet Anatomy (OSI Layers):**

```

Layer 2 (Data Link): Ethernet header

- Source MAC, Destination MAC, EtherType

Layer 3 (Network): IP header

- Source IP, Destination IP, TTL, Protocol, Flags

Layer 4 (Transport): TCP/UDP header

- Source Port, Destination Port, Flags, Sequence Number, Acknowledgment

Layer 7 (Application): Payload

- HTTP headers, DNS queries, TLS handshake, etc.

```

**Key Fields Examined:**

- Protocol identification
- Source/destination IP addresses and ports
- Packet size and timing
- TCP flags and sequence numbers
- Payload content (when unencrypted)

**Step 3: Apply Display Filters**

**Filter Examples:**

```


# Filter by protocol

ip.proto == 6          \# TCP only
ip.proto == 17         \# UDP only
http                   \# HTTP traffic

# Filter by IP address

ip.src == 192.168.1.1
ip.dst == 203.0.113.44

# Filter by port

tcp.port == 443        \# HTTPS
tcp.dstport == 22      \# SSH

# Filter by direction

tcp.flags.syn == 1 \&\& tcp.flags.ack == 0  \# SYN packets (connection initiation)

# Combination filters

(http.request.method == "POST") \&\& (http.host == "suspicious.com")

```

**Complex Filtering:**

```


# Find all DNS queries for specific domain

dns.qry.name contains "attacker.com"

# Find failed TCP connections

tcp.flags.rst == 1     \# RST flag (connection reset)

# Find potential reconnaissance

tcp.flags.syn == 1     \# SYN packets

# Find large data transfers

frame.len > 10000

```

### Traffic Analysis Findings

**Network Communication Patterns:**

1. **HTTP/HTTPS Traffic:** Encrypted vs. plaintext analysis
2. **DNS Queries:** Domain resolution patterns
3. **TCP Handshakes:** Connection establishment sequences
4. **Network Anomalies:** Unusual ports, protocols, packet sizes

**Security Observations:**

- Identified SSL/TLS certificate information
- Observed HTTP headers and methods
- Detected potential data exfiltration patterns
- Analyzed network timing and retransmissions

### Analysis Techniques

**Packet Analysis Methods:**

1. **Follow TCP Stream:** Reassemble application-layer data
2. **Protocol Hierarchy:** Understand protocol nesting
3. **Statistics:** Analyze traffic volume by protocol/IP
4. **Endpoint Conversation:** Identify communication pairs

**Indicators of Compromise (IOCs) Detection:**

- Unusual port combinations
- Excessive connection attempts
- Large data transfers to external IPs
- Known malicious domains/IPs

### Recommendations

1. **Traffic Monitoring:**
   - Establish baseline traffic patterns
   - Alert on deviations from baseline
   - Monitor for known malicious IPs/domains

2. **Network Segmentation:**
   - Isolate sensitive systems
   - Restrict outbound traffic
   - Implement DMZ for public-facing services

3. **Packet Retention:**
   - Implement packet capture for forensics
   - Store PCAP files for incident investigation
   - Establish retention policy per compliance requirements

### Additional Notes

**Limitations of Packet Analysis:**

- Encrypted traffic (TLS/SSL) prevents payload inspection
- High packet volume requires sampling strategies
- Real-time analysis requires powerful hardware

**Complementary Tools:**

- tshark (Wireshark CLI)
- tcpdump (packet capture utility)
- zeek (network analysis framework)
- suricata (IDS with flow analysis)

### Reflections/Notes

Packet analysis is fundamental to network security investigation. Wireshark's intuitive interface and powerful filtering capabilities make it essential for any security professional. The ability to understand traffic at the packet level provides deep insight into network communication and enables detection of sophisticated attacks.

---

## Entry 6: Port Reservation Forensic Investigation (Nov 5, 2025)

**Date:** 11/05/2025  
**Entry:** 6

### Description

Security incident investigation into unexpected port reservation that blocked Supabase database service. Through systematic forensic analysis, determined root cause to be Docker/WSL2 restart during Hyper-V network reinitialization. No compromise detected.

### Tool(s) used

- **Event Viewer** (Windows System & Security logs)
- **PowerShell 7-x64** (Get-WinEvent, Get-Process, Get-WmiObject)
- **netstat** (Network port monitoring)
- **netsh** (Windows network shell configuration)
- **Process Timeline Analysis** (Event correlation)
- **Forensic Timeline Construction**

### The 5 W's

- **Who caused the incident?** No malicious actor. System-level automatic process (Docker/WSL2 restart → Hyper-V port allocation)
- **What happened?** Windows automatically reserved port range 54252-54351 for Hyper-V/WinNAT during Docker Desktop restart. Supabase database port 54322 fell within reserved range and became inaccessible.
- **When did the incident occur?** Discovery: November 5, 2025 at 1:58 PM CST. Actual trigger: November 5, 2025 at 1:37 PM CST (Docker/WSL2 restart)
- **Where did the incident happen?** Local Windows development system (BDFS1), Hyper-V virtualization layer, WinNAT service
- **Why did the incident occur?** Docker Desktop and WSL2 services restarted (cause unclear: possibly Windows update, Docker auto-update, or manual restart). Full Hyper-V network stack re-negotiation triggered automatic port range reservation for container networking.

### Incident Timeline

| Time                    | Event                        | Source           | Significance                 |
| ----------------------- | ---------------------------- | ---------------- | ---------------------------- |
| 11/4 4:29 PM            | NIC disconnected             | Event Log        | Baseline - previous shutdown |
| 11/5 12:26 AM           | Port deleted, NIC cleanup    | Event Log        | System state change          |
| **11/5 1:37:15 PM**     | **Docker restart**           | Process Timeline | **TRIGGER EVENT**            |
| 11/5 1:37:35 PM         | com.docker.backend (2x)      | Process Timeline | Hyper-V layer init           |
| 11/5 1:37:38 PM         | com.docker.build             | Process Timeline | Docker build service         |
| 11/5 1:37:39 PM         | Docker Desktop.exe (4x)      | Process Timeline | Frontend initialization      |
| 11/5 1:37:17-1:38:17 PM | WSL services (20+ instances) | Process Timeline | Network stack restart        |
| 11/5 1:41:07 PM         | VMICTimeProvider warnings    | Event Log        | Hyper-V recovery phase       |
| 11/5 1:58 PM            | Port access fails            | User Report      | Issue discovery              |
| 11/5 2:04 PM            | Diagnostic commands run      | Process Timeline | Investigation begins         |

### Forensic Analysis & Findings

**Event Log Analysis:**

```

System Log Query (200 most recent events):
VMICTimeProvider entries - Normal Hyper-V time sync
Networking driver loads - Normal initialization
NIC/Port status messages - Expected during restart
NO suspicious admin modifications
NO unauthorized port exclusion commands
NO privilege escalation events
NO failed authentication attempts

```

**Process Timeline Analysis:**

```

Docker Services (Started 1:37 PM):

- com.docker.backend.exe (2 instances, 1:37:35 PM)
- com.docker.build.exe (1 instance, 1:37:38 PM)
- Docker Desktop.exe (4 instances, 1:37:39 PM)

WSL2 Services (Started 1:37-1:38 PM):

- wsl.exe (9 instances)
- wslhost.exe (10 instances)
- wslrelay.exe (1 instance)
- vmmemWSL (memory manager)

Assessment: EXPECTED RESTART CASCADE

```

**Port Analysis:**

```

Port Status Check:
netstat -ano | findstr :54322
Result: (empty - no listening process)

Windows Port Exclusions:
netsh interface ipv4 show excludedportrange protocol=tcp
Result: 54252-54351 reserved by Windows/Hyper-V

Conclusion: Port pre-allocated by OS, not actively used

```

**Software Installation Review:**

```

Recent Installations (Last 30 Days):

- Office 16 Click-to-Run
- PowerShell 7-x64
- Microsoft GameInput
- Duplicati (backup software - benign)

Assessment: NO SUSPICIOUS SOFTWARE DETECTED

```

### Root Cause Analysis

**Cause Chain:**

1. **Trigger:** Docker Desktop & WSL2 restarted (~1:37 PM)
   - Source: Unknown (Windows Update, Docker Update, or manual restart)
2. **Docker Initialization:** Full Hyper-V service restart
   - Multiple Docker backend processes started
   - Virtual network stack re-negotiation initiated
3. **Hyper-V Port Allocation:** Windows assigned port range for WinNAT
   - Automatic behavior during Hyper-V service startup
   - Port range 54252-54351 reserved for container networking
4. **Port Collision:** Supabase ports fell into reserved range
   - Port 54321 (API) - Outside range, still accessible
   - Port 54322 (Database) - IN RANGE, blocked
   - Port 54323 (Studio) - IN RANGE, blocked
5. **Access Denial:** Windows firewall enforced restrictions
   - Attempted access returned "permission denied"
   - System prompted to adjust firewall rules
   - Behavior is correct, not a vulnerability

### Security Assessment

| Finding                    | Status           | Confidence |
| -------------------------- | ---------------- | ---------- |
| **Malware present**        | None detected    | 99%        |
| **Unauthorized access**    | None found       | 98%        |
| **System compromise**      | Not compromised  | 99%        |
| **Active threat**          | No active threat | 99%        |
| **Zero-day vulnerability** | Not a zero-day   | 99%        |
| **Expected OS behavior**   | Confirmed        | 98%        |

**Verdict:** System is CLEAN. No security incident. Expected OS behavior during service restart.

### Remediation & Resolution

**Immediate Fix Applied:**

```


# supabase/config.toml (changed ports to safe range)

[api]
port = 63321  \# Outside Hyper-V pre-allocation ranges

[db]
port = 63322

[studio]
port = 63323

```

**Application Configuration Updated:**

```

// src/lib/supabase.js
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'http://127.0.0.1:63321'

```

```


# .env.local

VITE_SUPABASE_URL=http://127.0.0.1:63321

```

**Service Restart:**

```

supabase stop
supabase start
npm run dev

```

**Result:** Service operational without conflicts

### Preventive Measures Implemented

1. **Port Selection Policy:**
   - Avoid ports 49152-65535 (dynamic/ephemeral)
   - Avoid known Hyper-V ranges (54252-54351)
   - Use conventional ranges: 3000-3999, 8000-8999, 9000-9999

2. **Documentation:**
   - Recorded port allocations in `.env` configuration
   - Documented rationale for port selection
   - Updated runbooks with new port information

3. **Monitoring:**
   - Monitor Docker Desktop restart events
   - Track Hyper-V service state changes
   - Alert on unexpected port reservation modifications

### CVSS Scoring (If This Were a Vulnerability)

```

Attack Vector: Local (AV:L)
Attack Complexity: High (AC:H)
Privileges Required: High (PR:H)
User Interaction: Required (UI:R)
Scope: Unchanged (S:U)
Confidentiality Impact: None (C:N)
Integrity Impact: None (I:N)
Availability Impact: Low (A:L)

CVSS v3.1 Base Score: 1.5 (Lowest Severity)

Conclusion: Not eligible for CVE submission

```

### Incident Response Lessons Learned

**What Went Right:**
Proactive detection and reporting  
Systematic forensic investigation  
Multiple diagnostic approaches  
Evidence collection and preservation  
Root cause definitively identified  
Appropriate security consciousness

**Areas for Improvement:**
Windows could provide better port allocation transparency  
Error messages could explain port reservation cause  
Hyper-V documentation could be more developer-friendly  
Could automate port availability checks in startup scripts

### Additional Notes

**Key Insights:**

- Port conflicts are common in development environments
- Windows port allocation is documented but not well-publicized
- Forensic investigation requires multiple data sources
- Event correlation is essential for root cause analysis

**Recommended Further Study:**

- Microsoft Windows Kernel port allocation mechanisms
- Hyper-V networking architecture
- Docker Desktop for Windows internals
- WSL2 network bridge implementation

**Security Awareness Takeaway:**
Not all unexplained system behavior indicates a compromise. Systematic investigation and evidence analysis are essential before concluding malicious activity.

### Reflections/Notes

This incident provided an excellent real-world opportunity to practice forensic investigation skills in a non-destructive environment. The methodology employed (timeline reconstruction, log analysis, process tracking, correlation) mirrors professional incident response procedures.

**Key Takeaways:**

1. **Methodical Investigation:** Breaking down complex problems into manageable components
2. **Evidence-Based Conclusion:** Using data rather than assumptions
3. **Security Consciousness:** Taking every anomaly seriously while applying appropriate skepticism
4. **Documentation:** Recording findings thoroughly for future reference

The incident demonstrates the importance of both **security vigilance** and **technical understanding** in distinguishing genuine threats from expected system behavior.

**Investigation Quality:** Professional-level forensic analysis  
**Outcome:** Accurate root cause identification  
**System Status:** Secure and operational

---

## Entry 7: Wazuh SIEM Full Disk Exhaustion — Dual Root Cause Availability Incident

**Date:** 04/06/2026  
**Entry:** 7

### Description

The Wazuh SIEM stack on `os1` crashed due to complete disk exhaustion, taking all three containers offline and creating a full monitoring blind spot. What appeared to be a straightforward "ran out of disk" problem revealed two separate root causes: the Ubuntu VM's LVM logical volume had never been extended to match the 80GB VMware disk allocation (leaving only ~39GB usable), and no ISM retention policy had been configured at deployment. The `wazuh_queue` Docker volume accumulated 24GB of unprocessed event data within ~48 hours, exhausting the undersized LV entirely. Resolution required a multi-phase investigation, several failed recovery attempts, LVM expansion using `pvresize`/`lvextend`/`resize2fs`, and a fresh Wazuh 4.8.0 deployment with an ISM 30-day deletion policy.

### Tool(s) used

- **docker-compose** (stack lifecycle)
- **docker system prune / docker volume inspect** (space recovery and volume analysis)
- **df / du** (disk usage at OS and directory level)
- **ncdu** (visual disk space explorer — identified /var as 27.4 GiB dominant consumer)
- **journalctl --vacuum-size** (systemd journal cleanup)
- **pvresize / lvextend / resize2fs** (LVM and filesystem expansion)
- **OpenSearch REST API** (`_cat/indices`, `_cat/allocation`)
- **OpenSearch Dashboard** (ISM retention policy creation)

### The 5 W's

- **Who caused the incident?** No external actor. Two independent operational/infrastructure misconfigurations: (1) LVM never extended after VM provisioning, (2) Wazuh deployed without an ISM retention policy.
- **What happened?** All three Wazuh containers (manager, indexer, dashboard) crashed when the root LVM volume hit 100% capacity. The primary disk consumer was the `single-node_wazuh_queue` Docker volume at 24GB — not the OpenSearch indices. The underlying volume was only ~39GB despite VMware provisioning 80GB.
- **When did the incident occur?** Discovered April 6, 2026 ~18:06 CDT. Disk exhaustion likely occurred within 48 hours of initial deployment (~April 4). The LVM under-allocation was present since initial VM setup.
- **Where did the incident happen?** Host `os1` (Ubuntu 22.04 LTS, Alienware), `/dev/mapper/ubuntu--vg-ubuntu--lv` — the root logical volume hosting all Docker data at `/var/lib/docker`.
- **Why did the incident happen?** VMware provisioned 80GB, but `lvextend` was never run after VM initialization — the LV stayed at its default ~39GB. With Wazuh deployed on that undersized volume and no ISM policy in place, the event queue filled the available space within 48 hours.

### Incident Timeline

| Time (CDT)     | Event                                                                                       |
| -------------- | ------------------------------------------------------------------------------------------- |
| ~04/04/2026    | Wazuh deployed — no ISM policy; LV unextended at ~39GB                                      |
| ~04/04–05/2026 | wazuh_queue accumulates 24GB of event data; indices grow unbounded                          |
| 04/06 ~18:06   | "No such container" error on docker exec — investigation begins                             |
| 04/06 ~18:06   | `df -h /` → **39G 38G 0 100%** — disk completely full                                       |
| 04/06 ~18:07   | `docker system prune` → 4.5GB reclaimed → 93% — still critical                              |
| 04/06 ~18:08   | journalctl vacuum (639MB) + apt-get clean — marginal gains only                             |
| 04/06 ~18:09   | Stopped Docker, deleted overlay2 (8.0K), restarted — no meaningful impact                   |
| 04/06 ~18:12   | Installed ncdu → **/var = 27.4 GiB** identified as dominant consumer                        |
| 04/06 ~18:14   | Docker volume enumeration → **single-node_wazuh_queue = 24G** confirmed as primary offender |
| 04/06 ~18:16   | docker-compose down; removed indexer-data volume (20M) → df STILL 100%                      |
| 04/06 ~18:18   | **Root cause discovered**: VMware disk 80GB, LVM LV only ~39GB — 41GB unallocated           |
| 04/06 ~18:19   | pvresize → lvextend → resize2fs → **77G 34G 40G 46%** — 40GB headroom restored              |
| 04/06 ~18:23   | docker-compose up -d → Wazuh 4.8.0 pulled and deployed; all 3 containers up                 |
| 04/06 ~18:31   | ISM policy `retention` (30d) created via OpenSearch Dashboard → incident closed             |

### Root Cause Analysis

**Root Cause 1 — VMware/LVM Disk Allocation Gap:**

- VMware provisioned the VM with an 80GB virtual disk
- Ubuntu LVM was initialized but `pvresize` + `lvextend` were never run post-provisioning
- The LV was stuck at the OS installer's default (~39GB) — less than half the available physical space
- This is an infrastructure gap that existed from day one and would have caused problems regardless of Wazuh

**Root Cause 2 — Missing ISM Retention Policy:**

- Wazuh does not ship with a default retention policy — it must be manually configured
- Without it, `wazuh_queue` and alert indices grow without bound
- The queue accumulated 24GB in ~48 hours, which alone was enough to exhaust the 39GB LV

**Combined effect:** A manageable configuration gap (missing ISM policy) became catastrophic because it was compounded by an infrastructure gap (undersized LV) that cut available storage in half.

### Diagnostic Evidence

```
# After docker system prune — still critical
df -h /: 39G  34G  2.9G  93%

# ncdu visualization — root cause location
/var = 27.4 GiB (full bar)

# Docker volume breakdown — offender confirmed
single-node_wazuh_queue:  24G   ← 62% of entire volume
single-node_wazuh_logs:   25M
single-node_wazuh_etc:    2.9M
(all others < 1M)

# After LVM expansion — breathing room
df -h /: 77G  34G  40G  46%

# ISM policy confirmed active
policy_id: "retention", min_index_age: "30d", seqNo: 0, primaryTerm: 1
```

### Security Assessment

| Finding                     | Status                                       |
| --------------------------- | -------------------------------------------- |
| Malicious actor             | None                                         |
| Data exfiltration           | None                                         |
| Integrity impact            | None                                         |
| Confidentiality impact      | None                                         |
| Availability impact         | **Yes — Full SIEM outage**                   |
| Detection gap during outage | **Yes — monitoring blind spot ~2+ days**     |
| CVSS v3.1                   | 4.4 MEDIUM (AV:L/AC:L/PR:H/UI:N/C:N/I:N/A:H) |

### Additional Notes

- **Unanswered question:** What caused the wazuh_queue to accumulate 24GB so quickly? The queue buffers events when the manager can't process them fast enough (or when the indexer is unavailable). This may indicate the event ingestion rate exceeds what the single-node Wazuh config can handle. Worth monitoring the queue volume size after the fresh deployment to see if it grows again.
- **Key lesson:** Always verify `lvdisplay` against VMware disk allocation after provisioning a VM. Two-minute check, prevents this entirely.
- **Second lesson:** ISM retention policy is not optional for Wazuh — it goes in the deployment runbook as step 1, not an afterthought.
- **Third lesson:** Docker system prune and journalctl vacuum are useful for small cleanups but are entirely inadequate when a 24GB volume is the offender. You need to know what's actually consuming space before you can fix it. ncdu saved hours here.

### Reflections/Notes

This one was genuinely educational, and not in the way I expected. I assumed the indexer was the problem — that's the obvious suspect when a Wazuh stack runs out of disk. Turns out it was the manager's event queue sitting at 24GB, and under that was an even more fundamental issue: the VM I thought had 77GB only had 39GB because I never ran `lvextend` after provisioning.

The investigation required layering tools in the right order — container logs, df, docker prune, journalctl vacuum, ncdu, docker volume inspection — before the actual culprit came into view. Each step ruled something out and pointed deeper. That's exactly what incident response looks like in practice: you rarely know the root cause at first contact, and every failed fix still tells you something useful.

The fact that removing the indexer-data volume (20MB) made zero visible difference on the df output was the moment that made everything click. Something else was holding 24 gigabytes — and that something was still there. Finding the queue, then finding the unallocated VMware disk space — that was the actual pivot point of this incident.

Both root causes are fixed. ISM policy is live. LV is extended to the full 80GB allocation. This won't happen again the same way.

---
