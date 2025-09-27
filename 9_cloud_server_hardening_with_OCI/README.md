## Project: Hardening & Utilizing a Cloud Server with Oracle Cloud Infrastructure (OCI)

### Project Overview

This project details the end-to-end process of deploying a secure, public-facing Ubuntu Linux server and subsequently configuring it as a personal cloud storage solution. The project demonstrates a **defense-in-depth security strategy** and practical system integration, incorporating critical lessons learned from real-world troubleshooting scenarios. The process covers foundational SSH key management, cloud resource deployment, multi-layered security hardening, and final service implementation, resulting in a robust and useful cloud asset.

---

## Technical Walkthrough & Implementation

This section details the hands-on technical phases of the engagement. Each step is presented not just as a command that was run, but as a justified action derived from analysis and troubleshooting.

### Module 1: Foundational Setup & Key Management

**Objective:** To establish a secure and reliable foundation on the local machine (Kali Linux) and within the OCI console, ensuring that all subsequent steps are built upon a solid base.

* **Step 1.1: Local Environment Preparation (Kali Linux)**
    * **Action:** Open the Kali terminal and execute the following command to clear any existing SSH keys.
        ```bash
        rm -f ~/.ssh/*
        ```
    * **Justification:** We started with a clean SSH directory to prevent any conflicts from old or temporary keys. This ensures that the key we generate is the definitive one for this project, eliminating a common source of "Permission denied" errors.

* **Step 1.2: Generate Primary SSH Key**
    * **Action:** Execute the following command to generate a new key.
        ```bash
        ssh-keygen -t ed25519
        ```
    * **Justification:** We chose the `ed25519` algorithm because it offers better security and performance compared to older types like RSA. This creates a public/private key pair, which is the modern standard for secure, passwordless authentication, preventing brute-force password attacks.

* **Step 1.3: Prepare the Public Key**
    * **Action:** Execute `cat ~/.ssh/id_ed25519.pub` and copy the output.
    * **Justification:** The `cat` command displays the contents of the public key file. This key is the "lock" that we will install on the server. It's safe to share and allows anyone with the corresponding private key (which never leaves the local machine) to gain access.

### Module 2: Cloud Deployment & Troubleshooting

**Objective:** To successfully provision a virtual server instance in the cloud, navigating common platform-specific challenges like resource availability and network configuration.

* **Step 2.1 - 2.4: Instance Configuration & Key Installation**
    * **Action:** In the OCI console, navigate the "Create instance" workflow. Be prepared to change the Availability Domain or select an alternate VM shape (`VM.Standard.E2.1.Micro`) to overcome "Out of capacity" errors. Ensure a new Virtual Cloud Network (VCN) is created with a public IPv4 address assigned. In the "Add SSH keys" section, paste the copied `ed25519` public key.
    * **Justification:** Our troubleshooting revealed that the OCI Free Tier has fluctuating resource availability and that new accounts may require a new VCN. A public IP is essential for internet accessibility. Pasting the public key during creation is the most critical step for ensuring a successful first connection, as it instructs the server to trust our local Kali machine.

### Module 3: System Initialization & Maintenance

**Objective:** To establish a stable and secure operating environment by connecting to the server and bringing its software to a fully supported, up-to-date state.

* **Step 3.1: First Connection**
    * **Action:** From the Kali terminal, execute `ssh ubuntu@<YOUR_NEW_PUBLIC_IP>`. Type `yes` when prompted about the host's authenticity.
    * **Justification:** This action verifies that the key pair authentication is working correctly. The authenticity prompt is a standard security feature to prevent man-in-the-middle attacks.

* **Step 3.2: System Package Upgrade**
    * **Action:** Run the following commands.
        ```bash
        sudo apt update
        sudo apt upgrade -y
        ```
    * **Justification:** Before any major changes, we ensure all currently installed software packages are updated to their latest versions. This patches known vulnerabilities and ensures system stability.

### Module 4: System Stability Verification (Critical Finding)

**Objective:** To proactively prevent loss of remote access by verifying and correcting a critical service configuration, a step identified through root cause analysis of a previous failed deployment.

* **Step 4.1 & 4.2: Verify and Enable SSH Service**
    * **Action:** Before rebooting, check if the SSH service starts on boot with `sudo systemctl is-enabled ssh`. The check revealed the service was `disabled`. The command `sudo systemctl enable ssh` was executed to correct this.
    * **Justification:** During a previous attempt, we experienced a "Connection refused" error after a reboot. Root cause analysis determined the SSH service was not configured to start automatically. This verification and remediation step directly fixes the identified fault, guaranteeing persistent remote access.

* **Step 4.3: System Reboot**
    * **Action:** Execute `sudo reboot`.
    * **Justification:** A reboot is required to apply some package updates. With the SSH service now confirmed to be enabled, this action can be performed with confidence.

### Module 5: Multi-Layered Security Implementation (Defense in Depth)

**Objective:** To construct a robust "Defense in Depth" security posture where multiple independent layers protect the server from threats.

* **Step 5.1: Layer 1 - The Cloud Firewall (NSG)**
    * **Action:** In OCI, create a Network Security Group (NSG) and associate it with the server's network interface. Add ingress rules to allow SSH (port 22) only from a specific home IP, and another to allow web traffic (ports 80, 443) from anywhere.
    * **Justification:** The NSG acts as the first line of defense, filtering traffic at the cloud level before it ever reaches our server. This enforces the principle of least privilege, drastically reducing the attack surface for unauthorized login attempts.

* **Step 5.2: Layer 2 - The OS Firewall (UFW)**
    * **Action:** After discovering the `ufw` command was not found, install it with `sudo apt install ufw -y`. Then, configure a default-deny policy and explicitly allow SSH, HTTP, and HTTPS traffic.
    * **Justification:** This creates a second, redundant firewall layer. If the cloud-level NSG were ever misconfigured, the OS firewall would still protect the server, a core concept of defense in depth.

* **Step 5.3: Layer 3 - Service Hardening (SSH)**
    * **Action:** Edit `/etc/ssh/sshd_config` to set `PasswordAuthentication no` and `PermitRootLogin no`. Restart the ssh service.
    * **Justification:** This further hardens the most critical remote access point. Disabling password authentication makes brute-force attacks impossible. Disallowing direct root login forces administrators to use privilege escalation, which creates a better audit trail.

* **Step 5.4: Layer 4 - Active Intrusion Prevention (Fail2Ban)**
    * **Action:** Install the `fail2ban` package using `sudo apt install fail2ban -y`.
    * **Justification:** This moves from passive defense to active threat mitigation. Fail2Ban monitors logs for malicious patterns and automatically updates the OS firewall to block an attacker's IP address, providing automated, real-time protection.

### Module 6: Secure Personal Cloud Storage Implementation

**Objective:** To leverage the hardened server by configuring it as a secure, personal cloud storage solution accessible via a drag-and-drop interface from a Windows desktop.

* **Step 6.1: Server-Side Preparation**
    * **Action:** On the server, execute `mkdir ~/storage`.
    * **Justification:** This command creates a dedicated directory to house the cloud storage files, keeping them organized and separate from system files.

* **Step 6.2 & 6.3: Client-Side Configuration & Cross-Environment Key Integration (Critical Finding)**
    * **Action:** Install WinSCP on Windows 11 and configure it for SFTP. An initial "Server refused our key" error was traced to the fact that the Kali (WSL) environment and native Windows maintain separate SSH key stores. The issue was resolved by copying the private key from the WSL filesystem to the Windows filesystem.
        ```bash
        cp ~/.ssh/id_ed25519 /mnt/c/Users/<your_username_here>/.ssh/
        ```
    * **Justification:** We chose SFTP (SSH File Transfer Protocol) because it uses the existing, highly secure SSH connection, meaning all data is encrypted in transit. The key copy action made the private key accessible to WinSCP, a native Windows application, demonstrating a crucial understanding of the interaction between WSL and the host OS.

---

### Key Learnings & Troubleshooting Log

* **Issue:** SSH connection drops during a `nano` editing session, leaving a `.swp` lock file.
    * **Resolution:** The leftover lock file (e.g., `/etc/ssh/.sshd_config.swp`) must be manually deleted with `sudo rm` before the real configuration file can be edited again. This demonstrates a practical recovery skill for remote administration.

* **Issue:** Initial connection attempts fail with "Permission denied (publickey)".
    * **Resolution:** This is almost always caused by an error in pasting the public key during instance creation. The most reliable solution is to terminate the instance and create a new one, ensuring the key is copied perfectly.

* **Issue:** "Connection refused" after a major OS upgrade or reboot.
    * **Resolution:** The root cause was the SSH service being disabled and not starting on boot. The permanent fix is to proactively run `sudo systemctl enable ssh` before any reboot to ensure persistent remote access.

---

### Final Architecture

The final configuration resulted in a multi-layered, secure architecture that provides robust protection for the server and its data, both at rest and in transit.

```Network Architecture Diagram
+--------------------------------------------------+
|                                                  |
|                YOUR HOME NETWORK                 |
|                                                  |
|  +--------------------------------------------+  |
|  |                                            |  |
|  |               Windows 11 PC                |  |
|  |                                            |  |
|  |  +--------------+     +---------------+    |  |
|  |  |    WinSCP    |     |    Kali WSL   |    |  |
|  |  +--------------+     +---------------+    |  |
|  |         |                    |             |  |
|  +--------------------------------------------+  |
|          |                    |                  |
+----------|--------------------|------------------+
           |                    |
     (Your Router)        (The Internet) --->
           |                    |
           |                    |
+----------|--------------------|------------------+
| SFTP (Port 22) <------> SSH (Port 22)           |
| (File Transfers)      (Admin Commands)         |
|                                                  |
|      ORACLE CLOUD INFRASTRUCTURE (OCI)           |
|                                                  |
|  +--------------------------------------------+  |
|  |        Virtual Cloud Network (VCN)         |  |
|  |                                            |  |
|  |  +--------------------------------------+  |  |
|  |  |       Network Security Group         |  |  | (Layer 1: Cloud Firewall)
|  |  |  (Allows Port 22 & 80/443)           |  |  |
|  |  +--------------------------------------+  |  |
|  |                   |                        |  |
|  |                   V                        |  |
|  |  +--------------------------------------+  |  |
|  |  |          Your Ubuntu Server          |  |  |
|  |  |                                      |  |  |
|  |  |  +---------------------------------+ |  |  |
|  |  |  | UFW Firewall                    | |  |  | (Layer 2: OS Firewall)
|  |  |  +---------------------------------+ |  |  |
|  |  |  | Fail2Ban                        | |  |  | (Layer 4: Active Defense)
|  |  |  +---------------------------------+ |  |  |
|  |  |  | SSH Service (Hardened)          | |  |  | (Layer 3: Secure Access)
|  |  |  +---------------------------------+ |  |  |
|  |  |  | Storage Folder                  | |  |  |
|  |  |  +---------------------------------+ |  |  |
|  |  +--------------------------------------+  |  |
|  +--------------------------------------------+  |
|                                                  |
+--------------------------------------------------+
```

* **Layer 1 (Cloud Firewall):** The OCI Network Security Group (NSG) acts as the first gatekeeper, allowing only approved traffic from specified sources to reach the server's virtual network card.
* **Layer 2 (OS Firewall):** The UFW firewall on the Ubuntu server provides a second layer of packet filtering, ensuring that even if the NSG were compromised, the host itself remains protected.
* **Layer 3 (Secure Access):** The SSH service is hardened to disallow passwords and direct root login, forcing all administrative and file transfer connections to authenticate with a secure cryptographic key.
* **Layer 4 (Active Defense):** Fail2Ban actively monitors for malicious login attempts and automatically blocks offending IP addresses at the OS firewall level.

This defense-in-depth model ensures that a failure in any single security control does not lead to a full system compromise.