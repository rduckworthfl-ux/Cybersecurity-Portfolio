# Project 18: Advanced Linux Authentication Recovery & Bootloader Manipulation

## 1. Executive Summary

**Objective:** Regain administrative access to a critical development machine (HP 15-ba077cl / Ubuntu 22.04) following a complete account lockout caused by a scripted configuration error.
**Constraints:** \* **Zero-Data Loss:** Machine hosted the local database for the "Vulcan Scan" project.

- **Hardware Lock:** "Fast Boot" UEFI settings prevented standard keyboard interrupts.
- **Cryptographic Failure:** Account was locked due to a plaintext string injection into the shadow file.

**Outcome:** Successfully bypassed the bootloader, remounted the root filesystem, and manually reconstructed the password hash using OpenSSL, restoring access without data loss.

---

## 2. Root Cause Analysis (The Diagnosis)

The incident originated from a maintenance script that attempted to set the user password using the `usermod` command incorrectly:

```bash
# THE INCORRECT COMMAND (Triggered the Lockout)
usermod -p "password123" username-here
```
````

**Technical Failure:**
The `-p` flag in `usermod` expects a pre-encrypted hash (e.g., `$6$salt$hash...`). By passing a plaintext string, the system wrote `"password123"` literally into `/etc/shadow`.

- **Authentication Process:** When the user enters "password123" at login, PAM (Pluggable Authentication Modules) hashes the input (SHA-512) and compares it to the stored string.
- **Result:** `SHA512("password123") != "password123"`. The account was cryptographically impossible to access.

---

## 3. Recovery Procedure: Step-by-Step

### Phase 1: Bypassing the UEFI "Fast Boot" Lock

**Challenge:** The target machine's UEFI initialized hardware too quickly for standard interrupt keys (`Shift` or `Esc`) to register, rendering the GRUB menu inaccessible.

**Solution: The "Force Fail" Methodology**
I triggered the system's automated "failed boot detection" to force the menu to appear.

1. Powered on the machine.
2. **Hard Kill:** Immediately pressed and held the power button upon the first sign of the OS loading spinner.
3. **Repetition:** Repeated this process 3 times consecutively.
4. **Success:** On the 4th boot, the BIOS detected instability and paused, automatically presenting the GRUB boot menu.

### Phase 2: Gaining Root Privileges (Runlevel manipulation)

From the GRUB menu, I bypassed the login manager entirely:

1. Selected **"Advanced options for Ubuntu"**.
2. Selected the kernel entry ending in **"(recovery mode)"**.
3. In the Recovery Menu, selected **"root - Drop to root shell prompt"**.

**State:**

- **User:** `root` (UID 0)
- **Filesystem:** Read-Only (`/dev/sda1` mounted as `ro`)
- **Network:** Disabled

### Phase 3: Filesystem Write Access

By default, Recovery Mode mounts the root filesystem as Read-Only to prevent corruption. Password changes cannot be written to disk in this state.

**Command Executed:**

```bash
mount -o remount,rw /

```

- **Result:** The root partition was successfully remounted with Read-Write (RW) permissions.

### Phase 4: The Cryptographic Fix

Standard `passwd` attempts failed to resolve the specific corruption caused by the previous `usermod` error. I proceeded to manually generate a compliant hash and inject it directly into the user account configuration.

**Command Executed:**

```bash
usermod -p $(openssl passwd -6 'password123') username-here

```

**Breakdown of Command:**

- **`$( ... )`**: Command substitution runs the inner command first.
- **`openssl passwd -6`**: Invokes the OpenSSL library to generate a salt and hash the string using **SHA-512** (indicated by the `$6$` prefix in the output).
- **`usermod -p`**: Applies the valid, encrypted hash to the user `ryan`.
- **Result:** The shadow file entry was overwritten with a valid hash.

---

## 4. Establishing Redundancy (Break-Glass Account)

To adhere to the "Two is One, One is None" principle, I created a secondary administrative account while holding root access. This ensures future recovery does not require physical boot interruption.

**Commands Executed:**

1. **Create the user** (with home dir `-m` and bash shell `-s`):

```bash
useradd -m -s /bin/bash ops

```

2. **Set the password** (Interactively):

```bash
passwd ops

```

3. **Grant Sudo Privileges:**

```bash
usermod -aG sudo ops

```

4. **Verification:**

```bash
grep ops /etc/passwd

```

_Output confirmed: `ops:x:1001:1001::/home/ops:/bin/bash_`

---

## 5. Final Verification

**Command Executed:**

```bash
reboot

```

**Verification:**

- Logged in as `ryan` using the recovered password.
- Verified access to `sudo`.
- Confirmed `ops` account availability.
- **System Status:** Fully Operational.



---

