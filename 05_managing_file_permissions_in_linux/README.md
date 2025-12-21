# Linux Access Control & Permission Hardening

## Project Description

The Principle of Least Privilege is a cornerstone of cybersecurity: users and processes should only have the bare minimum access rights necessary to perform their function.

In this project, I audited and remediated the file system permissions for the organization's research team. The objective was to identify insecure configurations—specifically "world-writable" files and improperly accessible directories—and enforce strict authorization controls using standard Linux command-line tools.

## Scenario & Strategy

The security division identified that the `~/projects` directory contained sensitive files with overly permissive settings. Unauthorized users (the "Other" category) had potential write access, and archived hidden files retained write permissions that posed an integrity risk.

My remediation strategy involved:

1. **Auditing** current permissions, including hidden files.
2. **Hardening** standard project files by revoking world-write access.
3. **Locking down** archived/hidden files to "Read-Only" status.
4. **Isolating** sensitive subdirectories to the owner only.

## Technical Walkthrough

### 1. Permissions Audit

**Objective:** Inspect the current state of the file system.
**Logic:** I used the `ls` command with the `-la` flags.

- `-l`: Displays the long format (permissions, owner, size, modification date).
- `-a`: Reveals hidden files (those starting with a `.`), such as `.project_x.txt`.

```bash
ls -la

```

### 2. Remediating World-Writable Files

**Objective:** Secure `project_k.txt` which granted Write access to "Other" users.
**Logic:** The organization's security policy strictly forbids "Other" (users outside the owner and group) from having write access. I used `chmod` to remove the write (`w`) permission from the "Other" (`o`) category.

```bash
chmod o-w project_k.txt

```

- **Result:** The permission string changed from `-rw-rw-rw-` to `-rw-rw-r--`.

### 3. Securing Hidden Archives

**Objective:** Harden the hidden archive file `.project_x.txt`.
**Logic:** Archived files should not be modified. This file had write permissions for both the User and Group.

- **Step 1:** Revoke write permissions for User (`u`) and Group (`g`).
- **Step 2:** Ensure the Group (`g`) explicitly has read (`r`) access for auditing purposes.

```bash
# Revoke write access
chmod u-w,g-w .project_x.txt

# Grant read access
chmod g+r .project_x.txt

```

### 4. Directory Isolation

**Objective:** Restrict the `drafts` directory to the owner only.
**Logic:** Subdirectories often contain work-in-progress data that should not be shared. I modified the permissions of the `drafts` directory to remove all access for Group and Other, ensuring only the owner (`researcher2`) can enter or list the directory.

```bash
chmod g-,o- drafts

```

- **Note:** This effectively sets the permissions to `drwx------` (700), the most secure setting for a private user directory.

## Summary

This project highlights the critical role of the `chmod` command in system administration. By systematically identifying risks—such as hidden files with write permissions or directories exposed to the group—I was able to enforce the Principle of Least Privilege, significantly reducing the attack surface of the research server.
