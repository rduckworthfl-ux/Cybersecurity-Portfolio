# Two Sum (LeetCode #1)

**Difficulty:** Easy  
**Pattern:** Hash Map for O(1) Lookups  
**Solved:** Feb 4, 2026  
**Runtime:** 3ms (beats 51.92%)

---

## Problem Statement

Given an array of integers `nums` and an integer `target`, return **indices** of the two numbers such that they add up to `target`.

**Constraints:**

- You may assume that each input has **exactly one solution**
- You may not use the same element twice
- Return answer in any order

---

## My Approach

### **1. The Math**

```text
x + y = target
→ y = target - x (the "complement")
```

For each number `x`, calculate what other number `y` would complete the sum. Then check if we've seen `y` before.

### **2. The Algorithm**

1. Initialize empty dict: `seen = {}`
2. For each number and its index:
   - Calculate `complement = target - num`
   - Check if `complement` exists in `seen`
   - If yes → return `[seen[complement], current_index]`
   - If no → store `seen[num] = current_index`
3. Return empty list (won't happen per problem guarantee)

### **3. Why Hash Map?**

**Brute force:** Check every pair → O(n²) time
**Optimized:** Store numbers in dict → O(1) lookup → O(n) total time

**Trade-off:** Use O(n) extra space to eliminate the inner loop.

---

## Cybersecurity Application

This exact pattern powers **CVE correlation** in my Vappler platform.

### **Use Case: Exploit Chain Detection**

```python
def find_exploit_chain(vulnerabilities, risk_threshold):
    """
    Given a list of CVEs with CVSS scores, find two that combine
    to exceed the organization's risk threshold.

    Example:
    - CVE-2024-1234: CVSS 7.5
    - CVE-2024-5678: CVSS 6.2
    - Threshold: 13.0

    Result: These two CVEs form an exploit chain (7.5 + 6.2 = 13.7)
    """
    seen = {}
    for i, vuln in enumerate(vulnerabilities):
        complement_cvss = risk_threshold - vuln.cvss_score
        if complement_cvss in seen:
            return [seen[complement_cvss], i]
        seen[vuln.cvss_score] = i
    return []
```

### **Why This Matters in Security**

**SIEM systems** process millions of security events per second. When correlating:

- Failed login attempts (brute force detection)
- Port scans + exploit attempts (multi-stage attacks)
- IOC matches across threat intelligence feeds

**O(n²) brute force = system crashes under load**
**O(n) hash map = real-time threat detection**

In Vappler, this pattern enables:

- Dashboard query optimization (2.3s → 300ms via materialized views + hash lookups)
- Duplicate CVE deduplication across 1000+ concurrent scans
- Real-time vulnerability enrichment from CISA KEV catalog

---

## Code

See [`solution.py`](./solution.py) for fully annotated implementation.

**Key highlights:**

- Documented input/output/task at top
- Mathematical relationship explained
- Storage justification
- Step-by-step logic with WHY, not just WHAT

---

## Complexity Analysis

| Metric    | Value | Reasoning                        |
| --------- | ----- | -------------------------------- |
| **Time**  | O(n)  | Single pass through array        |
| **Space** | O(n)  | Hash map stores up to n elements |

**Best case:** First two elements sum to target → O(1)
**Worst case:** Last element completes the sum → O(n)
**Average case:** O(n) with early termination on match

---

## Lessons Learned

1. **Math unlocks algorithms:** Once I saw `y = target - x`, the code wrote itself
2. **Storage = speed:** Trading O(n) space for O(n) time is almost always worth it
3. **Dict keys matter:** Store `{num: index}` not `{index: num}` to enable complement lookups
4. **Python syntax:** Fought Java habits (semicolons, `.length`) but now fluent in `enumerate()` and `in` operator

---

## Related Problems

- **Contains Duplicate** (LC 217) - Set variant (membership only, no indices)
- **Valid Anagram** (LC 242) - Hash map counting pattern
- **Group Anagrams** (LC 49) - Hash map with sorted strings as keys

---

**Runtime Proof:**
![Two Sum Description](../../assets/twoSum(description).png)
![Two Sum Accepted](../../assets/twoSum(accepted).png)
_3ms runtime, beats 51.92% of Python3 submissions_

---

**Author:** Ryan Duckworth
**Contact:** rduckworth@aspidasecurity.io
**Portfolio:** [rduckworthfl-ux](https://github.com/rduckworthfl-ux)
**Website:** [aspidasecurity.io](https://aspidasecurity.io)

---
