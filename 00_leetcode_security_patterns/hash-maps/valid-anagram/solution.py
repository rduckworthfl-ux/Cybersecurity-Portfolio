from typing import Dict


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        """
        CYBERSECURITY APPLICATION:
        The character-frequency hash map is the backbone of string-based
        threat detection in security tooling.

        Real-world use cases in my Vappler platform:

        - Username Spoofing Detection (IAM):
          Attackers register "admni" or "adm1n" to impersonate "admin".
          An anagram check flags when two usernames share identical character
          sets — a strong signal for identity-based attacks.

        - Obfuscated Malware String Detection:
          Malware authors rearrange known attack signatures to evade static
          analysis. AV/EDR engines use character-frequency maps to detect
          rearranged payloads even when byte order is scrambled.

        - Log Field Normalization:
          SIEM parsers verify that two log fields describing the same event
          carry the same token set (e.g., HTTP method + path pairs must
          have matching character budgets after normalization).

        - Protocol Command Validation:
          In custom binary protocols, valid commands are anagrams of
          a whitelist. Invalid frequency maps = unknown/malicious commands.

        The O(n) frequency-map approach (vs O(n log n) sort) is critical
        when a SIEM processes millions of events per second.

        Pattern: Build frequency map → Decrement against second string →
                 Any non-zero value = mismatch = anomaly
        """

        # input  - two strings s and t
        # task   - determine if t is an anagram of s
        #          (same characters, same frequencies, any order)
        # output - bool: True if anagram, False otherwise

        # Early exit: anagrams must be the same length
        if len(s) != len(t):
            return False

        # Step 1: Initialize frequency storage
        count: Dict[str, int] = {}

        # Step 2: Increment frequency for every character in s
        for char in s:
            count[char] = count.get(char, 0) + 1

        # Step 3: Decrement frequency for every character in t
        # If t has chars not in s, count will go negative (non-zero)
        for char in t:
            count[char] = count.get(char, 0) - 1

        # Step 4: All frequencies must be zero — any remainder means mismatch
        for val in count.values():
            if val != 0:
                return False

        return True
