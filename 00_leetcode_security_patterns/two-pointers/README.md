# Two Pointers Pattern

**When to use:** Problems on sequences where comparing or converging from both ends is more efficient than nested loops.

**Core insight:** Replace an O(n²) nested scan with two coordinated indices that together traverse the sequence in O(n).

---

## Pattern Recognition Signals

- "Find a pair in a sorted array that..."
- "Check if a string is symmetric / reads the same backwards"
- "Maximize or minimize a value between two positions"
- "Remove duplicates in-place"
- "Merge two sorted arrays"

---

## Problems in This Category

1. **[Valid Palindrome](./validPalindrome/)**  -  Symmetric string check with normalization

---

## Cybersecurity Applications

Two-pointer traversal appears throughout security analytics:

- **Input normalization:** Strip punctuation + lowercase before string comparison  -  O(1) space vs O(n) clean-first approach
- **DPI symmetric payload detection:** Reflection/amplification attacks generate palindromic payloads; two-pointer scan detects them in a single pass
- **CVSS pair threshold detection:** On a sorted CVE list, find vulnerability pairs whose combined score exceeds a risk threshold in O(n)  -  Vappler's prioritization engine
- **Log deduplication:** Compare normalized log fields from both ends to detect mirror-image duplicate events

**The security principle:** O(n) or better for anything processing live traffic. O(n²) brute force does not scale to SIEM event volumes.
