# Linux User Provisioning, SSH Access, and Forced Password Rotation

> **Skills Demonstrated:** Linux user account management, `/etc/passwd` auditing, SSH remote authentication, password expiration policy enforcement, credential lifecycle validation
> **Platform:** Ubuntu Server ("SecVM") + Ubuntu Workstation ("Linux02")

---

## Overview

Account provisioning looks trivial on paper, but it's one of the most common places security policy quietly breaks down. A new hire account gets created with a shared default password, nobody forces a rotation, and that credential sits valid indefinitely - exactly the kind of stale, unmanaged account that shows up in real attack paths. This project walks through the full lifecycle of a Linux user account: provisioning it correctly on the server, verifying it does not already exist on a separate workstation, establishing a remote SSH session under the new identity, and enforcing a mandatory password reset on first login.

---

## Lab Environment

| Role          | Hostname | IP Address     | Purpose                                    |
| ------------- | -------- | -------------- | -------------------------------------------- |
| Server        | SecVM    | 192.168.10.25  | Hosts the target account and SSH service    |
| Workstation   | Linux02  | --             | Local login origin for the new user, SSH client |
| Admin Account | labuser  | --             | Password: Passw0rd!                          |
| New Account   | tlannister | --           | Full name: Tyrion Lannister                  |

---

## Phase 1: Provisioning the User Account on SecVM

Ran `adduser` interactively on the server to generate the new profile, setting the initial password and identity metadata, then queried `/etc/passwd` directly to confirm the entry:

```bash
sudo adduser tlannister
cat /etc/passwd | grep tlannister
```

```
tlannister:x:1001:1001:Tyrion Lannister,,,:/home/tlannister:/bin/bash
```

The returned line confirms the UID/GID assignment, full name field, home directory path, and default shell - all consistent with a standard `adduser` provisioning flow.

## Phase 2: Baseline Verification and Account Creation on Linux02

Provisioning on the server does not automatically create the same account on other hosts in the environment. A clean baseline check on the workstation confirmed `tlannister` had no local profile prior to this exercise (`grep -c` returned `0`), before provisioning the account locally as well.

> **Key concept:** Local account state is host-specific. A user existing on the server does not imply SSH login access will succeed from every client - the local account controls the workstation session, while the remote account on SecVM controls what happens once the SSH tunnel is established.

## Phase 3: Switching Profiles and Establishing SSH Access

Switched the workstation session to the new `tlannister` profile, then opened an SSH connection to the server:

```bash
ssh tlannister@192.168.10.25
```

Verified the shell context had genuinely shifted to the remote server (rather than displaying a renamed local prompt) via `hostnamectl`, which confirmed `Static hostname: secvm`.

## Phase 4: Enforcing a Mandatory Password Reset

A freshly provisioned account with an admin-set password is a liability if that credential never rotates. On the server, the account was flagged for immediate expiration:

```bash
passwd --expire tlannister
```

The next SSH login was interrupted by OpenSSH/PAM's forced-reset workflow, requiring `tlannister` to set a new password before the session was granted, and the server terminated the session immediately after the change - requiring a fresh authentication attempt with the new credential, which was verified successfully on the next connection.

---

## Concepts Covered

- `adduser` - interactive Linux account provisioning with home directory and GECOS field setup
- `/etc/passwd` - reading and auditing the flat-file user database, understanding UID/GID/shell fields
- `grep -c` - producing a scriptable baseline count for account-existence checks
- Host-specific local accounts vs. remote server accounts - why SSH access depends on both ends
- SSH host key verification - the ECDSA fingerprint trust-on-first-use model
- `hostnamectl` - confirming genuine remote shell context vs. a spoofed or misleading prompt
- `passwd --expire` - server-side enforcement of mandatory credential rotation
- Forced password change workflow - how OpenSSH/PAM interrupts a login to require a reset before granting a shell

---

## Security Takeaways

Provisioning an account correctly is only half the job - the credential lifecycle after creation is where most identity-related breaches actually happen. Forcing an immediate password change via `passwd --expire` closes the window where a default, admin-known password remains valid indefinitely. Combined with SSH host key verification, this workflow reflects the baseline identity hygiene that should exist before any new account is trusted with production access.

---

## Tech Stack

`Ubuntu Server` `OpenSSH` `PAM` `adduser` `passwd` `/etc/passwd`
