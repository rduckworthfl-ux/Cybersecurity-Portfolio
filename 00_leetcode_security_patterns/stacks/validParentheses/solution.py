from typing import Dict


class Solution:
    def isValid(self, s: str) -> bool:
        """
        CYBERSECURITY APPLICATION:
        The stack-based bracket matcher is one of the most deployed algorithms
        in security tooling  -  anywhere structured text must be validated before
        it reaches a parser, interpreter, or database.

        Real-world use cases in my Vappler platform:

        - Nmap XML Output Validation:
          Vappler ingests raw Nmap XML scan results. Before Celery workers parse
          the XML into CVE records, a stack validator confirms all XML tags are
          properly nested. Malformed/truncated XML (from a crashed scan) is
          rejected before it can corrupt the vulnerability database.

        - SQL Injection Pre-Filter:
          Unmatched parentheses in API query parameters are a strong indicator
          of SQL injection attempts. A stack check on incoming request strings
          provides O(n) pre-filtering before the query hits the database layer.

        - YARA Rule Syntax Validation:
          YARA rules (used in malware detection) rely on correctly nested
          `{}`, `()`, and `[]`. A stack validator catches malformed rules
          before they're compiled and deployed to endpoint agents.

        - JSON/BSON API Request Validation:
          Flask API endpoints in Vappler validate bracket structure of incoming
          JSON payloads before deserialization  -  preventing malformed-input
          attacks and unexpected behavior in nested data parsers.

        Pattern: Push opening brackets → On closing bracket, check top of stack
                 → Mismatch or leftover = invalid structure = reject
        """

        # input  - string s containing only bracket characters: ( ) { } [ ]
        # task   - determine if the brackets are validly nested and matched
        # output - bool: True if valid, False otherwise

        # Step 1: Initialize the stack (tracks unmatched opening brackets)
        stack = []

        # Step 2: Map each closing bracket to its expected opening bracket
        # Storing closing→opening means: when we see a closer, we know
        # what the top of the stack MUST be for it to be valid
        mapping: Dict[str, str] = {')': '(', '}': '{', ']': '['}

        for char in s:
            if char in mapping:
                # It's a closing bracket  -  pop the stack and verify match
                # Use '#' sentinel if stack is empty (prevents IndexError)
                top = stack.pop() if stack else '#'
                if top != mapping[char]:
                    return False  # Mismatch  -  invalid structure
            else:
                # It's an opening bracket  -  push onto stack to match later
                stack.append(char)

        # Step 3: Valid only if all opening brackets were matched (stack empty)
        return len(stack) == 0