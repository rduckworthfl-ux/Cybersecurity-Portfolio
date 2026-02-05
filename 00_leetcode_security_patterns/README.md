# LeetCode for Cybersecurity: Algorithmic Patterns in Threat Detection

**Author:** Ryan Duckworth  
**Context:** IBM Entry-Level AI Software Engineer Interview Prep  
**Date:** February 4, 2026  
**Portfolio:** [github.com/rduckworthfl-ux](https://github.com/rduckworthfl-ux)
**Website:** [Vappler](https://aspidasecurity.io)

---

## Executive Summary

When I started prepping for technical interviews, I realized something: **the same algorithmic patterns tested in LeetCode are the EXACT patterns I use daily in cybersecurity engineering.**

I built Vappler; a multi-tenant SaaS vulnerability management platform processing 1000+ concurrent security scans; using these exact data structures. Hash maps for CVE lookups. Sets for deduplication. Stacks for processing nested exploit chains. I was already DOING this in production; I just hadn't formalized the computer science theory behind it.

This repository documents my thought process as I:

1. **Decode interview problems** using first-principles mathematical reasoning
2. **Map abstract algorithms** to real-world security use cases
3. **Write production-quality code** with cybersecurity context embedded

I don't memorize solutions. I derive them from requirements, the same way I architect backend systems under pressure. Every solution here includes:

- The **mathematical relationship** I identified (e.g., `x + y = target → complement = target - x`)
- The **cybersecurity application** (how this pattern appears in SIEM, threat intel, or vuln management)
- The **step-by-step reasoning** that got me from problem statement to optimized code

**Why this matters for security engineering:** Processing millions of security events requires O(n) algorithms, not O(n²) brute force. The difference between a hash map lookup (O(1)) and a nested loop (O(n²)) is the difference between real-time threat detection and a system that crashes under load.

I learned this the hard way debugging Vappler's scan engine. Now I'm proving I can apply the same optimization mindset to any algorithmic challenge.

---

## My Learning Framework (Derived Feb 4, 2026)

After struggling with Two Sum for 4 hours, I cracked the code. Here's the exact 5-step process I now use for EVERY problem:

### **Step 1: Understand the Problem**

- Read 3 times: What's the input? Output? Constraints?
- Solve it manually with paper/pen
- **Key question:** "Can I explain this to a non-technical stakeholder?"

### **Step 2: Find the Math**

- Every algorithm has a core mathematical relationship
- **Example (Two Sum):** `x + y = target` → solve for `y = target - x`
- This is my unlock;I've always been good at math, and finding the algebra makes the code obvious

### **Step 3: Identify the Bottleneck**

- Write the brute force solution first (proves I understand the problem)
- **Ask:** "What's making this slow?"
- **Answer:** Usually nested loops → can I use a hash map to eliminate inner loop?

### **Step 4: Choose the Right Data Structure**

- Need fast lookups? → **Dict** (hash map)
- Need membership testing? → **Set**
- Need LIFO ordering? → **Stack** (list with append/pop)
- **Cybersecurity parallel:** Same decision I make choosing Redis vs PostgreSQL for Vappler's cache layer

### **Step 5: Translate to Code**

- Map each logical step to Python syntax
- **Pattern:** Storage initialization → Iteration → Check → Store/Return
- Document the WHY, not just the WHAT

**This framework came from my Vappler debugging process:**  
Understand failure → Find root cause (the "math") → Identify bottleneck → Pick the right tool → Implement fix

Same process. Different domain.

---

## Problems Solved (With Security Context)

### **1. Two Sum (LC 1) - Hash Map for Threat Correlation**

**Problem:** Given an array of integers and a target, return indices of two numbers that sum to target.

**My Approach:**

- **Math:** `x + y = target` → `complement = target - num`
- **Storage:** Dict to store `{number: index}` for O(1) lookups
- **Complexity:** O(n) time, O(n) space

**Cybersecurity Application:**
In Vappler, I use this exact pattern to correlate CVEs:

```python
# Find pairs of vulnerabilities that combine to exceed risk threshold
def find_exploit_chain(vulnerabilities, risk_threshold):
    seen = {}
    for i, vuln in enumerate(vulnerabilities):
        complement_cvss = risk_threshold - vuln.cvss_score
        if complement_cvss in seen:
            return [seen[complement_cvss], i]  # Exploit chain found
        seen[vuln.cvss_score] = i
```

**Why it matters:** SIEM systems process millions of events/second. O(n²) brute force (checking every pair) would crash the system. Hash maps enable real-time correlation.

**Result:** Accepted, beats 51.92% on runtime (3ms)

---

### **2. Contains Duplicate (LC 217) - Set for Deduplication**

**Problem:** Return true if any value appears twice in an array.

**My Approach:**

- **Logic:** "Have I seen this before?" → Set membership test
- **Storage:** Set for O(1) lookups (don't need indices, just existence)
- **Complexity:** O(n) time, O(n) space

**Cybersecurity Application:**
Deduplicating security alerts in Vappler's dashboard:

```python
# Filter duplicate vulnerability findings across scans
def deduplicate_findings(scan_results):
    seen = set()
    unique_vulns = []
    for vuln in scan_results:
        vuln_hash = f"{vuln.cve_id}_{vuln.host}_{vuln.port}"
        if vuln_hash not in seen:
            unique_vulns.append(vuln)
            seen.add(vuln_hash)
    return unique_vulns
```

**Why it matters:** Users don't want to see the same CVE-2024-1234 reported 50 times across 50 IPs. Set-based deduplication ensures clean dashboards.

**Result:** Accepted (pending final submission)

---

## The Java → Python Transition

I came from a Java background (JCCC networking class, enterprise mindset). My biggest hurdles:

| Java Habit                     | Python Reality       | How I Fixed It                                     |
| ------------------------------ | -------------------- | -------------------------------------------------- |
| `for (int i = 0; i < n; i++);` | `for i in range(n):` | Stopped reaching for semicolons after ~10 problems |
| `HashMap<Integer, Integer>`    | `dict` or `{}`       | Embraced dynamic typing                            |
| `array.length`                 | `len(array)`         | Muscle memory shift                                |
| `map.containsKey(x)`           | `x in map`           | Python's cleaner syntax won me over                |

**Key realization:** Python is "Java with less typing." Same logic, cleaner syntax. After 2 problems, I stopped fighting the language and started leveraging it.

---

## Why This Matters for IBM

The IBM "Entry-Level AI Software Engineer" role requires:

- Backend systems design (Flask, PostgreSQL, Docker); Vappler proves this
- Algorithmic thinking under pressure; This repo proves this
- Security-aware engineering; Every solution maps to a security use case

**I'm not only solving puzzles, but demonstrating the SAME thought process I use to architect production systems.**

When IBM asks "tell me about a time you optimized performance," I'll talk about:

1. **Vappler's dashboard:** Reduced query latency from 2.3s → 300ms (87%) using materialized views
2. **Two Sum pattern:** Reduced time complexity from O(n²) → O(n) using hash maps

**Same optimization mindset. Different scale.**

---

## Next Steps

**Immediate (Feb 5-6):**

- Valid Anagram (hash map counting pattern)
- Valid Parentheses (stack pattern)
- Longest Substring Without Repeating Characters (sliding window)

**By Feb 7:** 10 problems solved, all with security context documented

**Feb 8-9:** Take IBM HackerRank assessment

**Goal:** Prove I can translate requirements → algorithm → optimized code under time pressure, with security applications embedded in my thinking.

---

## Technical Setup

**Language:** Python 3.10+  
**Platform:** LeetCode  
**Documentation Standard:** Every solution includes:

- Input/output specification
- Mathematical relationship
- Storage justification
- Step-by-step logic
- Cybersecurity use case

**Why over-document?** Because in production (Vappler), I maintain 28-file microservices architecture. Future me (or teammates) needs to understand WHY I chose a dict over a list, not just THAT I chose it.

---

## Contact

**Ryan Duckworth**  
rduckworth@aspidasecurity.io  
[LinkedIn](https://www.linkedin.com/in/rduckworthfl333)  
[Portfolio](https://aspidasecurity.io)  
[Vappler Docs](https://github.com/rduckworthfl-ux/vapplerDocs)
[Website](https://aspidasecurity.io)

---

## Acknowledgment

This repository is a forcing function. I'm not naturally a "whiteboard coder";I'm a systems builder who debugs production crashes at 3 AM. But IBM's interview process tests algorithmic thinking, so I'm learning to formalize the patterns I've been using intuitively.

**Turns out:** The hash map that powers Vappler's CVE correlation is the SAME hash map that solves Two Sum.

I just needed to see the math. Now I do.

---

**Last Updated:** Feb 4, 2026, 20:47 CST  
**Problems Solved:** 2 (Two Sum, Contains Duplicate)  
**Target:** 10 by Feb 7

---
