# Valid Anagram (LeetCode #242)

**Difficulty:** Easy  
**Pattern:** Hash Map — Character Frequency Counting  
**Solved:** March 14, 2026  
**Runtime:** 11ms (beats 75.92%)  
**Memory:** 19.23MB (beats 98.50%)

---

## Problem Statement

Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise.

**Constraints:**

- `1 <= s.length, t.length <= 5 * 10⁴`
- `s` and `t` consist of lowercase English letters only

---

## My Approach

### **1. The Math**

```text
anagram: same characters, same frequencies, any order
→ build frequency map for s, decrement against t
→ any non-zero remainder = not an anagram
```

### **2. The Algorithm**

1. Early exit: if `len(s) != len(t)` → return `False`
2. Initialize empty dict: `count = {}`
3. Iterate `s` → increment `count[char]`
4. Iterate `t` → decrement `count[char]`
5. Check all values: if any `val != 0` → return `False`
6. Return `True`

### **3. Why Hash Map?**

**Sort approach:** Sort both strings → compare → O(n log n) time  
**Optimized:** Character frequency dict → O(1) lookup → O(n) total time

**Trade-off:** O(26) = O(1) space (lowercase letters only) to achieve O(n) time.

---

## Cybersecurity Application

This pattern is the backbone of string-based threat detection.

### **Use Case: Username Spoofing Detection**

```python
def detect_username_spoof(registered_users: list[str], new_username: str) -> bool:
    """
    Flag account registration if the new username is an anagram
    of any existing privileged account — a classic IAM attack vector.

    Example:
    - Existing: "admin"
    - Attempt:  "admni" → anagram → BLOCK

    Attackers use rearranged strings to impersonate admin/root accounts
    and bypass simple string equality checks.
    """
    count = {}
    for char in new_username:
        count[char] = count.get(char, 0) + 1

    for user in registered_users:
        if len(user) != len(new_username):
            continue
        check = count.copy()
        for char in user:
            check[char] = check.get(char, 0) - 1
        if all(v == 0 for v in check.values()):
            return True  # SPOOF DETECTED
    return False
```

### **Why This Matters in Security**

**Static malware analysis** uses character-frequency maps to detect obfuscated attack strings. Malware authors rearrange known signatures to evade AV engines that rely on exact string matching.

Frequency map approach catches:

- Rearranged attack payloads
- Permutation-based evasion in command injection
- SIEM field normalization mismatches

In Vappler, this pattern enables:

- Deduplication of CVE identifiers with minor encoding differences
- Validating Nmap XML tag pairs have consistent character sets
- Detecting anomalous API parameter names in incoming scan requests

---

## Code

See [`solution.py`](./solution.py) for fully annotated implementation.

**Key highlights:**

- Early-exit length check eliminates unnecessary work
- Single dict (not two) — decrement on second pass = elegant O(1) space
- Step-by-step comments explain WHY, not just WHAT

---

## Complexity Analysis

| Metric    | Value | Reasoning                             |
| --------- | ----- | ------------------------------------- |
| **Time**  | O(n)  | Two linear passes through each string |
| **Space** | O(1)  | At most 26 keys (lowercase alphabet)  |

**Best case:** Length mismatch detected immediately → O(1)  
**Worst case:** Full scan, last character mismatches → O(n)  
**Average case:** O(n) with early termination

---

## Lessons Learned

1. **Decrement, don't use two maps:** One dict with +1/-1 is cleaner and uses half the memory
2. **Early exit is free performance:** Length check costs O(1) and eliminates O(n) work
3. **O(1) space claim:** "Up to 26 keys" is a constant, not n — technically O(1) for bounded alphabets
4. **Extension:** For Unicode strings, this still works — just a larger but bounded key space

---

## Related Problems

- **Two Sum** (LC 1) — Hash map for O(1) complement lookup
- **Contains Duplicate** (LC 217) — Set variant (membership only)
- **Group Anagrams** (LC 49) — Hash map with sorted string as key

---

**Runtime Proof:**  
![Valid Anagram Accepted](<../../assets/validAnagram(accepted).png>)  
_11ms runtime, beats 75.92% | 19.23MB memory, beats 98.50%_

---

**Author:** Ryan Duckworth  
**Contact:** rduckworth@aspidasecurity.io  
**Portfolio:** [rduckworthfl-ux](https://github.com/rduckworthfl-ux)  
**Website:** [aspidasecurity.io](https://aspidasecurity.io)
