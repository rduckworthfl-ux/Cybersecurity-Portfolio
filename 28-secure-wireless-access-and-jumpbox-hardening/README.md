# Secure Network Infrastructure & Host Hardening

**Organization:** Aspida Security
**Project Scope:** Wireless Network Provisioning, Access Control, Host Hardening, and Centralized Auditing

---

## Executive Summary

End-to-end configuration and securing of a segmented network environment: deploying a secure wireless access point, establishing a hardened Linux jump box for administrative access, and implementing centralized log aggregation for security auditing.

By applying infrastructure hardening principles - transitioning from password-based to cryptographic key-based authentication, enforcing strict MAC-level network filtering, reducing the attack surface by purging unnecessary daemons, and deploying dynamic `rsyslog` templates - the environment was secured against common unauthorized access vectors and lateral movement attempts.

---

## Phase 1: Wireless Infrastructure Provisioning (OpenWRT)

**Objective:** Deploy and secure a wireless access point to control ingress to the administrative network.

- **System Identity:** Hostname set to `HexWireless01`.
- **Wireless Interface (`radio0`):** ESSID `HexeloWireless` configured as a hidden network to prevent passive discovery, with a strict MAC-address allow-list controlling which hardware could associate.
- **Network Interface:** Static IPv4 assigned (`192.168.10.1`) with a restricted DHCP scope (limit 42 leases, 8h lease time).
- **Infrastructure Backup:** Device configuration states were exported and version-controlled via PowerShell on a Windows Server 2022 VM.

## Phase 2: Secure Access Implementation (Key-Based Auth)

**Objective:** Deprecate password-based SSH authentication in favor of RSA public/private key pairs to facilitate secure, automated Infrastructure-as-Code connectivity.

Administrators were provisioned on both the local workstation and the remote jump box. Keys were generated on the workstation and securely transferred via `ssh-copy-id`:

```bash
ssh-keygen
ssh-copy-id admin@192.168.10.11
ssh admin@192.168.10.11
```

**Result:** Authentication succeeded automatically once the public key was appended to the jump box's `~/.ssh/authorized_keys`.

## Phase 3: Host Hardening & Attack Surface Reduction

**Objective:** Lock down the jump box by enforcing strict SSH policies, implementing legal warning banners, and purging unnecessary running services.

**SSH daemon hardening** (`/etc/ssh/sshd_config`):

```text
PermitRootLogin no           # Prevents network-based root brute-forcing
PubkeyAuthentication yes     # Enforces cryptographic key usage
PasswordAuthentication no    # Disables legacy password entry
Banner /etc/ssh/warning      # Maps to the legal warning banner
```

**Service purging:** The unneeded Apache web server was stopped, disabled from boot, and completely uninstalled to minimize the system's attack surface:

```bash
systemctl stop httpd
systemctl disable httpd
dnf -y remove httpd
systemctl daemon-reload
```

## Phase 4: Centralized Auditing (Log Aggregation)

**Objective:** Prevent local log tampering on the jump box by automatically forwarding all system logs to the administrative workstation for centralized archiving and analysis.

The jump box's `/etc/rsyslog.conf` streamed all facilities to the admin workstation over UDP (`*.* @192.168.10.12:514`). The receiving workstation was configured with a dynamic template routing incoming logs into structured, per-host directories:

```text
module(load="imudp")
input(type="imudp" port="514")

$template DynamicFile,"/var/log/%HOSTNAME%/forwarded-logs.log"
*.* -?DynamicFile
```

**Verification:** A test log injected on the jump box (`logger Test`) was successfully captured, dynamically routed into a dedicated per-host directory, and written to disk on the admin workstation - proving the centralized auditing pipeline fully operational end to end.

---

## Concepts Covered

- OpenWRT wireless configuration - hidden SSID, MAC filtering, restricted DHCP scoping
- SSH key-based authentication - `ssh-keygen`, `ssh-copy-id`, passwordless handshake validation
- SSH daemon hardening - disabling root login and password auth, legal warning banners
- Attack surface reduction - systematic service purging via `systemctl` and `dnf`
- Centralized log aggregation - `rsyslog` UDP forwarding with dynamic per-host templating
- Infrastructure backup and version control for network device configuration

---

## Tech Stack

`OpenWRT` `SSH (RSA Key-Based Auth)` `rsyslog` `Linux Host Hardening` `PowerShell` `Windows Server 2022`
