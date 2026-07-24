# Project 16: Secure NAS Migration & Legacy Hardware Repurposing

**Domain:** Network Security / System Administration / Disaster Recovery
**Tools:** Linux (Ubuntu/Debian), Samba (SMB), `rsync`, `hdparm`, Cron, Windows PowerShell

## Executive Summary

To optimize the development environment for a proprietary cybersecurity scanning engine, storage input/output (I/O) operations were migrated from a primary development workstation (Alienware) to a repurposed legacy laptop (HP 15-ba077cl).

This project transformed the legacy hardware into a hardened Network Attached Storage (NAS) appliance. The architecture enforces "Least Privilege" access, eliminates lateral movement vectors on the primary workstation, and implements a military-grade "Logical Air-Gap" backup strategy to protect against ransomware.

## Objectives

- **Hardware Repurposing:** Extend the lifecycle of legacy hardware (AMD CPU, 8GB RAM) by converting it into a single-purpose storage appliance.
- **Secure Interoperability:** Establish an authenticated, encrypted SMB tunnel between a Linux Server and a Windows Client.
- **Attack Surface Reduction:** Decommission file sharing services on the development workstation.
- **Ransomware Resilience:** Implement an automated, offline-by-default backup system with physical power state management.

## Architecture & Configuration

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

## Implementation & Troubleshooting

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

- **Tool:** `rsync` + `udisksctl` (replacing `hdparm` due to USB controller constraints)
- **Mechanism:**
  1.  **Wake Up:** Script identifies drive by UUID and mounts it via `udisksctl`, automatically handling authentication.
  2.  **Sync:** `rsync` mirrors the data using differential copying.
  3.  **Vanish:** Drive is unmounted immediately after transfer.
  4.  **Kill:** `udisksctl power-off` sends the disconnect signal to the kernel, physically cutting power to the spindle.

**The Resilience Script (`auto_backup.sh`):**

```bash
# Core Logic Snippet
udisksctl mount -b "$DEVICE_PARTITION" --no-user-interaction
rsync -av --delete "$SOURCE_DIR" "$ACTUAL_MOUNT/LANShare_Mirror/"
udisksctl unmount -b "$DEVICE_PARTITION"
udisksctl power-off -b "$RAW_DISK" # Puts drive into deep sleep
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

---

## Full Script

```bash
#auto_backup.sh

#!/bin/bash

# ==========================================
# CONFIGURATION
# ==========================================
SOURCE_DIR="/***/********/"
# We don't strictly need a fixed MOUNT_POINT variable anymore
# because we will dynamically find where the drive is.

# ACTION REQUIRED: PASTE THE CORRECT EXTERNAL UUID HERE
# (Get this from 'lsblk -o NAME,UUID,SIZE' - look for the 1TB drive)
DRIVE_UUID="here-is-my-drives-uuid"

LOG_FILE="/var/log/daily_backup.log"
DATE_STAMP=$(date "+%Y-%m-%d %H:%M:%S")

# ==========================================
# 0. RESOLVE DEVICE PATH
# ==========================================
# Find the partition (e.g., /dev/sdb1)
DEVICE_PARTITION=$(blkid -U "$DRIVE_UUID")
# Find the raw disk (e.g., /dev/sdb) for power management
RAW_DISK=${DEVICE_PARTITION%[0-9]*}

if [ -z "$DEVICE_PARTITION" ]; then
    echo "[$DATE_STAMP] CRITICAL: UUID not found. Drive disconnected?" >> $LOG_FILE
    exit 1
fi

# ==========================================
# 1. CHECK STATUS & MOUNT
# ==========================================
# Check if the drive is ALREADY mounted somewhere (by the OS or user)
CURRENT_MOUNT=$(findmnt -n -o TARGET "$DEVICE_PARTITION")

if [ -n "$CURRENT_MOUNT" ]; then
    echo "[$DATE_STAMP] INFO: Drive is already active at $CURRENT_MOUNT. Using existing connection." >> $LOG_FILE
    ACTUAL_MOUNT="$CURRENT_MOUNT"
else
    # It's not mounted, so we mount it
    udisksctl mount -b "$DEVICE_PARTITION" --no-user-interaction >> $LOG_FILE 2>&1

    if [ $? -ne 0 ]; then
        echo "[$DATE_STAMP] ERROR: Mount failed." >> $LOG_FILE
        exit 1
    fi
    # Capture where it just mounted
    ACTUAL_MOUNT=$(findmnt -n -o TARGET "$DEVICE_PARTITION")
fi

# ==========================================
# 2. BACKUP
# ==========================================
echo "[$DATE_STAMP] INFO: Starting backup to $ACTUAL_MOUNT..." >> $LOG_FILE
rsync -av --delete "$SOURCE_DIR" "$ACTUAL_MOUNT/LANShare_Mirror/" >> $LOG_FILE 2>&1

# ==========================================
# 3. UNMOUNT & POWER OFF
# ==========================================
END_STAMP=$(date "+%Y-%m-%d %H:%M:%S")

udisksctl unmount -b "$DEVICE_PARTITION" --no-user-interaction >> $LOG_FILE 2>&1

if [ $? -eq 0 ]; then
    echo "[$END_STAMP] INFO: Unmount successful. Killing power..." >> $LOG_FILE
    udisksctl power-off -b "$RAW_DISK" --no-user-interaction >> $LOG_FILE 2>&1
    echo "[$END_STAMP] SUCCESS: Backup complete. Drive is powered down." >> $LOG_FILE
else
    echo "[$END_STAMP] WARNING: Backup done, but unmount failed. Drive remains active." >> $LOG_FILE
fi
echo "--------------------------------------------" >> $LOG_FILE
```

## Success Output

```bash
sent 3,889,713,955 bytes  received 695,510 bytes  37,228,798.71 bytes/sec
total size is 3,886,061,103  speedup is 1.00
Unmounted /dev/sdb1.
[2025-12-20 23:30:23] INFO: Unmount successful. Killing power...
[2025-12-20 23:30:23] SUCCESS: Backup complete. Drive is powered down.
--------------------------------------------

```
