# Dynamic Firewall Provisioning & Network Access Control

**Organization:** Aspida Security
**Project Scope:** Host-Based Firewall Configuration, Traffic Filtering, Threat Mitigation, and Remote Access Governance

---

## Executive Summary

Strategic implementation of host-based network security using the Linux `iptables` utility. The primary objective was to securely expose a production web server to the public internet while simultaneously mitigating known threat actors and restricting administrative access to a dedicated internal subnet.

By applying the principle of least privilege at the network layer, the environment was hardened against unauthorized access - accepting legitimate HTTP/HTTPS traffic, silently dropping connections from blacklisted malicious IP addresses, and locking down SSH administration to a tightly controlled IP range.

---

## Technical Glossary: `iptables` Flag Breakdown

| Flag | Meaning |
| ---- | ------- |
| `-A INPUT` (Append) | Adds the new rule to the bottom of the `INPUT` chain (incoming traffic destined for the local system) |
| `-D INPUT` (Delete) | Removes a specific, pre-existing rule from the `INPUT` chain |
| `-p tcp` (Protocol) | Explicitly targets the TCP protocol for the rule |
| `--dport` (Destination Port) | Specifies the exact port the incoming traffic is attempting to reach (e.g., 80, 443, 22) |
| `-s` (Source) | Identifies the origin IP address or subnet (CIDR notation) of the incoming packet |
| `-j ACCEPT` / `-j DROP` (Jump Target) | Dictates the action on a match; `ACCEPT` allows traffic through, `DROP` silently discards the packet without a rejection notice, masking the server's presence |

---

## Phase 1: Web Service Exposition

**Objective:** Open the necessary network ports to allow global ingress to the web server's core HTTP and HTTPS services.

```bash
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j ACCEPT
```

**Result:** The firewall dynamically updated to permit incoming connections requesting web assets via ports 80 and 443 from any origin.

## Phase 2: Threat Mitigation & IP Blacklisting

**Objective:** Block hostile actors from interacting with any services on the web server by implementing strict source-IP DROP rules.

```bash
iptables -A INPUT -s 209.6.7.80 -j DROP
iptables -A INPUT -s 188.5.6.70 -j DROP
iptables -A INPUT -s 192.168.10.26 -j DROP   # internal verification test
```

**Verification (the blackhole test):** An administrative SSH connection was attempted from the blacklisted internal testing machine. As designed, the SSH client hung indefinitely and timed out - because a `DROP` rule (unlike `REJECT`) sends no response packet, the attacking machine cannot easily determine whether the server is offline or actively blocking it.

## Phase 3: Secure Remote Administration (Least Privilege)

**Objective:** Restore internal network functionality and lock down SSH administrative access so it is only reachable from a dedicated, secure internal subnet.

```bash
# Remove the temporary testing DROP rule
iptables -D INPUT -s 192.168.10.26 -j DROP

# Explicitly ACCEPT traffic from the internal testing machine
iptables -A INPUT -s 192.168.10.26 -j ACCEPT

# Lock down all SSH access to the authorized administrative subnet
iptables -A INPUT -p tcp -s 10.10.15.0/24 --dport 22 -j ACCEPT
```

**Result:** The web server is publicly accessible for HTTP/HTTPS traffic, invisible to known malicious threat actors, and securely segmented for administrative SSH access.

---

## Concepts Covered

- Host-based firewall rule ordering and chain evaluation (`INPUT` chain, append vs. delete)
- IP blacklisting via `DROP` vs. `REJECT` - traffic masking as a defensive technique
- Principle of least privilege applied at the network layer (subnet-scoped SSH access)
- Verification-first firewall testing - proving a rule works before trusting it in production

---

## Tech Stack

`Linux` `iptables` `Network Access Control` `Least Privilege Network Design`
