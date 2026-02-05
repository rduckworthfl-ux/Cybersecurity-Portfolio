# Project 17: Secure Linux Dev Infrastructure & System Hardening

## Project Overview

This project involved the engineering and deployment of a hardened, high-performance Linux development environment on repurposed hardware ("HP-Lab"). The objective was to build a secure foundation for the **Vappler** vulnerability management platform.

Key achievements included implementing a **ZRAM-based memory architecture** to overcome hardware limitations, engineering a **Samba Permission Airlock** to sanitize cross-platform file transfers, and enforcing a **Zero-Trust Network posture** using UFW.

## Objectives

- **Infrastructure Optimization:** maximize available RAM using compression algorithms (ZRAM).
- **Cross-Platform Integration:** Establish a secure, sanitized file bridge between Windows (Alienware) and Linux (HP-Lab).
- **Access Control:** Implement a "Default Deny" firewall policy, whitelisting only verified LAN assets.
- **Compliance:** Enable Ubuntu Pro/Livepatch for automated vulnerability management.

---

## Implementation Log

### Phase 1: Performance Engineering (ZRAM)

To support Docker containers on limited RAM, I implemented ZRAM (compressed swap in memory) rather than relying on slow disk-based swap.

**Commands Executed:**

```bash
# 1. Install ZRAM tools
sudo apt install zram-tools

# 2. Configure the swap size (Allocating 8GB compressed)
echo "ALGO=lz4" | sudo tee -a /etc/default/zramswap
echo "PERCENT=100" | sudo tee -a /etc/default/zramswap

# 3. Reload and Verify
sudo systemctl restart zramswap
zramctl
free -h
               total        used        free      shared  buff/cache   available
Mem:           7.2Gi       2.2Gi       313Mi        58Mi       4.7Gi       5.1Gi
Swap:          8.0Gi       256Ki       8.0Gi

```

**Outcome:** Confirmed 8GB of high-speed compressed swap available.

### Phase 2: The "Permission Airlock" (Samba Setup)

I configured a Network Attached Storage (NAS) entry point that automatically normalizes file permissions. This prevents "Permission Drift" where Windows ACLs corrupt Linux file ownership.

**Commands Executed:**

```bash
# 1. Install Samba
sudo apt install samba

# 2. Create the "Airlock" Directory
sudo mkdir -p /srv/samba/LANShare
sudo chown shareusersmb:shareusersmb /srv/samba/LANShare
sudo chmod 600 /srv/samba/LANShare
# 3. Configure the Airlock (smb.conf)
sudo nano /etc/samba/smb.conf

```

**Configuration Block (`smb.conf`):**

```ini
[LANShare]
    comment = Secure Dev Share
    path = /srv/samba/LANShare
    read only = no
    browsable = yes
    # The Airlock Mechanism:
    force user = shareusersmb
    create mask = 0660
    directory mask = 0770

```

**User Provisioning:**

```bash
# Create the dedicated service account
sudo useradd -M -s /sbin/nologin shareusersmb
sudo smbpasswd -a shareusersmb
sudo usermod -aG shareusersmb $USER  # Granting local admin access to the group

```

Because my local user was locked out, I could not use VS Code or Terminal on the HP laptop to edit those files without using sudo every time, which makes development painful.

To fix this, I added my local user to the "Trusted Circle" (the smbuser group). This gives me full access locally while maintaining the security structure.

```bash
sudo usermod -aG smbuser $USER
```

To promote accessibility of the drive, I added a folder to the drive to the Desktop of the OS. This allowed me to access the drive from the HP laptop without using sudo every time.

```bash
ln -s /srv/samba/LANShare ~/Desktop/LANShare
```

### Phase 3: Troubleshooting & Resolution

During deployment, connectivity between the Windows Client (Alienware) and Linux Server failed.

**Issue 1: "Extended Error" / Connection Refused**

- **Symptom:** Windows could ping the server but failed to mount the drive with specific error codes.
- **Root Cause:** The UFW Firewall was active but lacked rules for the Samba protocol (Ports 137, 138, 139, 445).
- **Resolution:** Implemented specific firewall allow rules.

**Issue 2: Windows Credential Caching**

- **Symptom:** Windows attempted to use old credentials from a previous project ("Project 16"), causing authentication failures even after the firewall was fixed.
- **Resolution:** Performed a client-side flush.

```cmd
# On Windows Client
net use * /delete /yes
klist purge
ipconfig /flushdnS

```

### Phase 4: Network Hardening (Firewall)

Moved from a testing state to a hardened "Default Deny" posture.

**Commands Executed:**

```bash
# 1. Reset to Factory State (Purge bad rules)
sudo ufw reset

# 2. Set Default Policies (The Shield)
sudo ufw default deny incoming
sudo ufw default allow outgoing

# 3. Whitelist Trusted LAN Assets (The "Need to Know" List)
# Admin Workstation & Trusted Nodes
sudo ufw allow from 192.168.XX.XXX to any app Samba
sudo ufw allow from 192.168.XX.XXX to any port 22 proto tcp
sudo ufw allow from 192.168.XX.XXX to any app Samba
sudo ufw allow from 192.168.XX.XXX to any port 22 proto tcp
sudo ufw allow from 192.168.XX.XXX to any app Samba
sudo ufw allow from 192.168.XX.XXX to any port 22 proto tcp

# 4. Enable Logging & Activation
sudo ufw logging on
[1] Logging enabled
sudo ufw enable
[1] Firewall is active and enabled on system startup

5. Restart pc and verify
sudo reboot
sudo ufw status numbered
[1] Status: active

To                         Action      From
     --                         ------      ----
[1] Samba                      ALLOW IN    192.168.XX.XXX
[2] 22/tcp                     ALLOW IN    192.168.XX.XXX
[3] Samba                      ALLOW IN    192.168.XX.XXX
[4] 22/tcp                     ALLOW IN    192.168.XX.XXX
[5] Samba                      ALLOW IN    192.168.XX.XXX
[6] 22/tcp                     ALLOW IN    192.168.XX.XXX
```

### Phase 5: Compliance (Ubuntu Pro)

Enabled Extended Security Maintenance (ESM) to ensure the development environment receives patches for 10 years.

**Commands Executed:**

```bash
sudo pro attach [REDACTED_TOKEN]
pro status

```

**Outcome:** Verified `esm-apps`, `esm-infra`, and `livepatch` services are active.

---

## Final Architecture

- **Hostname:** `hp-lab`
- **IP Assignment:** Static (Via Router Reservation)
- **Firewall:** Strict Allowlist (Dropping all other traffic)
- **Storage:** `/srv/samba/LANShare` (Mapped as Z: Drive on Windows)
