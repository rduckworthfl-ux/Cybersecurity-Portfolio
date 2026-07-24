class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:

        """
        CYBERSECURITY APPLICATION:
        This hash map pattern is the foundation of security analytics and threat detection.
        
        Real-world use cases in my Vappler platform:
        - CVE Correlation: Given vulnerability scan results, find pairs of CVEs that 
          combine to create a critical exploit chain (CVSS scores sum to threshold)
        - Log Analysis: Identify suspicious login patterns by matching failed authentication 
          attempts (IP addresses) with known attack signatures (port scans)
        - Threat Intelligence: Cross-reference IOCs (Indicators of Compromise) against 
          live network traffic by storing observed IPs/domains in hash map for O(1) lookups
        
        The mathematical relationship (x + y = target) translates to:
        "Given a threat severity threshold, which two attack vectors combine to exceed it?"
        
        This same O(n) time complexity is critical in SIEM systems processing millions 
        of security events per second - can't afford O(n²) brute force when analyzing 
        real-time threats.
        
        Pattern: Store known threats → Check incoming events → Alert on match
        """
        
        # input         - array[int] named nums, and an int named target
        # task          - take input array nums and find the two indices that will Sum to equal input var target
        # output        - array[int] 2 ints in the input array (the indices) 
        #                   which will equal the target variable
        
        # expression    - x + y = t
        # translation   - complement = target - num
        

        # Requirements  - since we are comparing iterables, we will need to store them to compare
        # Step 1. : Initialize Storage for results of iteration
        seen = {}

        # Step 2. : Iterate to loop through indices of nums array
        for i, num in enumerate(nums):

            # Step 3. : Calculate value of indices at the iteration point to see if the value complements the solution
            complement = target - num

            # Step 4. : Check if the complement exists in storage (seen) 
            if complement in seen:  #Check if NUMBER exists
                return [seen[complement], i]    # Get its INDEX

            # Step 5. : Store current number for future iterations
            # Remember this number in case it's a complement later"
            seen[num] = i

        # Step 6: No solution found (won't happen per problem guarantee)
        return []