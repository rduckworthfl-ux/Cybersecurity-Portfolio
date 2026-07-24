# Linux Data Archival & Recovery Lab

> **Skills Demonstrated:** `tar`, `gzip`, file system operations, backup strategy, disaster recovery simulation
> **Platform:** Linux (root shell)

---

## Overview

When you spend time spinning up virtual machines and stress-testing systems, you need a reliable way to restore your environment quickly. This project demonstrates a complete backup and recovery workflow using native Linux command-line tools - no third-party software required. It covers staging a mock data environment, creating standard and compressed archives, simulating total data loss, and performing full restoration.

---

## Environment

| Component        | Detail                     |
| ----------------- | --------------------------- |
| Shell             | Bash (root)                 |
| Archive Tool      | `tar` (GNU)                  |
| Compression       | `gzip`                        |
| Data Directories  | `/Data/DirA`, `/Data/DirB`   |
| Archive Target    | `/Archive`                    |
| Recovery Target   | `/Restored`                    |

---

## Phase 1: Staging the Environment

Constructed a mock data structure: a primary `/Data` directory with two subdirectories, ten staged files, and dedicated folders for archives and recovery.

```bash
mkdir /Data; mkdir /Data/DirA; mkdir /Data/DirB
touch /Data/DirA/file1 /Data/DirA/file2 /Data/DirA/file3 /Data/DirA/file4 /Data/DirA/file5
touch /Data/DirB/file6 /Data/DirB/file7 /Data/DirB/file8 /Data/DirB/file9 /Data/DirB/file10
mkdir /Archive; mkdir /Restored
```

## Phase 2: Standard Archiving and Appending

Created a baseline uncompressed `.tar` archive of `DirA`, then tested incremental backup by appending a newly created `file99` to the existing archive without repacking it:

```bash
tar -cvf /Archive/backup1.tar /Data/DirA/*
touch /Data/DirA/file99
tar -rf /Archive/backup1.tar /Data/DirA/file99
tar -tf /Archive/backup1.tar
```

> **Key Concept:** The `-r` flag appends to an existing archive without extracting and repacking it - critical for incremental backup workflows.

## Phase 3: Compressed Archiving with Exclusions

Switched to `gzip` compression for `DirB` to reduce archive size, explicitly excluding `file10` to simulate filtering out temporary or irrelevant data:

```bash
tar -czf /Archive/backup2.tar.gz --exclude='/Data/DirB/file10' /Data/DirB/*
tar -tf /Archive/backup2.tar.gz
```

`file10` is absent from the manifest - the `--exclude` flag worked as intended, and the compressed archive was significantly smaller than the uncompressed equivalent.

## Phase 4: Simulated Data Loss & Restoration

Wiped both original directories to simulate a complete data loss event, then extracted both archives to `/Restored` and verified every file - including the incrementally appended `file99` - restored successfully:

```bash
rm -R /Data/DirA
rm -R /Data/DirB
cd /Restored
tar -xf /Archive/backup1.tar
tar -xzvf /Archive/backup2.tar.gz -C /Restored
```

**All six files restored, including `file99`, which was appended after the initial archive was created.**

---

## Concepts Covered

- `tar -cvf` - create verbose uncompressed archive
- `tar -rf` - append files to an existing archive (incremental backup)
- `tar -czf` - create compressed gzip archive
- `--exclude` - filter specific files from an archive
- `tar -tf` - inspect archive contents without extraction
- `tar -xf` / `tar -xzvf` - extract standard and compressed archives
- `rm -R` - recursive deletion (simulated data loss event)
- `-C` flag - extract to a specific target directory

---

## Takeaway

A solid backup strategy doesn't require enterprise tooling. With `tar` and a consistent naming convention, you can build incremental, compressed, and exclusion-aware archives entirely from the command line - fast enough to fit into any lab teardown and restore workflow.

---

## Tech Stack

`Linux` `tar` `gzip` `Bash` `Disaster Recovery Simulation`
