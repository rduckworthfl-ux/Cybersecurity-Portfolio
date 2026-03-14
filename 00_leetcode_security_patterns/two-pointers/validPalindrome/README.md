# Valid Palindrome (LeetCode #125)

**Difficulty:** Easy  
**Pattern:** Two Pointers — Inward Scan with Normalization  
**Solved:** March 14, 2026  
**Runtime:** 9ms (beats 43.14%)  
**Memory:** 19.57MB (beats 91.14%)

---

## Problem Statement

A phrase is a palindrome if, after converting all uppercase letters to lowercase and removing all non-alphanumeric characters, it reads the same forward and backward.

Given a string `s`, return `true` if it is a palindrome, or `false` otherwise.

---

## My Approach

### **1. The Insight**

```text
A palindrome is symmetric → check from the outside in
→ Use two pointers starting at opposite ends, moving inward
→ Skip non-alphanumeric characters (they don't count)
→ Compare case-insensitively
```

### **2. The Algorithm**

1. Initialize `left = 0`, `right = len(s) - 1`
2. While `left < right`:
   - Skip non-alphanumeric from the left
   - Skip non-alphanumeric from the right
   - Compare `s[left].lower()` vs `s[right].lower()`
   - Mismatch → return `False`
   - Match → move both pointers inward
3. Return `True`

### **3. Why Two Pointers?**

**Clean-then-check approach:** Strip string first, then compare halves → O(n) time but O(n) extra space  
**Optimized:** Skip in-place with two pointers → O(n) time, **O(1) space**

**No new string allocated.** The pointers navigate the original string directly.

---

## Cybersecurity Application

Two-pointer inward scanning powers input validation and symmetric pattern detection.

### **Use Case: Input Sanitization Validation**

```python
def is_normalized_palindrome(raw_input: str) -> bool:
    """
    Before storing user-supplied strings (asset names, scan target labels),
    Vappler normalizes input by stripping non-alphanumeric characters and
    lowercasing — the same transformation used here.

    This also validates that special-character padding (a common injection
    technique) does not create asymmetric inputs that bypass downstream
    string equality checks.

    Example attack attempt:
    Input: "'; DROP TABLE assets; --"
    After normalization: "droptableassets"
    → Non-palindrome AND contains known SQL keyword pattern
    → Flag for inspection before DB layer
    """
    left, right = 0, len(raw_input) - 1
    while left < right:
        while left < right and not raw_input[left].isalnum():
            left += 1
        while left < right and not raw_input[right].isalnum():
            right -= 1
        if raw_input[left].lower() != raw_input[right].lower():
            return False
        left += 1
        right -= 1
    return True
```

### **Why This Matters in Security**

**Input normalization is a security primitive.** Before any string reaches a parser, database, or comparison engine, it must be normalized consistently.

The two-pointer technique applies directly to:

- **Log field normalization:** SIEM parsers strip punctuation/casing before correlation — identical transformation, run on millions of events/second
- **DPI palindrome detection:** Reflection attacks generate symmetric packet payloads; two-pointer scanning detects them in O(n) without buffering
- **CVSS sorted-array traversal:** Two pointers on a sorted vulnerability list find pairs exceeding a combined risk threshold in O(n) — used in Vappler's prioritization engine

In Vappler, this pattern enables:

- Asset name normalization before database storage (prevents encoding-based injection)
- Binary search on sorted CVSS arrays for risk threshold pair detection
- Efficient string comparison in the KEV correlation pipeline

---

## Code

See [`solution.py`](./solution.py) for fully annotated implementation.

**Key highlights:**

- Inner `while` loops skip non-alphanumeric in-place — no extra string allocation
- `.isalnum()` handles both letters and digits cleanly
- `.lower()` applied only at comparison — not to the whole string upfront

---

## Complexity Analysis

| Metric    | Value | Reasoning                                           |
| --------- | ----- | --------------------------------------------------- |
| **Time**  | O(n)  | Each character visited at most once                 |
| **Space** | O(1)  | Only two integer pointers — no new string allocated |

**Best case:** First vs last character mismatch → O(1)  
**Worst case:** Full valid palindrome → O(n) scan  
**Average case:** O(n) with early termination on mismatch

---

## Lessons Learned

1. **O(1) space matters:** Creating a cleaned string first works but costs O(n) memory — pointers avoid it
2. **Nested while loops:** The inner skips are still O(n) total across the whole run — not O(n²)
3. **`.isalnum()` is your friend:** Built-in Python method handles all alphanumeric in one call
4. **Two pointers generalize:** This same pattern solves container-with-most-water, sorted-pair-sum, and more

---

## Related Problems

- **Two Sum II — Input Array Is Sorted** (LC 167) — Two pointers on sorted array
- **Container With Most Water** (LC 11) — Two pointers maximize area
- **3Sum** (LC 15) — Two pointers inside a loop for triplet detection

---

**Runtime Proof:**  
![Valid Palindrome Accepted](<../../assets/validPalindrome(accepted).png>)  
_9ms runtime, beats 43.14% | 19.57MB memory, beats 91.14%_

---

**Author:** Ryan Duckworth  
**Contact:** rduckworth@aspidasecurity.io  
**Portfolio:** [rduckworthfl-ux](https://github.com/rduckworthfl-ux)  
**Website:** [aspidasecurity.io](https://aspidasecurity.io)
