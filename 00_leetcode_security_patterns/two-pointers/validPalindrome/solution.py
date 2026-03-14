class Solution:
    def isPalindrome(self, s: str) -> bool:
        """
        CYBERSECURITY APPLICATION:
        The two-pointer inward scan is the foundation of symmetric pattern
        detection — a technique used throughout network analysis and
        input validation in security tooling.

        Real-world use cases in my Vappler platform:

        - Network Payload Symmetry Analysis:
          Certain protocol-level attacks (reflection attacks, amplification DDoS)
          generate network packets with symmetric payloads. Two-pointer scanning
          identifies palindromic byte sequences in captured traffic — a strong
          anomaly indicator in DPI (Deep Packet Inspection) engines.

        - Input Sanitization Validation:
          Before storing user-supplied strings (scan target names, asset labels),
          Vappler strips non-alphanumeric characters and normalizes case — the
          exact transformation in this algorithm — ensuring consistent storage
          and preventing encoding-based injection via special character padding.

        - Binary Search on Sorted CVSS Scores:
          The two-pointer technique generalizes to O(n) sorted-array traversal.
          In Vappler's prioritization engine, left/right pointers scan sorted
          CVE lists to find vulnerability pairs that together exceed a risk
          threshold — same O(n) time as this palindrome check.

        - Log String Normalization:
          SIEM parsers strip punctuation and case-normalize log fields before
          correlation — identical to the alphanumeric filter + lowercase
          transformation applied here. Consistent normalization prevents
          attackers from evading detection via punctuation padding in payloads.

        Pattern: Strip noise (non-alphanumeric) → Normalize (lowercase) →
                 Compare from outside in → Mismatch at any point = not symmetric
        """

        # input  - string s (may contain alphanumerics, spaces, punctuation)
        # task   - determine if s reads the same forwards and backwards
        #          after keeping only alphanumeric chars and lowercasing
        # output - bool: True if valid palindrome, False otherwise

        # Step 1: Initialize two pointers at opposite ends
        left = 0
        right = len(s) - 1

        while left < right:
            # Step 2: Advance left past any non-alphanumeric characters
            # (skip punctuation, spaces — they don't count)
            while left < right and not s[left].isalnum():
                left += 1

            # Step 3: Retreat right past any non-alphanumeric characters
            while left < right and not s[right].isalnum():
                right -= 1

            # Step 4: Compare normalized characters
            # Case-insensitive: 'A' and 'a' are the same
            if s[left].lower() != s[right].lower():
                return False  # Asymmetry found — not a palindrome

            # Step 5: Move both pointers inward and continue
            left += 1
            right -= 1

        # All characters matched — valid palindrome
        return True