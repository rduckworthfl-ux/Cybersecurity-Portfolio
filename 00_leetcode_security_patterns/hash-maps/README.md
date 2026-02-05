# Hash Map Pattern

**When to use:** Problems requiring fast lookups, counting, or checking existence.

**Core insight:** Sacrifice O(n) space to achieve O(1) lookup time.

---

## Pattern Recognition Signals

- "Find a pair that..."
- "Check if... exists"
- "Count occurrences of..."
- "Group items by..."

---

## Problems in This Category

1. **[Two Sum](./two-sum/)** - Find pair summing to target
2. **[Contains Duplicate](./contains-duplicate/)** - Check if value appears twice (uses Set variant)
3. **Valid Anagram** (coming soon) - Count character frequencies

---

## Cybersecurity Applications

Hash maps power:

- **Threat intelligence lookups:** Check if IP/domain is in blocklist (O(1) vs scanning entire list)
- **Log deduplication:** Filter duplicate security events by hashing event signatures
- **CVE correlation:** Map vulnerability IDs to CVSS scores for instant risk calculation

In Vappler, I use Redis (in-memory hash map) to cache:

- Vulnerability metadata from NVD/CISA APIs
- Scan results for dashboard queries
- User session tokens

**Same data structure, production scale.**

---
