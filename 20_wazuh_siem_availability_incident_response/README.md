# Incident Report: Wazuh SIEM Full Disk Exhaustion - Dual Root Cause

**Incident ID:** INC-2026-0406-001  
**Date:** April 6, 2026  
**Analyst:** Ryan Duckworth  
**Classification:** Availability Incident - Full Service Outage  
**Severity:** Medium-High  
**Status:** Resolved  
**Framework Reference:** NIST SP 800-61 Rev. 2

---

## Executive Summary

On April 6, 2026, the Wazuh SIEM stack deployed on `os1` crashed due to complete disk exhaustion. All three containers - `wazuh.manager`, `wazuh.indexer`, and `wazuh.dashboard` - stopped running, creating a full monitoring blind spot across the home lab environment.

What initially appeared to be a straightforward "ran out of disk space" issue turned out to be a **two-layer infrastructure failure**. The underlying Ubuntu VM had been initialized with an 80GB VMware disk allocation, but the LVM logical volume was never extended beyond its default ~39GB - leaving over half the provisioned disk space sitting unused and unallocated. On top of that, no Wazuh ISM (Index State Management) retention policy had been configured at deployment, allowing the `wazuh_queue` Docker volume and OpenSearch alert indices to grow unbounded. Within approximately 48 hours of deployment, the available ~39GB was exhausted.

The investigation required multiple diagnostic phases, several failed recovery attempts, and eventually the discovery of the VM disk allocation gap before a viable fix path emerged. Resolution was achieved by extending the LVM logical volume to use the full physical disk, followed by redeploying the Wazuh stack and applying a 30-day ISM retention policy. No confidentiality or integrity impact occurred. No threat actor was involved.

---

## Environment

| Component             | Detail                                                                |
| --------------------- | --------------------------------------------------------------------- |
| **Affected Host**     | os1 (Ubuntu 22.04 LTS, Alienware)                                     |
| **Hypervisor**        | VMware (VM provisioned with 80GB disk)                                |
| **Platform**          | Wazuh 4.x → upgraded to 4.8.0 during recovery                         |
| **Affected Services** | wazuh.indexer, wazuh.manager, wazuh.dashboard (all stopped)           |
| **LVM Volume**        | `/dev/mapper/ubuntu--vg-ubuntu--lv` - 39GB effective (77GB after fix) |
| **Physical Disk**     | `/dev/sda3` - 80GB VMware provisioned, LVM not extended               |
| **Network Access**    | 100.81.156.19 (Tailscale VPN)                                         |
| **Discovery Method**  | Manual - `docker exec` returned "no such container"                   |

---

## 1. Detection & Initial Discovery

The incident was discovered when a `docker exec` command targeting the Wazuh indexer container returned:

```
Error response from daemon: No such container: single-node-wazuh.indexer-1
```

`docker-compose ps` confirmed no containers were running at all - the entire stack was dead. An immediate `df -h` revealed the underlying cause:

```
Filesystem                         Size   Used  Avail  Use%  Mounted on
/dev/mapper/ubuntu--vg-ubuntu--lv  39G    38G   0      100%  /
```

The root volume was **completely full**. Zero bytes available.

---

## 2. Investigation & Diagnostic Phase

What followed was a multi-step investigation to find exactly what consumed the disk and recover enough space to restore operations.

### Phase 1 - Docker Cleanup Attempts

The first instinct was to reclaim space from Docker's layer cache:

```bash
docker system prune
```

**Result:** `Total reclaimed space: 4.502GB`

```bash
df -h /
# /dev/mapper/ubuntu--vg-ubuntu--lv  39G  34G  2.9G  93%
```

Partial success - went from 100% to 93% - but still critically low with only ~2.9GB free. Not enough to safely bring the stack back up.

### Phase 2 - System-Level Space Recovery

```bash
# Vacuum old systemd journal logs
journalctl --vacuum-size=100M
# Result: Freed 639.4MB of archived journals

# Clear APT package cache
apt-get clean

# Stop Docker, clear overlay filesystem, restart
sudo systemctl stop docker
sudo du -sh /var/lib/docker/overlay2/   # → 8.0K (already nearly empty)
sudo rm -rd /var/lib/docker/overlay2
sudo systemctl start docker
```

**Result:** These recovered only marginal space. After all three steps, `df -h` still showed **39G 34G 2.8G 93%**. The disk remained critically full.

### Phase 3 - Disk Visualization with ncdu

With standard cleanup failing to make a dent, installed `ncdu` to get a clear visual breakdown of where disk space was actually going:

```bash
sudo apt-get install -y ncdu
sudo ncdu /
```

**ncdu output (top consumers):**

```
27.4 GiB [####################] /var          ← DOMINANT CONSUMER
 4.0 GiB [###               ] /var/swap.img
 2.5 GiB [#                 ] /usr
 2.1 GiB [#                 ] /snap
103.3 MiB [                  ] /boot

Total disk size: 36.1 GiB
```

`/var` was consuming 27.4 GiB. `/var/lib/docker` was the primary suspect.

### Phase 4 - Docker Volume Deep-Dive

```bash
# Check total Docker footprint
sudo du -sh /var/lib/docker/
# → 24G  /var/lib/docker/

# List all Wazuh-related Docker volumes
sudo docker volume ls | grep queue
# → local  single-node_wazuh_queue

# Enumerate all volumes with sizes
for vol in $(sudo docker volume ls -q | grep single-node); do
  echo -n "$vol: "
  sudo du -sh /var/lib/docker/volumes/$vol/_data 2>/dev/null || echo "0"
done
```

**Volume size breakdown (full enumeration):**

| Docker Volume                       | Size                       |
| ----------------------------------- | -------------------------- |
| single-node_wazuh_queue             | **24G** ← PRIMARY OFFENDER |
| single-node_wazuh_logs              | 25M                        |
| single-node_wazuh_etc               | 2.9M                       |
| single-node_wazuh_active_response   | 300K                       |
| single-node_wazuh_api_configuration | 140K                       |
| single-node_wazuh_wodles            | 416K                       |
| single-node_wazuh_agentless         | 64K                        |
| single-node_wazuh_integrations      | 80K                        |
| single-node_wazuh-dashboard-config  | 12K                        |
| single-node_wazuh-dashboard-custom  | 4K                         |
| single-node_wazuh_var_multigroups   | 4K                         |
| single-node_filebeat_etc            | 536K                       |
| single-node_filebeat_var            | 404K                       |

**The `wazuh_queue` volume was consuming 24GB** - nearly two-thirds of the entire 39GB volume. This was the event queue for Wazuh's manager service, which had accumulated a massive backlog of unprocessed events. OpenSearch indices were not the primary culprit; the queue was.

Confirming via `docker system df`:

```
TYPE            TOTAL   ACTIVE  SIZE        RECLAIMABLE
Images          3       0       4.502GB     4.502GB (100%)
Containers      0       0       0B          0B
Local Volumes   13      0       25.5GB      25.5GB (100%)
```

Docker images: `wazuh-dashboard:4.8.0` (1.17GB), `wazuh-indexer:4.8.0` (2.32GB), `wazuh-manager:4.8.0` (1.3GB).

### Phase 5 - Attempted Volume Removal (Insufficient)

```bash
# Locate indexer volume mount
sudo docker volume inspect single-node_wazuh-indexer-data 2>/dev/null | grep Mountpoint
# → "Mountpoint": "/var/lib/docker/volumes/single-node_wazuh-indexer-data/_data"

sudo du -sh /var/lib/docker/volumes/single-node_wazuh-indexer-data/
# → 20M

# Take stack down and remove indexer volume
sudo docker-compose down
sudo docker volume rm single-node_wazuh-indexer-data
```

**Result:**

```
df -h /
/dev/mapper/ubuntu--vg-ubuntu--lv  39G  38G  0  100%
```

**Still 100% full.** Removing the 20MB indexer volume made no meaningful difference. The 24GB `wazuh_queue` volume was still present and still consuming disk. This is the point where it became clear that no amount of cleaning existing data would solve this - the available storage was fundamentally undersized.

---

## 3. Root Cause Discovery

### Root Cause #1 - VMware Disk Provisioning Gap (Infrastructure)

At this stage, investigation shifted to the VM's disk configuration. The VMware virtual machine had been provisioned with an **80GB disk**, but the Linux LVM logical volume had never been extended to match. The physical volume on `/dev/sda3` reflected the full 80GB disk, but `lvextend` had never been run after the initial OS install - leaving the LV locked at its default ~39GB.

```bash
# Check physical volume
sudo pvresize /dev/sda3
# → Physical volume "/dev/sda3" changed
# → 1 physical volume(s) resized or updated / 0 physical volume(s) not resized

# Extend logical volume to use 100% of available free PE
sudo lvextend -l +100%FREE /dev/ubuntu-vg/ubuntu-lv
# → Size of logical volume ubuntu-vg/ubuntu-lv changed
#   from <39.00 GiB (9983 extents) to <78.00 GiB (19967 extents).
# → Logical volume ubuntu-vg/ubuntu-lv successfully resized.

# Expand filesystem to fill the new LV size (online, no unmount required)
sudo resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv
# → resize2fs 1.47.0 (5-Feb-2023)
# → Filesystem at /dev/mapper/ubuntu--vg-ubuntu--lv is mounted on /; on-line resizing required
# → The filesystem on /dev/mapper/ubuntu--vg-ubuntu--lv is now 20446208 (4k) blocks long.

df -h /
# → /dev/mapper/ubuntu--vg-ubuntu--lv  77G  34G  40G  46%
```

40GB of headroom recovered - without deleting a single file. The disk space was there the entire time; it just wasn't accessible to the filesystem.

### Root Cause #2 - Missing ISM Retention Policy (Configuration)

With the storage constraint resolved, the second root cause remained: no Wazuh ISM policy had been configured. Without one, the `wazuh_queue` volume and `wazuh-alerts-*` OpenSearch indices would grow unbounded again. The same failure would recur, just more slowly on the larger volume.

### Combined Root Cause Chain

```
VMware disk provisioned at 80GB
  └─ LVM LV never extended (default ~39GB allocated)
       └─ Effective usable storage: ~39GB

Wazuh deployed with no ISM retention policy
  └─ wazuh_queue volume accumulates event backlog
       └─ 24GB consumed within ~48 hours
            └─ 39GB LV exhausted → containers crash → SIEM offline
```

---

## 4. Containment & Recovery

### Step 1 - LVM Expansion (already completed above)

Volume expanded from 39GB → 77GB. 40GB headroom confirmed.

### Step 2 - Wazuh Stack Redeployment

```bash
cd ~/wazuh-docker/single-node
sudo docker-compose up -d
```

Docker pulled fresh Wazuh 4.8.0 images and created all three containers:

```
Pulling wazuh.manager  (wazuh/wazuh-manager:4.8.0)... done
Pulling wazuh.indexer  (wazuh/wazuh-indexer:4.8.0)... done
Pulling wazuh.dashboard (wazuh/wazuh-dashboard:4.8.0)... done

Creating single-node_wazuh.indexer_1   ... done
Creating single-node_wazuh.manager_1   ... done
Creating single-node_wazuh.dashboard_1 ... done
```

### Step 3 - Confirm Stack Health

From container logs, OpenSearch cluster health progressed as expected:

```
[wazuh.indexer] Cluster health status changed from [YELLOW] to [GREEN]
[wazuh.manager] IndexerConnector initialized successfully for index: wazuh-states-vulnerabilities
[wazuh.manager] Connection to backoff(elasticsearch(https://wazuh.indexer:9200)) established
[wazuh.manager] template with name 'wazuh' loaded
```

### Step 4 - Apply ISM Retention Policy

Navigated to OpenSearch Dashboard → `☰ → OpenSearch Plugins → Index Management → ISM Policies → Create Policy → JSON Editor`

```json
{
  "policy": {
    "description": "Wazuh 30-day retention",
    "default_state": "hot",
    "states": [
      {
        "name": "hot",
        "actions": [],
        "transitions": [
          {
            "state_name": "delete",
            "conditions": { "min_index_age": "30d" }
          }
        ]
      },
      {
        "name": "delete",
        "actions": [{ "delete": {} }],
        "transitions": []
      }
    ],
    "ism_template": [
      {
        "index_patterns": ["wazuh-alerts-*", "wazuh-archives-*"],
        "priority": 100
      }
    ]
  }
}
```

**Policy ID:** `retention` | **Confirmed via:** View JSON (`seqNo: 0`, `primaryTerm: 1`, `schema_version: 19`)

---

## 5. Full Incident Timeline

| Time (CDT)     | Event                                                                                                                 |
| -------------- | --------------------------------------------------------------------------------------------------------------------- |
| ~04/04/2026    | Wazuh deployed on os1 - no ISM policy; VM LV only ~39GB (VMware disk: 80GB, unextended)                               |
| ~04/04–05/2026 | `wazuh_queue` volume accumulates event backlog; indices grow unbounded                                                |
| 04/06 ~18:06   | `docker exec` → "no such container" - incident discovered; `docker-compose ps` → empty                                |
| 04/06 ~18:06   | `df -h /` → **39G 38G 0 100%** - disk COMPLETELY FULL                                                                 |
| 04/06 ~18:07   | `docker system prune` → 4.502GB reclaimed; df → 39G 34G 2.9G 93% - still critical                                     |
| 04/06 ~18:08   | `journalctl --vacuum-size` → freed 639.4MB; `apt-get clean` → marginal gains                                          |
| 04/06 ~18:09   | Stopped Docker; deleted `/var/lib/docker/overlay2` (8.0K, effectively empty); restarted Docker - no meaningful impact |
| 04/06 ~18:12   | Installed `ncdu`; disk visualization confirms `/var = 27.4 GiB` dominant consumer                                     |
| 04/06 ~18:14   | Docker volume enumeration: **`single-node_wazuh_queue` = 24G** - primary offender identified                          |
| 04/06 ~18:15   | `docker volume inspect single-node_wazuh-indexer-data` → only **20M**                                                 |
| 04/06 ~18:16   | `docker-compose down`; `docker volume rm single-node_wazuh-indexer-data`; df → still 100%                             |
| 04/06 ~18:18   | **Root cause #2 discovered**: VMware disk 80GB, LVM LV only ~39GB - half the disk unallocated                         |
| 04/06 ~18:19   | `pvresize /dev/sda3` → PV resized; `lvextend -l +100%FREE` → LV: 39GB → 78GB                                          |
| 04/06 ~18:20   | `resize2fs /dev/mapper/ubuntu--vg-ubuntu--lv` → filesystem expanded online                                            |
| 04/06 ~18:20   | `df -h /` → **77G 34G 40G 46%** - 40GB headroom restored                                                              |
| 04/06 ~18:23   | `docker-compose up -d` → pulled Wazuh 4.8.0; all 3 containers created                                                 |
| 04/06 ~18:30   | Cluster health confirmed GREEN; manager-indexer connection established                                                |
| 04/06 ~18:31   | ISM retention policy `retention` created → 30d delete on wazuh-alerts-_ / wazuh-archives-_                            |
| 04/06 ~18:31   | Policy confirmed via View JSON; incident closed                                                                       |

---

## 6. Post-Incident Analysis

### Impact Assessment

| CIA Triad           | Impact                | Notes                                                                                                              |
| ------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------------ |
| **Confidentiality** | None                  | No data exposed                                                                                                    |
| **Integrity**       | None                  | No data modified                                                                                                   |
| **Availability**    | **Yes - Full outage** | SIEM completely offline; monitoring blind spot for ~2+ days of effective queue buildup plus active outage duration |

**Severity Note:** In a production SOC environment, this would be classified **High** - a SIEM going dark creates an undetected attack window. An adversary with knowledge of this gap could operate freely for the duration of the outage without generating any alerting.

### What Went Right

- Systematic diagnostic approach - did not just blindly restart
- Used multiple tools to narrow down the actual consumer (ncdu → du → docker volume inspection)
- Identified the LVM under-allocation, which was a deeper infrastructure problem that would have recurred
- Applied both a structural fix (LV expansion) and a policy fix (ISM retention) - not just the quick patch
- Full documentation captured during the session

### What Went Wrong

- **VM provisioning was never verified post-deployment** - the LV/disk mismatch should have been caught at setup time
- **No ISM retention policy at deployment** - this is documented as a required post-install step in Wazuh's operational guidance
- **No disk utilization monitoring** - there were no alerts configured for disk saturation or container health
- **No deployment checklist** - both gaps (LVM and ISM) are preventable at setup time with a documented runbook
- **No external SIEM watchdog** - the monitoring system cannot alert on its own outage

### CVSS Scoring (Internal Reference)

```
Attack Vector:           Local          (AV:L)
Attack Complexity:       Low            (AC:L)
Privileges Required:     High           (PR:H)
User Interaction:        None           (UI:N)
Scope:                   Unchanged      (S:U)
Confidentiality Impact:  None           (C:N)
Integrity Impact:        None           (I:N)
Availability Impact:     High           (A:H)

CVSS v3.1 Base Score: 4.4 (MEDIUM)

Applies to the configuration gap that caused the outage.
Not eligible for CVE submission.
```

---

## 7. Recommendations

### Immediate Actions Completed

- [x] LVM logical volume extended: 39GB → 77GB
- [x] Wazuh stack redeployed on Wazuh 4.8.0
- [x] ISM 30-day retention policy applied to wazuh-alerts-_ and wazuh-archives-_
- [x] Policy confirmed active via OpenSearch Dashboard

### Short-Term (Next 7 Days)

**Monitor daily ingest rate** - need 48–72 hours of clean operation to calculate burn rate:

```bash
curl -k -u admin:SecretPassword   "https://localhost:9200/_cat/indices/wazuh-alerts-*?v&h=index,docs.count,store.size&s=index"
```

**Wazuh queue monitoring** - the 24GB queue buildup suggests the manager had a processing backlog. After the fresh deployment, watch queue volume size:

```bash
sudo du -sh /var/lib/docker/volumes/single-node_wazuh_queue/_data
```

If it's growing rapidly again, the event ingestion rate may exceed what the manager can process - which warrants investigating Wazuh's `queue.alerts.warn` and `queue.alerts.overflow` configuration.

**Disk threshold alert** (cron, runs every 15 minutes):

```bash
*/15 * * * * df / | awk 'NR==2 {gsub(/%/,"",$5); if ($5+0 > 75)   print "DISK WARN: "$5"% used on root volume"}' | mail -s "os1 Disk Alert" admin@localhost
```

**Container health watchdog**:

```bash
*/5 * * * * for c in wazuh.indexer wazuh.manager wazuh.dashboard; do   docker inspect -f '{{.State.Running}}' single-node_${c}_1 2>/dev/null | grep -q true ||   echo "ALERT: $c is DOWN"; done
```

### Long-Term

1. **VM Provisioning Checklist:** After any VM deployment, verify that the LVM LV reflects the full provisioned disk size before installing workloads. One command:

   ```bash
   # Should show same size as VMware allocation
   sudo lvdisplay /dev/ubuntu-vg/ubuntu-lv | grep "LV Size"
   ```

2. **Wazuh Deployment Runbook:** Create a Day-1 checklist for any Wazuh deployment. Non-negotiable items: (1) verify LVM/disk allocation, (2) apply ISM retention policy, (3) configure disk alert, (4) configure container health check.

3. **Retention Window Tuning:** After calculating daily burn rate, adjust the 30-day window. Formula: `retention_days = (available_GB × 0.8) / daily_GB_rate`. At 77GB with ~10GB OS overhead and 24GB queue, effective available for indices ≈ 40GB. Tune accordingly.

4. **Independent Monitoring:** Deploy a lightweight external watchdog (Uptime Kuma, or a simple cron-based HTTP check) that monitors the Wazuh Dashboard at `https://100.81.156.19` from a separate system. A SIEM cannot alert on its own unavailability.

---

## 8. Incident Classification

| Field                      | Value                                                         |
| -------------------------- | ------------------------------------------------------------- |
| **Incident Type**          | Availability - Full Service Outage                            |
| **Root Cause 1**           | Infrastructure misconfiguration (VMware disk/LVM LV mismatch) |
| **Root Cause 2**           | Operational misconfiguration (missing ISM retention policy)   |
| **Primary Disk Consumer**  | `single-node_wazuh_queue` Docker volume (24GB)                |
| **Threat Actor**           | None - internal/operational                                   |
| **Data Impacted**          | None                                                          |
| **Detection Method**       | Manual                                                        |
| **MITRE ATT&CK Relevance** | N/A (no adversarial activity)                                 |
| **Resolution Time**        | ~2.5 hours (single session)                                   |
| **Recurrence Risk**        | Low (both root causes addressed)                              |

---

_Report authored by: Ryan Duckworth | April 6, 2026_  
_Environment: Personal Home Lab - aspida-security project_
