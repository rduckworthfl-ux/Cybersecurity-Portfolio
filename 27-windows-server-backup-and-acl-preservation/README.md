# Windows Server Backup & ACL Preservation Lab

> **Skills Demonstrated:** Windows Server Backup, PowerShell, NTFS ACL management, disaster recovery simulation, permission preservation
> **Platform:** Windows Server 2019 (Local Administrator)

---

## Overview

In environments where ransomware simulations, lateral movement testing, and repeated system teardowns are routine, a reliable recovery strategy is non-negotiable. Restoring files alone is not sufficient - the **Access Control Lists (ACLs)** that govern who can access what must also survive the recovery process intact. If they don't, security policies break silently and the restored environment becomes a different threat surface than the one you backed up.

This project demonstrates a complete Windows Server backup and recovery workflow: staging a controlled directory with specific user permissions, installing and configuring Windows Server Backup, simulating total data loss, and verifying that both the files and their associated NTFS permissions restored correctly.

---

## Environment

| Component        | Detail                                    |
| ------------------ | -------------------------------------------- |
| OS                 | Windows Server 2019                          |
| Shell              | PowerShell 5.1 (Administrator)                |
| Backup Tool        | Windows Server Backup (GUI + `wbadmin`)        |
| Source Data        | `C:\FolderA`                                    |
| Backup Target      | `D:\` (secondary local volume)                   |
| Recovery Target    | `C:\Restored`                                     |
| Test Account       | `user1` (local, no password)                        |

---

## Phase 1: Staging the Directory Structure and Access Controls

Created source and recovery directories, staged placeholder files, and provisioned a local test account via PowerShell (`New-LocalUser -Name user1 -NoPassword`). NTFS permissions for `user1` were applied to `C:\FolderA` through the Security tab, with default inheritance enabled to propagate the ACE to child objects - the permission state the backup must preserve.

> **Why this matters:** In a real recovery scenario after a ransomware event, restoring files without their ACLs means every affected user loses access silently. You won't see an error - files just appear locked.

## Phase 2: Installing and Configuring Windows Server Backup

Installed the Windows Server Backup feature via Server Manager (no reboot required), then configured a one-time custom backup job:

| Parameter          | Value                          |
| -------------------- | -------------------------------- |
| Backup type          | Custom (selected items only)      |
| Items selected       | `C:\FolderA`                        |
| Destination volume   | `D:\`                                |
| VSS setting          | VSS Copy Backup                       |

**Equivalent `wbadmin` command for reference:**

```cmd
wbadmin start backup -backupTarget:D: -include:C:\FolderA -allCritical -quiet
```

The backup engine created a Volume Shadow Copy of the selected path and wrote block-level data to `D:\WindowsImageBackup\`.

## Phase 3: Simulated Data Loss and Recovery Execution

Permanently deleted `C:\FolderA` (`Remove-Item -Path C:\FolderA -Recurse -Force`) to simulate total data loss equivalent to a destructive ransomware payload, then ran the Recovery Wizard:

| Step                  | Selection                            |
| ---------------------- | -------------------------------------- |
| Recovery type          | Files and folders                        |
| Items to recover       | `C:\FolderA`                                |
| Recovery destination   | Another location -> `C:\Restored`             |
| ACL handling           | Restore ACLs (default, preserved)               |

**Post-recovery validation** confirmed both files present and, critically, the `user1` ACE intact:

```powershell
(Get-Acl "C:\Restored\FolderA\file1.txt").Access |
  Select-Object IdentityReference, FileSystemRights, AccessControlType
```

```
IdentityReference      FileSystemRights              AccessControlType
------------------      ----------------              -----------------
BUILTIN\Administrators  FullControl                   Allow
NT AUTHORITY\SYSTEM     FullControl                   Allow
WIN-SERVER\user1        ReadAndExecute, Synchronize   Allow
```

**Both files restored. `user1` permissions confirmed intact.**

---

## Concepts Covered

- `New-Item` / `New-LocalUser -NoPassword` - PowerShell directory, file, and account provisioning
- NTFS ACL inheritance - applying and propagating Access Control Entries via the Security tab
- Windows Server Backup - feature installation, custom backup job configuration, VSS snapshots
- `wbadmin start backup` - CLI equivalent of GUI-driven backup jobs
- VSS (Volume Shadow Copy Service) - block-level snapshot mechanism underlying Windows backup
- Recovery Wizard - backup mount, extraction, and ACL-preserving restore to an alternate path
- `Get-Acl` - PowerShell ACL inspection for post-recovery permission validation
- `Test-Path` - confirming file system state before and after destructive operations

---

## Takeaway

Windows Server Backup's default behavior preserves NTFS ACLs during recovery - but only if the recovery job is configured correctly and the destination path is compatible. This project validates that behavior under controlled conditions. In production incident response, silently broken permissions after a restore are as dangerous as the data loss itself.

---

## Tech Stack

`Windows Server 2019` `Windows Server Backup` `wbadmin` `PowerShell` `NTFS ACLs` `VSS`
