# Project 16: Secure NAS Migration & Legacy Hardware Repurposing

**Domain:** Network Security / System Administration / Disaster Recovery
**Tools:** Linux (Ubuntu/Debian), Samba (SMB), `rsync`, `hdparm`, Cron, Windows PowerShell

## 🛡️ Executive Summary

To optimize the development environment for a proprietary cybersecurity scanning engine, storage input/output (I/O) operations were migrated from a primary development workstation (Alienware) to a repurposed legacy laptop (HP 15-ba077cl).

This project transformed the legacy hardware into a hardened Network Attached Storage (NAS) appliance. The architecture enforces "Least Privilege" access, eliminates lateral movement vectors on the primary workstation, and implements a military-grade "Logical Air-Gap" backup strategy to protect against ransomware.

## 🎯 Objectives

- **Hardware Repurposing:** Extend the lifecycle of legacy hardware (AMD CPU, 8GB RAM) by converting it into a single-purpose storage appliance.
- **Secure Interoperability:** Establish an authenticated, encrypted SMB tunnel between a Linux Server and a Windows Client.
- **Attack Surface Reduction:** Decommission file sharing services on the development workstation.
- **Ransomware Resilience:** Implement an automated, offline-by-default backup system with physical power state management.

## 🛠️ Architecture & Configuration

### 1. Identity & Access Management (IAM)

A dedicated service account was created on the Linux host to decouple file access from the `root` user.

```bash
# Creation of the dedicated Samba user
sudo useradd -M -s /usr/sbin/nologin smbuser
sudo smbpasswd -a smbuser

```

### 2. File System Hardening

The directory structure utilizes the `setgid` bit to prevent permission drift.

- **Path:** `/srv/samba/LANShare`
- **Permissions:** `2770` (rwxrws---)
- **User/Group:** Full Control
- **Others:** No Access
- **SetGID:** New files automatically inherit the secure group ownership.

### 3. Samba Configuration (`smb.conf`)

The share definitions explicitly reject guest connections and enforce strict user masking.

```ini
[LANShare]
   path = /srv/samba/LANShare
   guest ok = no
   valid users = @smbgroup
   force group = smbgroup
   create mask = 0660
   directory mask = 2770

```

## 🔍 Implementation & Troubleshooting

### Phase 1: The Migration & "False Positive" Incident

During the verification phase, Windows File Explorer flagged an error: `Z:\.directory: Access is denied`.

**Forensic Analysis:**

- **Observation:** The root of the share was writable, but a specific hidden file threw an error.
- **Root Cause:** The `.directory` file was a root-owned artifact from the Linux desktop environment.
- **Resolution:** Identified as a **False Positive**. The error confirmed that the security controls were functioning correctly by preventing the lower-privileged SMB user from modifying system-level files.

### Phase 2: Attack Surface Reduction (Legacy Host)

Following the migration, the SMB service on the original host (Alienware) was terminated to prevent "Zombie Share" vulnerabilities.

- **Action:** Executed `Remove-SmbShare` via administrative PowerShell on the legacy host.
- **Verification:** Audited active shares using `net share` to confirm only default administrative resources (`C$`, `IPC$`) remained.
- **Result:** Eliminated the lateral movement vector on the primary development workstation.

### Phase 3: Automated Logical Air-Gap & Power Management

To mitigate ransomware risks, a "Mount-on-Demand" protocol was engineered. The backup drive remains physically connected but logically unmounted (invisible to the OS) and powered down 99% of the time.

- **Tool:** `rsync` + `hdparm`
- **Mechanism:**

1. **Wake Up:** Script identifies drive by UUID, mounts it, and spins up the platters.
2. **Sync:** `rsync` mirrors the data using differential copying.
3. **Vanish:** Drive is unmounted immediately after transfer.
4. **Kill:** `hdparm -Y` issues an ATA Sleep command, physically stopping the spindle.

**The Resilience Script (`auto_backup.sh`):**

```bash
# Core Logic Snippet
mount -U "$DRIVE_UUID" "$MOUNT_POINT"
rsync -av --delete "$SOURCE_DIR" "$MOUNT_POINT/LANShare_Mirror/"
umount "$MOUNT_POINT"
hdparm -Y "$RAW_DISK" # Puts drive into deep sleep

```

### Phase 4: Orchestration (Cron)

The protocol is automated via the system scheduler to run daily at 03:00 AM.

```bash
# Root Crontab Entry
0 3 * * * /usr/local/bin/auto_backup.sh

```

## Executive Conclusion

This project successfully transitioned the organization's storage architecture from a workstation-dependent model to a centralized, hardened infrastructure.

By implementing a **Logical Air-Gap strategy**, the system provides enterprise-grade resilience. The backup media exists in a disconnected, powered-down state when not in use, effectively eliminating the attack surface for automated cryptolockers while maintaining full automation.

- **Confidentiality:** Enforced via Linux IAM and Samba masking.
- **Integrity:** Preserved via `rsync` archive mode.
- **Availability:** Guaranteed via redundant, cold-storage backup.
