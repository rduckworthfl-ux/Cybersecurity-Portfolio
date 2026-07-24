"""
Contains Duplicate - LeetCode #217
Pattern: Set for Membership Testing
Author: Ryan Duckworth
Date: Feb 4, 2026
Runtime: 7ms (beats 89.35%)
"""

class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        """
        Check if any value appears at least twice in the array.
        
        Args:
            nums: Array of integers to check for duplicates
            
        Returns:
            True if any duplicate exists, False if all elements are distinct
            
        Time:  O(n) - single pass with O(1) set lookups
        Space: O(n) - worst case stores all n elements
        """
        
        # INPUT:  array[int] named nums
        # TASK:   Check if any number appears more than once
        # OUTPUT: bool (True if duplicate exists, False if all unique)
        
        # STEP 1: Initialize set to track seen values
        # Using set() instead of {} (which creates dict)
        seen = set()
        
        # STEP 2: Iterate through array values
        for num in nums:
            
            # STEP 2a: Check if number already exists (O(1) lookup)
            if num in seen:
                return True  # Duplicate found - early return optimization
            
            # STEP 3: Add number to set for future checks
            seen.add(num)
        
        # STEP 4: No duplicates found
        return False


# ==============================================================================
# COMPLEXITY ANALYSIS
# ==============================================================================
# Time:  O(n) - Single pass through array, O(1) set operations
# Space: O(n) - Worst case (no duplicates) stores all n elements
#
# PERFORMANCE: 7ms runtime (beats 89.35% of Python3 submissions)
#              31.27 MB memory (beats 66.37%)
#
# WHY FAST: Early return on first duplicate + O(1) set lookups


# ==============================================================================
# CYBERSECURITY APPLICATION (Brief inline context)
# ==============================================================================
"""
This pattern is used in Vappler for:

1. KEV Catalog Lookup (tasks.py):
   - Load CISA's 10K+ known exploited CVEs into set
   - Check discovered vulnerabilities: if vuln['cve_id'] in kev_cves
   - O(1) lookup vs O(n) list scan

2. Nmap Script Validation (mapper.py):
   - ALLOWED_SCRIPTS = {'vulners', 'http-enum', 'ssl-cert', ...}
   - Reject unauthorized scripts: if script_id not in ALLOWED_SCRIPTS

Note: Vulnerability deduplication uses Postgres UNIQUE index, not Python sets.
Database-level is faster for persistent data (50ms for 100K rows).

See README.md for full architecture details and 5 security use cases.
"""
