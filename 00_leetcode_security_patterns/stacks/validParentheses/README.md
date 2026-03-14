# Valid Parentheses (LeetCode #20)

**Difficulty:** Easy  
**Pattern:** Stack — Last In, First Out (LIFO) Bracket Matching  
**Solved:** March 14, 2026  
**Runtime:** 3ms (beats 34.55%)  
**Memory:** 19.32MB (beats 59.78%)

---

## Problem Statement

Given a string `s` containing only the characters `(`, `)`, `{`, `}`, `[`, and `]`, determine if the input string is valid.

**Valid rules:**

- Open brackets must be closed by the same type of bracket
- Open brackets must be closed in the correct order
- Every close bracket must have a corresponding open bracket

---

## My Approach

### **1. The Insight**

```text
The most recently opened bracket must be the next one closed.
→ This is a LIFO (Last In, First Out) relationship → Stack
```

### **2. The Algorithm**

1. Initialize empty stack
2. Build mapping: `{closing: opening}` — e.g. `')': '('`
3. For each character:
   - If closing bracket → pop stack, verify it matches `mapping[char]`
   - If opening bracket → push onto stack
4. Return `len(stack) == 0` (all openers matched)

### **3. Why Stack?**

**Naive approach:** Repeatedly scan and remove matched pairs → O(n²)  
**Optimized:** Push/pop in a single pass → O(n) time, O(n) space

**The sentinel trick:** Use `'#'` as a default pop value when the stack is empty — avoids IndexError and cleanly handles mismatched closers at the start.

---

## Cybersecurity Application

Stack-based validation is one of the most deployed algorithms in security tooling.

### **Use Case: Nmap XML Validation in Vappler**

```python
def validate_nmap_xml_structure(xml_string: str) -> bool:
    """
    Before parsing Nmap scan output into CVE records, verify the
    XML bracket structure is intact. Truncated or corrupted XML
    from a crashed scan worker can contain malformed tags that
    corrupt the vulnerability database if parsed blindly.

    This O(n) pre-check runs before any XML deserialization.
    Malformed structure → reject → re-queue scan → prevent DB corruption.
    """
    stack = []
    mapping = {'>': '<', ')': '(', ']': '[', '}': '{'}
    for char in xml_string:
        if char in mapping:
            top = stack.pop() if stack else '#'
            if top != mapping[char]:
                return False
        elif char in '<([{':
            stack.append(char)
    return len(stack) == 0
```

### **Why This Matters in Security**

**Parsers trust structure.** XML, JSON, and SQL parsers assume well-formed input. An attacker who can send malformed-but-parseable input can:

- Cause unexpected deserialization behavior (XXE, object injection)
- Bypass WAF rules that expect canonical bracket structure
- Crash parser threads and cause DoS

A stack pre-filter costs O(n) and provides a structural guarantee before any complex parsing logic runs.

In Vappler, this pattern enables:

- Pre-validation of Nmap XML before Celery worker deserialization
- API request pre-filtering in Flask endpoints (unmatched `{` in JSON body = reject)
- YARA rule syntax validation before compilation and agent deployment

---

## Code

See [`solution.py`](./solution.py) for fully annotated implementation.

**Key highlights:**

- Mapping stores `closing → opening` (not the reverse) for clean O(1) lookup
- Sentinel `'#'` prevents IndexError on empty-stack pop
- Final `len(stack) == 0` elegantly handles unclosed openers

---

## Complexity Analysis

| Metric    | Value | Reasoning                             |
| --------- | ----- | ------------------------------------- |
| **Time**  | O(n)  | Single pass through string            |
| **Space** | O(n)  | Stack holds at most n/2 open brackets |

**Best case:** First character is a closer with empty stack → O(1)  
**Worst case:** All openers, then all closers → O(n)  
**Average case:** O(n) single pass

---

## Lessons Learned

1. **Map closing to opening:** Allows direct `mapping[char]` lookup on close — cleaner than the reverse
2. **Sentinel value:** `stack.pop() if stack else '#'` — one line handles the empty stack edge case
3. **LIFO = Stack:** Any time the "most recent" item is what matters, reach for a stack
4. **len(stack) == 0:** Don't just check for `False` returns — unclosed openers must also fail

---

## Related Problems

- **Min Stack** (LC 155) — Stack with O(1) minimum tracking
- **Daily Temperatures** (LC 739) — Monotonic stack pattern
- **Evaluate Reverse Polish Notation** (LC 150) — Stack for expression parsing

---

**Runtime Proof:**  
![Valid Parentheses Accepted](<../../assets/validParenthesis(accepted).png>)  
_3ms runtime, beats 34.55% | 19.32MB memory, beats 59.78%_

---

**Author:** Ryan Duckworth  
**Contact:** rduckworth@aspidasecurity.io  
**Portfolio:** [rduckworthfl-ux](https://github.com/rduckworthfl-ux)  
**Website:** [aspidasecurity.io](https://aspidasecurity.io)
