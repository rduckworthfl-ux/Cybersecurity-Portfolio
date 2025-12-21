# Case Study: Secure OS Migration and Endpoint Hardening for Legacy Hardware

---

## 1. Executive Summary

This project involved reviving an older HP 15-ba077cl laptop initially running a slow and potentially insecure Windows installation. The primary goal was to replace Windows with a lightweight, secure, and performant Linux distribution suitable for a non-technical home user (referred to as the "customer"). The project successfully navigated significant hardware compatibility issues during bootable media creation and OS booting, ultimately resulting in a stable Lubuntu 22.04 LTS installation. Post-installation hardening measures were implemented, including firewall configuration, automated security updates, antivirus setup, and browser security enhancements, significantly improving the device's usability and security posture.

---

## 2. Problem Statement / Initial Assessment

* **Hardware:** HP 15-ba077cl laptop (UEFI, 8GB RAM, AMD APU).
* **Initial State:** The laptop was running an unspecified version of Windows, exhibiting extremely poor performance, including slow operation and significant overheating. Access to the existing Windows installation was blocked by an unknown password, preventing data recovery (though ultimately deemed unnecessary by the customer).
* **Security Concerns:** An unmaintained, poorly performing Windows installation poses significant security risks due to potential unpatched vulnerabilities and lack of modern security features. The performance issues also rendered the device impractical for daily use.
* **Goal:** Replace Windows with a secure, stable, and lightweight Linux distribution to restore usability and provide a safe computing environment for a non-technical home user. Document the process for a cybersecurity portfolio.

---

## 3. Troubleshooting & OS Selection

The initial phase involved significant troubleshooting related to bootable media creation and hardware compatibility.

### 3.1. Bootable Media Creation Challenges

* **Initial Attempt:** Linux Mint 22.2 XFCE was chosen initially for its user-friendliness and relatively low resource usage.
* **Creation Environment:** Bootable USB (microSD + SD Adapter + USB Reader) was created using Rufus on an Alienware m16r2 workstation running Windows 11.
* **Identified Conflicts:**
    * **Antivirus Interference:** BitDefender's "Immunization" feature, initially activated on drive insertion, was suspected of corrupting the boot structure.
    * **Windows Ejection Bug:** A known quirk on the Alienware workstation prevented safe USB ejection via standard methods, reporting the device as "still in use". Forcible removal after failed ejection attempts likely caused filesystem corruption on the USB drive.
* **Symptoms:** Windows prompted to "Scan and fix" the created USB drive upon re-insertion, indicating corruption. The initial boot attempt on the HP laptop failed with "Unable to find a medium containing a live file system".
* **Resolution:**
    * Temporarily disabled relevant BitDefender USB scanning/immunization features before drive insertion.
    * Implemented a robust safe ejection workaround using Windows Device Manager (`Disk drives` -> `Uninstall device` -> `Action` -> `Scan for hardware changes` -> Immediate eject via tray icon), which successfully bypassed the "in use" bug and resulted in a clean unmount confirmed by the "Safe To Remove Hardware" notification.

### 3.2. Linux Mint Boot Failures (Hardware Incompatibility)

* Despite creating clean bootable media, Linux Mint 22.2 (Ubuntu 24.04 base) failed to boot correctly on the HP 15-ba077cl.
* **Symptoms:**
    * **Normal Mode:** Screen flashed on/off repeatedly after showing the Mint logo, indicating graphics driver initialization failure.
    * **Compatibility Mode:** Boot process hung in a loop, repeatedly starting/stopping `lightdm.service` and `gpu-manager.service`, with blinking text output.
* **Troubleshooting Steps (Kernel Parameters):** Various kernel parameters were attempted by editing the GRUB boot entry for compatibility mode:
    * `nomodeset`: Already present in compatibility mode; insufficient to resolve the issue.
    * `radeon.modeset=0`: Added specifically to target the AMD graphics driver; loop persisted, though blinking rate slightly changed.
    * `acpi=off`: Added as a more drastic measure to disable power management/hardware configuration; loop still persisted.
* **Conclusion:** The persistent failure even with multiple standard workarounds strongly indicated an incompatibility between the newer kernel/driver stack in the Ubuntu 24.04 base and the specific AMD APU/graphics hardware in the HP 15-ba077cl.

### 3.3. OS Selection Rationale: Lubuntu 22.04 LTS

* Based on the Mint 22.2 failures, a different distribution was selected.
* **Lubuntu 22.04.5 LTS** was chosen for the following reasons:
    * **Ubuntu 22.04 LTS Base:** Uses an older, potentially more stable kernel and driver set compared to the 24.04 base, increasing the likelihood of compatibility with the target hardware.
    * **LXQt Desktop Environment:** Lubuntu uses LXQt, which is even more lightweight than XFCE, making it ideal for maximizing performance on the low-spec HP laptop (8GB RAM, older AMD APU).
    * **Successful Boot:** Lubuntu 22.04.5 booted successfully into the live environment without requiring additional kernel parameters. A Rufus warning about a revoked UEFI bootloader was noted but deemed irrelevant as Secure Boot was disabled on the target machine.

---

## 4. Installation Process

The installation proceeded using the Lubuntu graphical installer (Calamares) from the live USB environment.

* **Internet Connection:** Established Wi-Fi connection within the live environment using the `nmcli` terminal command (required using single quotes for a password containing '!') after the GUI applet failed to appear.
* **Installation Type:** Selected **"Erase disk and install Lubuntu"** to completely remove the existing Windows partitions and dedicate the entire internal drive to Lubuntu.
* **Updates & Drivers:** Opted to **download updates** and **install third-party software** during installation for completeness and hardware support.
* **Partitioning & Swap:** Allowed the installer to perform automatic partitioning, which includes the creation of an **automatic swap file** (suitable for this hardware configuration).
* **User Setup:** Created a standard (non-administrator by default) user account with a strong password.
* **Completion:** Installation completed successfully, followed by a system restart and removal of the USB medium when prompted.

---

## 5. Post-Installation Hardening

Several steps were taken to secure the fresh Lubuntu installation for the non-technical end-user:

1.  **System Updates:** Immediately applied all available system updates via the Update Notifier upon first boot, including numerous security patches. Configured automatic checking and installation of security updates daily via `Software Sources` GUI.
2.  **Firewall Configuration:** Enabled the Uncomplicated Firewall (UFW) using `sudo ufw enable`. Verified status with `sudo ufw status verbose`, confirming it defaults to denying incoming connections while allowing outgoing, providing essential network protection.
3.  **Antivirus Installation:** Installed `ClamAV` and its graphical front-end `ClamTk` (`sudo apt install clamtk -y`) to provide on-demand scanning capabilities for downloaded files or user directories, offering peace of mind without the constant resource usage of a background daemon. Configured daily signature updates via the ClamTk GUI.
4.  **Web Browser Security:** Installed the **uBlock Origin** extension in the default Firefox browser to block intrusive and potentially malicious advertisements, significantly reducing the user's exposure to web-based threats like malvertising and phishing.
5.  **User Account Security:** Confirmed the primary user account operates with standard privileges, requiring `sudo` (and password entry) for administrative tasks. Ensured a strong password was set during installation. (Guest account status check recommended - *SysAdmin note: confirm if guest login is disabled via GUI later*).

---

## 6. Results & Performance

* **Performance:** The difference was immediate and significant. The laptop runs Lubuntu 22.04 LTS smoothly, responsively, and remains cool during operation, a stark contrast to the overheating and sluggishness experienced under Windows.
* **Security Posture:** The device is now running a currently supported Long-Term Support (LTS) Linux distribution with critical security updates configured to install automatically. The enabled firewall, optional antivirus, and browser-level ad/tracker blocking provide multiple layers of defense suitable for a home user.
* **Usability:** The lightweight LXQt desktop environment provides a familiar and easy-to-use interface for the non-technical customer, fulfilling the project's primary goal.

---

## 7. Conclusion & Learnings

The project successfully replaced an insecure and poorly performing Windows installation on an older HP laptop with a lightweight, secure, and performant Lubuntu 22.04 LTS system. The primary challenges involved overcoming hardware incompatibilities with newer Linux kernels/drivers (requiring systematic troubleshooting with boot parameters and ultimately a change in distribution base) and reliably creating bootable media on a workstation with a known USB ejection defect (requiring specific Device Manager workarounds).

This case study demonstrates proficiency in:

* Diagnosing and resolving complex Linux boot issues related to hardware compatibility (graphics, ACPI).
* Systematic troubleshooting of bootable media creation errors, including mitigating third-party software conflicts (antivirus) and OS-level hardware bugs (Windows USB ejection).
* Selecting appropriate Linux distributions based on hardware specifications and user needs (LTS vs. rolling, desktop environment choices).
* Performing secure Linux OS installation and implementing essential post-installation hardening measures (updates, firewall, AV, browser security) tailored for an end-user environment.
* Clear documentation of technical processes, challenges, and solutions.

The significant improvement in performance and security validates the choice of migrating away from the unsupported Windows installation on this hardware.