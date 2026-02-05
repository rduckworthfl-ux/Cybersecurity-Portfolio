# Set Pattern

**When to use:** Problems requiring membership testing, uniqueness checks, or simple existence validation (no associated values needed).

**Core insight:** Sets provide O(1) lookups for "does this exist?" questions without the overhead of storing key-value pairs.

---

## Pattern Recognition Signals

- "Check if... appears at least twice"
- "Find all unique..."
- "Remove duplicates..."
- "Does this exist in...?"
- "Intersection/union of..."

**Key difference from Hash Maps:**

- **Set:** Just stores VALUES → `{1, 2, 3}`
- **Dict:** Stores KEY-VALUE pairs → `{1: 'a', 2: 'b', 3: 'c'}`

**Use Set when:** You only need to check "is this present?" (yes/no)  
**Use Dict when:** You need to retrieve associated data (index, count, metadata)

---

## Problems in This Category

1. **[Contains Duplicate](./contains-duplicate/)** - Check if any value appears twice (7ms, beats 89.35%)
2. **Valid Anagram** (coming soon) - Uses dict for counting, not set (different pattern)
3. **Intersection of Two Arrays** (future) - Set operations

---

## Python Set Operations Cheat Sheet

```python
# Creating sets
s = set()           # Empty set
s = {1, 2, 3}       # Set with values
s = set()  # From list (removes duplicates) → {1, 2, 3}

# Adding/removing
s.add(4)            # Add element
s.remove(2)         # Remove (raises error if not found)
s.discard(2)        # Remove (silent if not found)

# Checking membership
if 3 in s:          # O(1) lookup
    print("Found")

# Set operations
a = {1, 2, 3}
b = {2, 3, 4}

a | b               # Union: {1, 2, 3, 4}
a & b               # Intersection: {2, 3}
a - b               # Difference: {1}
a ^ b               # Symmetric difference: {1, 4}

# Size
len(s)              # Number of elements

# Conversion
list(s)             # Set to list
set()      # List to set (deduplicates)
```

---

## Cybersecurity Applications

Sets are critical in security engineering for:

### **1. Blocklist/Allowlist Lookups**

```python
# Check if IP is blocked (O(1) instead of scanning list)
blocked_ips = set(['192.168.1.100', '10.0.0.5', ...])

if incoming_ip in blocked_ips:
    return "Access Denied"
```

### **2. Vulnerability Deduplication**

```python
# Remove duplicate CVEs across scans
seen_cves = set()
unique_vulns = []

for vuln in scan_results:
    if vuln.cve_id not in seen_cves:
        unique_vulns.append(vuln)
        seen_cves.add(vuln.cve_id)
```

### **3. IOC (Indicator of Compromise) Matching**

```python
# Check if observed domain is in threat intel feed
malicious_domains = set(load_threat_feed())

for dns_query in network_traffic:
    if dns_query.domain in malicious_domains:
        alert("Potential C2 communication detected")
```

### **4. Log Event Deduplication (SIEM)**

```python
# Filter duplicate security events
seen_events = set()

for event in event_stream:
    event_hash = hash(f"{event.timestamp}_{event.source}_{event.signature}")
    if event_hash not in seen_events:
        process_event(event)
        seen_events.add(event_hash)
```

**Why Sets matter at scale:** In Vappler, checking if a CVE exists in a set of 100,000 known vulnerabilities is O(1). Using a list would be O(n) = 100,000 comparisons. At 1000+ scans/day, that's the difference between real-time and system overload.

---

## Set vs Dict Decision Tree

**Ask yourself:**

1. **Do I need to retrieve associated data?**
   - **YES** → Use `dict` (e.g., `{cve_id: cvss_score}`)
   - **NO** → Continue to #2

2. **Do I only need to check existence?**
   - **YES** → Use `set` (e.g., `{blocked_ips}`)
   - **NO** → Continue to #3

3. **Do I need to maintain order?**
   - **YES** → Use `list` or `OrderedDict`
   - **NO** → Use `set` for uniqueness, `dict` for mapping

**Examples from LeetCode:**

- **Two Sum:** Need indices → `dict {num: index}`
- **Contains Duplicate:** Just need "seen before?" → `set {nums}`
- **Group Anagrams:** Need to group words → `dict {pattern: [words]}`

---

## Performance Characteristics

| Operation               | Set  | List           | Dict                                      |
| ----------------------- | ---- | -------------- | ----------------------------------------- |
| Check membership (`in`) | O(1) | O(n)           | O(1)                                      |
| Add element             | O(1) | O(1) amortized | O(1)                                      |
| Remove element          | O(1) | O(n)           | O(1)                                      |
| Space complexity        | O(n) | O(n)           | O(n)                                      |
| Ordered?                | No   | Yes            | No (dict is insertion-ordered in Py 3.7+) |
| Duplicates?             | No   | Yes            | No (keys)                                 |

**When set wins:** Membership testing, deduplication, set algebra (union/intersection)

---

## Common Pitfalls (Java → Python)

### **Wrong: Creating empty set**

```python
s = {}  # This is a DICT, not a set!
```

### **Right:**

```python
s = set()  # Empty set
s = {1, 2, 3}  # Set with values
```

---

### **Wrong: Trying to add duplicates**

```python
s = {1, 2, 3}
s.add(2)
print(s)  # Still {1, 2, 3} - silently ignores duplicate
```

### **Right: Understand sets auto-deduplicate**

```python
s = set()
s.add(1)
s.add(2)
s.add(3)
s.add(2)
print(s)  # {1, 2, 3} - duplicates removed
```

---

### **Wrong: Assuming sets are ordered**

```python
s = {3, 1, 2}
print(s)  # Might print {1, 2, 3} or any order - don't rely on it!
```

### **Right: Use sets when order doesn't matter**

```python
# Good: Checking if user has required permissions
required_perms = {'read', 'write'}
user_perms = {'read', 'write', 'admin'}

if required_perms.issubset(user_perms):
    print("Access granted")
```

---

## Related Patterns

- **Hash Maps** (`dict`) - When you need key-value associations
- **Two Pointers** - When you need to compare elements at different positions
- **Sliding Window** - When you need to track elements in a moving range (often uses set for uniqueness)

---

## Lessons from Contains Duplicate

**What I learned solving Contains Duplicate (beats 89.35%):**

1. **Sets are FASTER than dicts for pure membership testing** (no key-value overhead)
2. **Early return is critical** - exit as soon as duplicate found
3. **Set syntax is cleaner than Java's HashSet** - `num in seen` vs `seen.contains(num)`
4. **Empty set requires `set()`** - `{}` creates a dict (Java habit trap!)

**Real-world impact:** In Vappler's dashboard, switching from list-based duplicate checking to set-based reduced query time from 850ms → 120ms for 1000+ vulnerability findings.

---

**Author:** Ryan Duckworth  
**Contact:** rduckworth@aspidasecurity.io  
**Portfolio:** [aspidasecurity.io](https://aspidasecurity.io)

**Last Updated:** Feb 4, 2026  
**Problems Documented:** 1 (Contains Duplicate)

---
