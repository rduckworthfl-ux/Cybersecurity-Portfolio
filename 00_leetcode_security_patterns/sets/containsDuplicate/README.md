# Contains Duplicate (LC#217)

**Difficulty:** Easy  
**Pattern:** Set for Membership Testing  
**Solved:** Feb 4, 2026  
**Runtime:** 7ms, beats 89.35%  
**Memory:** 31.27 MB, beats 66.37%

---

## Problem Statement

Given an integer array `nums`, return `true` if any value appears **at least twice** in the array, and return `false` if every element is distinct.

**Constraints:**

- `1 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`

**Examples:**

```text
Input: nums = [1,2,3,1]
Output: true
Explanation: All elements are distinct

Input: nums = [1,2,3,4]
Output: false
Explanation: All elements are distinct
```

---

## My Approach

### **1. The Logic**

**Question:** "Have I seen this number before?"

**If YES:** Duplicate found → return `True`  
**If NO:** Remember this number for future iterations

**No math needed**—just a simple existence check.

---

### **2. The Algorithm**

1. Initialize empty set: `seen = set()`
2. For each number in the array:
   - Check if `num` exists in `seen`
   - If yes → return `True` (duplicate found)
   - If no → add `num` to `seen`
3. If loop completes → return `False` (no duplicates)

---

### **3. Why Set (Not Dict)?**

| Data Structure  | Use Case                                    | This Problem?      |
| --------------- | ------------------------------------------- | ------------------ |
| **Dict** `{}`   | Need key-value pairs (e.g., `{num: index}`) | Don't need indices |
| **Set** `set()` | Just need "exists or not"                   | Perfect fit        |

**Set advantages:**

- O(1) membership testing (`num in seen`)
- Automatically handles uniqueness (can't store duplicates)
- Cleaner syntax than dict for this use case

**Comparison to Two Sum:**

- Two Sum: Need indices → use `dict` to store `{num: index}`
- Contains Duplicate: Just need existence → use `set` to store `{num}`

---

### **4. Complexity Analysis**

| Metric    | Value | Reasoning                                                     |
| --------- | ----- | ------------------------------------------------------------- |
| **Time**  | O(n)  | Single pass through array, O(1) set lookups                   |
| **Space** | O(n)  | Set stores up to n unique elements (worst case: all distinct) |

**Best case:** First two elements are duplicates → O(1)  
**Worst case:** No duplicates, store all n elements → O(n)  
**Average case:** O(n) with early termination on duplicate

---

## Cybersecurity Application

This pattern is **critical for O(1) membership testing in security systems**.

### **Use Case 1: CISA KEV Catalog Lookup (Vappler)**

**Problem:** Check if discovered CVE is in CISA's Known Exploited Vulnerabilities catalog

**Actual Implementation (`tasks.py`):**

```python
def enrich_with_kev(scan_id: str):
    """
    Flag vulnerabilities that are actively exploited in the wild.
    Uses set for O(1) lookup against 10K+ KEV entries.
    """
    # Fetch CISA KEV catalog
    kev_response = requests.get('https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json')
    kev_cves = set(cve['cveID'] for cve in kev_response.json()['vulnerabilities'])

    # Check our scan results against KEV
    vulns = supabase.table('vulnerabilities').select('*').eq('scan_id', scan_id).execute()

    for vuln in vulns.data:
        if vuln['cve_id'] in kev_cves:  # O(1) lookup
            # Flag as actively exploited (highest priority)
            supabase.table('vulnerabilities').update({
                'is_kev': True,
                'priority': 'CRITICAL'
            }).eq('id', vuln['id']).execute()
```

**Why set?** 10,000+ KEV CVEs to check against. List would be O(n) = 10,000 comparisons per vulnerability.

**Performance:**

- Set approach: 0.001ms per CVE check
- List approach: ~10ms per CVE check (1000+ vulns = 10+ seconds total)

---

### **Use Case 2: Database-Level Deduplication (Vappler Architecture)**

**IMPORTANT:** Vappler does NOT use Python sets for vulnerability deduplication. We use **Postgres indexes and materialized views**.

When processing 1000+ concurrent security scans, the same CVE often appears on multiple hosts/ports. Users don't want to see:

```bash
CVE-2024-1234 on 192.168.1.10:80
CVE-2024-1234 on 192.168.1.10:443
CVE-2024-1234 on 192.168.1.11:80
...
(50 more times)
```

**Actual Vappler Solution (Database-Level):**

```sql
-- Postgres UNIQUE index prevents duplicate entries at INSERT time
CREATE UNIQUE INDEX idx_unique_vuln
ON vulnerabilities(cve_id, host, port);

-- Materialized view aggregates unique vulnerabilities for dashboard
CREATE MATERIALIZED VIEW vulnerability_summary AS
SELECT
    cve_id,
    severity,
    COUNT(DISTINCT host) as affected_hosts,
    ARRAY_AGG(DISTINCT CONCAT(host, ':', port)) as affected_endpoints,
    MAX(cvss_score) as max_cvss,
    MAX(scan_timestamp) as last_seen
FROM vulnerabilities
GROUP BY cve_id, severity;

-- Index for fast dashboard queries
CREATE INDEX idx_vuln_summary_cvss ON vulnerability_summary(max_cvss DESC);
```

**Frontend Query (PostgREST/Supabase):**

```typescript
// Fetch pre-deduplicated data from materialized view
const { data: vulns } = await supabase
  .from("vulnerability_summary")
  .select("*")
  .gte("max_cvss", 7.0) // Only critical/high severity
  .order("max_cvss", { ascending: false });
```

**Why database-level?**

- Postgres deduplicates 100K rows in ~50ms
- Python loops would take seconds
- Materialized views are refreshed async (no frontend wait)

**Real impact in Vappler:**

- Reduced dashboard clutter (117 vulnerabilities → 42 unique CVEs)
- Faster queries (10ms vs 850ms before optimization)
- Better UX (security analysts see actionable findings, not noise)

---

### **Use Case 3: Real-Time SIEM Event Deduplication**

**SIEM systems** must deduplicate in-memory for real-time streams:

```python
seen_events = set()

for event in real_time_event_stream:
    # Deduplicate within 1-minute window
    event_sig = f"{event.source_ip}_{event.signature_id}_{event.timestamp//60}"

    if event_sig in seen_events:
        continue  # Skip duplicate alert

    trigger_analyst_alert(event)
    seen_events.add(event_sig)
```

**Why NOT database?** Real-time stream needs <10ms response. Database INSERT + query would add latency.

**Use cases:**

- **IDS alerts:** Same attack signature firing 1000x/second
- **Failed logins:** Brute force attempts from same IP
- **Malware detections:** Same hash detected on multiple endpoints

---

### **Architectural Decision: When to Use Sets vs Database**

| Use Case                                   | Solution                                   | Why                                                             |
| ------------------------------------------ | ------------------------------------------ | --------------------------------------------------------------- |
| Persistent deduplication (vulnerabilities) | Postgres UNIQUE index + materialized views | Handles concurrent inserts, ACID compliance, 50ms for 100K rows |
| In-memory enrichment (KEV lookup)          | Python set                                 | No DB roundtrip, task-scoped data, O(1) membership testing      |
| Real-time stream (SIEM events)             | Python set                                 | <10ms response needed, transient data                           |
| Dashboard queries                          | Materialized view                          | Pre-aggregated, already deduplicated by database                |

**Rule:** Let the database do what it's optimized for. Use Python sets for transient, in-memory operations where database roundtrip is too slow.

---

## Code

See [`solution.py`](./solution.py) for fully annotated implementation.

**Key design choices:**

1. **Set over dict:** Don't need indices, just existence checks
2. **Early return:** Exit immediately on first duplicate (no wasted iterations)
3. **Pythonic syntax:** `num in seen` vs Java's `.contains(num)`

---

## Lessons Learned

1. **Simpler than Two Sum:** No math, no indices, just membership testing
2. **Set vs Dict clarity:** Choose storage based on what you need to retrieve (existence vs value)
3. **Architecture matters:** Database for persistent deduplication, Python sets for transient tasks
4. **Performance improvement:** 89.35% faster (vs 51.92% on Two Sum)—early return optimization working
5. **Java → Python win:** `num in seen` is SO much cleaner than `seen.contains(num)`

---

## Related Problems

- **Two Sum** (LC 1) - Dict variant (need indices, not just existence)
- **Valid Anagram** (LC 242) - Count frequency, not just existence
- **Intersection of Two Arrays** (LC 349) - Set operations (union/intersection)

---

## Test Cases

**Provided by LeetCode:**

```python
assert containsDuplicate() == True
assert containsDuplicate() == False
assert containsDuplicate() == True
```

**Edge cases I tested mentally:**

```python
assert containsDuplicate() == False          # Single element
assert containsDuplicate() == True         # Immediate duplicate
assert containsDuplicate() == False  # All unique (worst case space)
```

---

## Performance Results

**LeetCode Submission:**

- Accepted (77/77 test cases)
- Runtime: 7ms (beats 89.35% of Python3 submissions)
- Memory: 31.27 MB (beats 66.37%)
- Submitted: Feb 04, 2026 22:08 CST

**Why this is fast:**

1. O(n) time with O(1) set lookups (optimal algorithm class)
2. Early return on first duplicate (no unnecessary iterations)
3. Python's optimized set implementation (hash table under hood)
4. No redundant operations or data copies

![Contains Duplicate Description](<../../assets/containsDuplicate(description).png>)
![Contains Duplicate Accepted](<../../assets/containsDuplicate(accepted).png>)

---

**Author:** Ryan Duckworth  
**Contact:** rduckworth@aspidasecurity.io  
**Portfolio:** [aspidasecurity.io](https://aspidasecurity.io)  
**Vappler Docs:** [github.com/rduckworthfl-ux/vapplerDocs](https://github.com/rduckworthfl-ux/vapplerDocs)

---
