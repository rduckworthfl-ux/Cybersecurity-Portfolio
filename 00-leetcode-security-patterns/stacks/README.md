# Stack Pattern

**When to use:** Problems where the most recently added item is the next one needed.

**Core insight:** LIFO (Last In, First Out)  -  the stack processes items in reverse order of insertion. Any problem where "undo," "nesting," or "match the most recent" is required is a stack problem.

---

## Pattern Recognition Signals

- "Valid / matching brackets or tags"
- "Most recent... must match the next..."
- "Undo / backtrack the last action"
- "Evaluate expressions with precedence"
- "Next greater / smaller element"

---

## Problems in This Category

1. **[Valid Parentheses](./validParentheses/)**  -  Match nested bracket pairs

---

## Cybersecurity Applications

Stacks power structural validation across the entire security stack:

- **XML/JSON pre-validation:** Reject malformed payloads before parser deserialization (prevents XXE, object injection)
- **Nmap XML parsing:** Vappler uses stack validation before ingesting scan output into the CVE database
- **SQL injection pre-filter:** Unmatched parentheses in query params = injection signal
- **YARA rule compilation:** Validate bracket structure in threat detection rules before agent deployment
- **Call stack analysis:** Malware sandbox tracers use stacks to track execution depth and detect stack-smashing exploits

**The security principle:** Never let a parser see structurally invalid input. Validate structure first  -  O(n) stack check before O(n²) parsing logic.
```

***