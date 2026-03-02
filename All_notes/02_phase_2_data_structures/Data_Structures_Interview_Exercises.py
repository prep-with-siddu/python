"""
=============================================================================
 DATA STRUCTURES — HANDS-ON INTERVIEW EXERCISES 
=============================================================================
 Topics: Lists, Tuples, Dictionaries, Sets, deque, heapq, bisect, enum
 Difficulty: Medium to Hard (Expected for 3 YOE Python Backend Developer)
 
 Instructions:
 - Try solving each problem YOURSELF before looking at the solution.
 - Focus on TIME & SPACE complexity — interviewers WILL ask.
 - Each exercise has: Problem → Hints → Solution → Explanation
=============================================================================
"""

# ============================================================================
# SECTION 1: LISTS (Most Asked in Interviews)
# ============================================================================

# ────────────────────────────────────────────────────────────────────────────
# Exercise 1: Flatten a Nested List (Any Depth)
# ────────────────────────────────────────────────────────────────────────────
# Given an arbitrarily nested list, flatten it into a single list.
# Example: [1, [2, [3, 4], 5], [6, 7]] → [1, 2, 3, 4, 5, 6, 7]
#
# Why asked? Tests recursion + understanding of iterables.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def flatten(nested_list):
    """Recursively flatten a nested list of any depth."""
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

# Test
assert flatten([1, [2, [3, 4], 5], [6, 7]]) == [1, 2, 3, 4, 5, 6, 7]
assert flatten([1, [2, [3, [4, [5]]]]]) == [1, 2, 3, 4, 5]
assert flatten([]) == []
print("✅ Exercise 1 passed")

# 🔍 Follow-up: Iterative version using a stack (interviewers love this!)
def flatten_iterative(nested_list):
    stack = list(reversed(nested_list))
    result = []
    while stack:
        item = stack.pop()
        if isinstance(item, list):
            stack.extend(reversed(item))
        else:
            result.append(item)
    return result

assert flatten_iterative([1, [2, [3, 4], 5], [6, 7]]) == [1, 2, 3, 4, 5, 6, 7]
print("✅ Exercise 1 (iterative) passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 2: Group Anagrams
# ────────────────────────────────────────────────────────────────────────────
# Given a list of strings, group the anagrams together.
# Example: ["eat","tea","tan","ate","nat","bat"] 
#        → [["eat","tea","ate"], ["tan","nat"], ["bat"]]
#
# Why asked? Tests dict + sorting + grouping — very common 3 YOE question.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
from collections import defaultdict

def group_anagrams(words):
    """Group anagrams using sorted word as key."""
    groups = defaultdict(list)
    for word in words:
        key = tuple(sorted(word))  # "eat" → ('a', 'e', 't')
        groups[key].append(word)
    return list(groups.values())

result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
# Verify grouping: sort inner lists and outer list for comparison
result_sorted = [sorted(g) for g in result]
result_sorted.sort()
assert result_sorted == [['ate', 'eat', 'tea'], ['bat'], ['nat', 'tan']]
print("✅ Exercise 2 passed")

# Time: O(n * k log k) where n = number of words, k = max word length
# Space: O(n * k)


# ────────────────────────────────────────────────────────────────────────────
# Exercise 3: Find All Duplicates in a List (O(n) time, O(1) extra space)
# ────────────────────────────────────────────────────────────────────────────
# Given a list of integers where 1 ≤ a[i] ≤ n (n = size of list),
# some elements appear twice. Find all duplicates.
# Example: [4, 3, 2, 7, 8, 2, 3, 1] → [2, 3]
#
# Why asked? Tests in-place array manipulation — classic 3 YOE question.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution (Index marking trick — no extra space):
def find_duplicates(nums):
    """Find duplicates using index-marking (negate values at index)."""
    duplicates = []
    for num in nums:
        index = abs(num) - 1
        if nums[index] < 0:
            duplicates.append(abs(num))
        else:
            nums[index] = -nums[index]
    return duplicates

assert sorted(find_duplicates([4, 3, 2, 7, 8, 2, 3, 1])) == [2, 3]
print("✅ Exercise 3 passed")

# Time: O(n) | Space: O(1) extra (modifies input)


# ────────────────────────────────────────────────────────────────────────────
# Exercise 4: Rotate a List by K Positions (In-Place)
# ────────────────────────────────────────────────────────────────────────────
# Rotate a list to the right by k steps.
# Example: [1,2,3,4,5,6,7], k=3 → [5,6,7,1,2,3,4]
#
# Why asked? Tests slicing knowledge + modular arithmetic.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution 1 — Pythonic slicing:
def rotate_list(nums, k):
    k = k % len(nums)  # Handle k > len
    return nums[-k:] + nums[:-k]

assert rotate_list([1, 2, 3, 4, 5, 6, 7], 3) == [5, 6, 7, 1, 2, 3, 4]
print("✅ Exercise 4a passed")

# ✅ Solution 2 — Reverse algorithm (asked in interviews for in-place):
def rotate_inplace(nums, k):
    """In-place rotation using triple reverse."""
    n = len(nums)
    k = k % n
    
    def reverse(start, end):
        while start < end:
            nums[start], nums[end] = nums[end], nums[start]
            start += 1
            end -= 1
    
    reverse(0, n - 1)       # Reverse entire list
    reverse(0, k - 1)       # Reverse first k
    reverse(k, n - 1)       # Reverse remaining
    return nums

assert rotate_inplace([1, 2, 3, 4, 5, 6, 7], 3) == [5, 6, 7, 1, 2, 3, 4]
print("✅ Exercise 4b (in-place) passed")

# Time: O(n) | Space: O(1) for in-place version


# ────────────────────────────────────────────────────────────────────────────
# Exercise 5: Merge Intervals
# ────────────────────────────────────────────────────────────────────────────
# Given a list of intervals, merge all overlapping intervals.
# Example: [[1,3],[2,6],[8,10],[15,18]] → [[1,6],[8,10],[15,18]]
#
# Why asked? VERY common — tests sorting + interval logic.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def merge_intervals(intervals):
    """Merge overlapping intervals after sorting by start time."""
    if not intervals:
        return []
    
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:  # Overlapping
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    
    return merged

assert merge_intervals([[1,3],[2,6],[8,10],[15,18]]) == [[1,6],[8,10],[15,18]]
assert merge_intervals([[1,4],[4,5]]) == [[1,5]]
print("✅ Exercise 5 passed")

# Time: O(n log n) due to sort | Space: O(n)


# ────────────────────────────────────────────────────────────────────────────
# Exercise 6: Product of Array Except Self (No Division!)
# ────────────────────────────────────────────────────────────────────────────
# Given list nums, return list where output[i] = product of all elements 
# except nums[i]. WITHOUT using division.
# Example: [1,2,3,4] → [24,12,8,6]
#
# Why asked? Classic prefix/suffix pattern — asked at Amazon, Google, etc.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def product_except_self(nums):
    """Use prefix and suffix products."""
    n = len(nums)
    result = [1] * n
    
    # Left pass: result[i] = product of all elements to the left
    prefix = 1
    for i in range(n):
        result[i] = prefix
        prefix *= nums[i]
    
    # Right pass: multiply by product of all elements to the right
    suffix = 1
    for i in range(n - 1, -1, -1):
        result[i] *= suffix
        suffix *= nums[i]
    
    return result

assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
assert product_except_self([2, 3, 4, 5]) == [60, 40, 30, 24]
print("✅ Exercise 6 passed")

# Time: O(n) | Space: O(1) extra (output doesn't count)


# ============================================================================
# SECTION 2: DICTIONARIES (Backend Developer Bread & Butter)
# ============================================================================

# ────────────────────────────────────────────────────────────────────────────
# Exercise 7: Two Sum (Return indices)
# ────────────────────────────────────────────────────────────────────────────
# Given a list of nums and a target, return indices of two numbers 
# that add up to target. Assume exactly one solution exists.
# Example: nums=[2,7,11,15], target=9 → [0,1]
#
# Why asked? THE most common interview question — tests dict lookup.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def two_sum(nums, target):
    """One-pass hash map approach."""
    seen = {}  # value → index
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

assert two_sum([2, 7, 11, 15], 9) == [0, 1]
assert two_sum([3, 2, 4], 6) == [1, 2]
print("✅ Exercise 7 passed")

# Time: O(n) | Space: O(n)


# ────────────────────────────────────────────────────────────────────────────
# Exercise 8: LRU Cache Implementation
# ────────────────────────────────────────────────────────────────────────────
# Implement an LRU (Least Recently Used) cache with get() and put().
# Both operations should be O(1).
#
# Why asked? Tests OrderedDict knowledge — very common for 3 YOE.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution using OrderedDict:
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)  # Mark as recently used
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # Remove oldest (first item)

# Test
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
assert cache.get(1) == 1       # Returns 1, makes key=1 most recent
cache.put(3, 3)                 # Evicts key=2 (least recently used)
assert cache.get(2) == -1       # key=2 was evicted
cache.put(4, 4)                 # Evicts key=1
assert cache.get(1) == -1       # key=1 was evicted
assert cache.get(3) == 3
assert cache.get(4) == 4
print("✅ Exercise 8 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 9: Frequency Sort
# ────────────────────────────────────────────────────────────────────────────
# Sort a list by frequency of elements (most frequent first).
# If same frequency, maintain original order.
# Example: [1,1,2,2,2,3] → [2,2,2,1,1,3]
#
# Why asked? Tests Counter + sorted with custom key.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
from collections import Counter

def frequency_sort(nums):
    """Sort by frequency descending, maintain relative order for ties."""
    freq = Counter(nums)
    # Sort by (-frequency, first_occurrence_index) for stable ordering
    return sorted(nums, key=lambda x: (-freq[x], nums.index(x)))

# Simpler version just by frequency:
def frequency_sort_simple(nums):
    freq = Counter(nums)
    return sorted(nums, key=lambda x: -freq[x])

assert frequency_sort_simple([1, 1, 2, 2, 2, 3]) == [2, 2, 2, 1, 1, 3]
print("✅ Exercise 9 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 10: Invert a Dictionary (Handle Duplicate Values)
# ────────────────────────────────────────────────────────────────────────────
# Given a dict, swap keys and values. Since values may not be unique,
# collect all original keys as a list for each new key.
# Example: {"a": 1, "b": 2, "c": 1} → {1: ["a", "c"], 2: ["b"]}
#
# Why asked? Tests defaultdict + dict comprehension awareness.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def invert_dict(d):
    """Invert dict, grouping keys that had the same value."""
    inverted = defaultdict(list)
    for key, value in d.items():
        inverted[value].append(key)
    return dict(inverted)

assert invert_dict({"a": 1, "b": 2, "c": 1}) == {1: ["a", "c"], 2: ["b"]}
assert invert_dict({}) == {}
print("✅ Exercise 10 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 11: Merge Two Dicts — Deep Merge (Nested)
# ────────────────────────────────────────────────────────────────────────────
# Merge two nested dicts. If both have a key with dict values, merge them
# recursively. Otherwise, second dict's value wins.
#
# Why asked? Very practical for config management in backend systems.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def deep_merge(dict1, dict2):
    """Recursively merge dict2 into dict1."""
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result

base = {"db": {"host": "localhost", "port": 5432}, "debug": True}
override = {"db": {"port": 5433, "name": "mydb"}, "debug": False}
expected = {"db": {"host": "localhost", "port": 5433, "name": "mydb"}, "debug": False}
assert deep_merge(base, override) == expected
print("✅ Exercise 11 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 12: First Non-Repeating Character in a String
# ────────────────────────────────────────────────────────────────────────────
# Find the first character that appears only once.
# Example: "aabbccdde" → "e"
# Example: "abacabad" → "c"
#
# Why asked? Tests Counter/dict + preserve insertion order (Python 3.7+).
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def first_unique_char(s):
    """Find first non-repeating character using Counter."""
    freq = Counter(s)
    for char in s:
        if freq[char] == 1:
            return char
    return None

assert first_unique_char("aabbccdde") == "e"
assert first_unique_char("abacabad") == "c"
assert first_unique_char("aabb") is None
print("✅ Exercise 12 passed")

# Time: O(n) | Space: O(1) — at most 26 chars for lowercase English


# ============================================================================
# SECTION 3: SETS (Often Overlooked but Important!)
# ============================================================================

# ────────────────────────────────────────────────────────────────────────────
# Exercise 13: Find the Longest Consecutive Sequence
# ────────────────────────────────────────────────────────────────────────────
# Given an unsorted list, find the length of the longest consecutive 
# sequence. Must run in O(n).
# Example: [100, 4, 200, 1, 3, 2] → 4 (sequence: [1,2,3,4])
#
# Why asked? Classic use of sets for O(1) lookup — asked at top companies.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def longest_consecutive(nums):
    """Use a set and only start counting from sequence beginnings."""
    num_set = set(nums)
    longest = 0
    
    for num in num_set:
        # Only start counting if num is the START of a sequence
        if num - 1 not in num_set:
            current = num
            streak = 1
            while current + 1 in num_set:
                current += 1
                streak += 1
            longest = max(longest, streak)
    
    return longest

assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
assert longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
assert longest_consecutive([]) == 0
print("✅ Exercise 13 passed")

# Time: O(n) — each number is visited at most twice
# Space: O(n) for the set


# ────────────────────────────────────────────────────────────────────────────
# Exercise 14: Find All Pairs with Given Difference
# ────────────────────────────────────────────────────────────────────────────
# Given a list of distinct integers and a target difference k,
# find all pairs (a, b) where a - b = k.
# Example: [1, 5, 3, 4, 2], k=2 → [(3,1), (4,2), (5,3)]
#
# Why asked? Tests set-based lookup vs brute force.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def find_pairs_with_diff(nums, k):
    """Use set lookup: if num - k exists in set, it's a valid pair."""
    num_set = set(nums)
    pairs = []
    for num in sorted(nums):
        if num - k in num_set:
            pairs.append((num, num - k))
    return pairs

assert find_pairs_with_diff([1, 5, 3, 4, 2], 2) == [(3, 1), (4, 2), (5, 3)]
print("✅ Exercise 14 passed")

# Time: O(n log n) due to sort | Space: O(n)


# ────────────────────────────────────────────────────────────────────────────
# Exercise 15: Set Operations — Real-World Scenario
# ────────────────────────────────────────────────────────────────────────────
# You have three API endpoints. Each returns a set of user IDs.
# Find: 
#   a) Users who accessed ALL three endpoints
#   b) Users who accessed ONLY endpoint A (not B or C)
#   c) Users who accessed exactly two endpoints
#
# Why asked? Tests real-world set operations — common in backend analytics.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def analyze_endpoint_users(a, b, c):
    set_a, set_b, set_c = set(a), set(b), set(c)
    
    # a) Users in ALL three
    all_three = set_a & set_b & set_c
    
    # b) Users ONLY in A
    only_a = set_a - set_b - set_c
    
    # c) Users in exactly 2 endpoints
    in_ab = (set_a & set_b) - set_c
    in_ac = (set_a & set_c) - set_b
    in_bc = (set_b & set_c) - set_a
    exactly_two = in_ab | in_ac | in_bc
    
    return all_three, only_a, exactly_two

a_users = [1, 2, 3, 4, 5]
b_users = [3, 4, 5, 6, 7]
c_users = [5, 6, 7, 8, 9]

all_three, only_a, exactly_two = analyze_endpoint_users(a_users, b_users, c_users)
assert all_three == {5}
assert only_a == {1, 2}
assert exactly_two == {3, 4, 6, 7}
print("✅ Exercise 15 passed")


# ============================================================================
# SECTION 4: TUPLES (Quick but Tricky Interview Questions)
# ============================================================================

# ────────────────────────────────────────────────────────────────────────────
# Exercise 16: Tuple as Dict Key — Caching Pattern
# ────────────────────────────────────────────────────────────────────────────
# Implement a simple function cache using tuples as dictionary keys.
# Cache the results of an expensive function call.
#
# Why asked? Tests understanding of hashability and why tuples can be keys.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def make_cached(func):
    """Simple memoization decorator using tuples as cache keys."""
    cache = {}
    
    def wrapper(*args):
        key = args  # args is already a tuple — hashable!
        if key not in cache:
            cache[key] = func(*args)
        return cache[key]
    
    wrapper.cache = cache  # Expose for testing
    return wrapper

@make_cached
def expensive_add(a, b):
    print(f"  Computing {a} + {b}...")  # Shows when actually computed
    return a + b

result1 = expensive_add(3, 4)   # Prints "Computing 3 + 4..."
result2 = expensive_add(3, 4)   # No print — cached!
result3 = expensive_add(5, 6)   # Prints "Computing 5 + 6..."

assert result1 == 7
assert result2 == 7
assert result3 == 11
assert len(expensive_add.cache) == 2
print("✅ Exercise 16 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 17: Named Tuple for API Response Modeling
# ────────────────────────────────────────────────────────────────────────────
# Model an API response using namedtuple. Parse raw dicts into namedtuples.
#
# Why asked? Tests knowledge of namedtuple vs dict vs dataclass.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
from collections import namedtuple

APIResponse = namedtuple("APIResponse", ["status_code", "data", "error"])

def parse_responses(raw_responses):
    """Convert raw dicts to namedtuples and categorize."""
    responses = [APIResponse(**r) for r in raw_responses]
    success = [r for r in responses if 200 <= r.status_code < 300]
    errors = [r for r in responses if r.status_code >= 400]
    return success, errors

raw = [
    {"status_code": 200, "data": {"id": 1}, "error": None},
    {"status_code": 404, "data": None, "error": "Not Found"},
    {"status_code": 201, "data": {"id": 2}, "error": None},
    {"status_code": 500, "data": None, "error": "Server Error"},
]

success, errors = parse_responses(raw)
assert len(success) == 2
assert len(errors) == 2
assert success[0].data == {"id": 1}
assert errors[0].error == "Not Found"
print("✅ Exercise 17 passed")


# ============================================================================
# SECTION 5: DEQUE, HEAPQ, BISECT (Advanced — Differentiators!)
# ============================================================================

# ────────────────────────────────────────────────────────────────────────────
# Exercise 18: Sliding Window Maximum (Using deque)
# ────────────────────────────────────────────────────────────────────────────
# Given an array and window size k, return the max of each window.
# Example: nums=[1,3,-1,-3,5,3,6,7], k=3 → [3,3,5,5,6,7]
#
# Why asked? Tests deque for monotonic queue — hard but common at 3 YOE.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
from collections import deque

def max_sliding_window(nums, k):
    """Use a monotonic decreasing deque of indices."""
    dq = deque()  # Stores indices, front = index of current max
    result = []
    
    for i in range(len(nums)):
        # Remove indices outside the window
        while dq and dq[0] < i - k + 1:
            dq.popleft()
        
        # Remove smaller elements from the back (they'll never be max)
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        
        dq.append(i)
        
        # Window is fully formed starting at index k-1
        if i >= k - 1:
            result.append(nums[dq[0]])
    
    return result

assert max_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
assert max_sliding_window([1], 1) == [1]
print("✅ Exercise 18 passed")

# Time: O(n) — each element enters and leaves deque at most once
# Space: O(k)


# ────────────────────────────────────────────────────────────────────────────
# Exercise 19: Top K Frequent Elements (Using heapq)
# ────────────────────────────────────────────────────────────────────────────
# Given a list and integer k, return the k most frequent elements.
# Example: [1,1,1,2,2,3], k=2 → [1,2]
#
# Why asked? Tests heap + Counter — extremely common interview question.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
import heapq

def top_k_frequent(nums, k):
    """Use Counter + heapq.nlargest (or min-heap of size k)."""
    freq = Counter(nums)
    # nlargest uses a min-heap internally — O(n log k)
    return [item for item, count in heapq.nlargest(k, freq.items(), key=lambda x: x[1])]

assert sorted(top_k_frequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
assert top_k_frequent([1], 1) == [1]
print("✅ Exercise 19 passed")

# Alternative: Bucket sort approach — O(n) time!
def top_k_frequent_bucket(nums, k):
    """Bucket sort: index = frequency, value = list of nums with that freq."""
    freq = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    
    for num, count in freq.items():
        buckets[count].append(num)
    
    result = []
    for i in range(len(buckets) - 1, -1, -1):
        for num in buckets[i]:
            result.append(num)
            if len(result) == k:
                return result
    return result

assert sorted(top_k_frequent_bucket([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
print("✅ Exercise 19 (bucket sort) passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 20: Find Median from Data Stream (Using two heaps)
# ────────────────────────────────────────────────────────────────────────────
# Design a class that supports:
#   - addNum(num): Add a number from the stream
#   - findMedian(): Return the median of all added numbers
#
# Why asked? Classic heap problem — tests design skills for 3 YOE.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
class MedianFinder:
    def __init__(self):
        self.small = []  # Max-heap (inverted) — stores smaller half
        self.large = []  # Min-heap — stores larger half
    
    def addNum(self, num):
        # Push to max-heap (negate for max-heap behavior)
        heapq.heappush(self.small, -num)
        
        # Ensure max of small ≤ min of large
        if self.small and self.large and (-self.small[0]) > self.large[0]:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        
        # Balance sizes (small can have at most 1 more than large)
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)
    
    def findMedian(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2

mf = MedianFinder()
mf.addNum(1)
mf.addNum(2)
assert mf.findMedian() == 1.5
mf.addNum(3)
assert mf.findMedian() == 2
mf.addNum(4)
assert mf.findMedian() == 2.5
print("✅ Exercise 20 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 21: Insert Position using bisect
# ────────────────────────────────────────────────────────────────────────────
# Use the bisect module to maintain a sorted list efficiently and
# implement a ranking system.
#
# Why asked? Tests knowledge of bisect for efficient sorted operations.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
import bisect

class Leaderboard:
    """Maintain a sorted leaderboard using bisect."""
    
    def __init__(self):
        self.scores = []       # Sorted list of scores
        self.players = {}      # player → score
    
    def add_score(self, player, score):
        if player in self.players:
            # Remove old score
            old_score = self.players[player]
            idx = bisect.bisect_left(self.scores, old_score)
            self.scores.pop(idx)
        
        # Insert new score in sorted position
        bisect.insort(self.scores, score)
        self.players[player] = score
    
    def get_rank(self, player):
        """Rank 1 = highest score."""
        if player not in self.players:
            return -1
        score = self.players[player]
        # Position from the right (higher = better)
        return len(self.scores) - bisect.bisect_right(self.scores, score) + 1
    
    def top_k(self, k):
        """Return top k scores."""
        return self.scores[-k:][::-1]

lb = Leaderboard()
lb.add_score("Alice", 100)
lb.add_score("Bob", 200)
lb.add_score("Charlie", 150)

assert lb.get_rank("Bob") == 1
assert lb.get_rank("Charlie") == 2
assert lb.get_rank("Alice") == 3
assert lb.top_k(2) == [200, 150]

lb.add_score("Alice", 250)  # Alice updates score
assert lb.get_rank("Alice") == 1
print("✅ Exercise 21 passed")


# ============================================================================
# SECTION 6: MIXED / REAL-WORLD BACKEND SCENARIOS
# ============================================================================

# ────────────────────────────────────────────────────────────────────────────
# Exercise 22: Rate Limiter using deque (Sliding Window)
# ────────────────────────────────────────────────────────────────────────────
# Implement a rate limiter: max N requests per window of T seconds.
# This is a REAL backend interview question!
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
import time

class RateLimiter:
    """Sliding window rate limiter using deque."""
    
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests = defaultdict(deque)  # user_id → deque of timestamps
    
    def is_allowed(self, user_id, current_time=None):
        if current_time is None:
            current_time = time.time()
        
        user_requests = self.requests[user_id]
        
        # Remove timestamps outside the window
        while user_requests and user_requests[0] <= current_time - self.window:
            user_requests.popleft()
        
        if len(user_requests) < self.max_requests:
            user_requests.append(current_time)
            return True
        return False

# Test: 3 requests per 10 seconds
rl = RateLimiter(max_requests=3, window_seconds=10)
assert rl.is_allowed("user1", current_time=1.0) == True
assert rl.is_allowed("user1", current_time=2.0) == True
assert rl.is_allowed("user1", current_time=3.0) == True
assert rl.is_allowed("user1", current_time=4.0) == False  # Limit hit!
assert rl.is_allowed("user1", current_time=12.0) == True   # Window moved
assert rl.is_allowed("user2", current_time=4.0) == True    # Different user
print("✅ Exercise 22 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 23: Implement a Simple In-Memory Key-Value Store with TTL
# ────────────────────────────────────────────────────────────────────────────
# Like a mini Redis! set(key, value, ttl) and get(key).
# Keys expire after ttl seconds.
#
# Why asked? Tests dict + time handling — real backend design question.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
class KVStore:
    """In-memory key-value store with TTL (Time To Live)."""
    
    def __init__(self):
        self.store = {}      # key → value
        self.expiry = {}     # key → expiry_timestamp
    
    def set(self, key, value, ttl=None, current_time=None):
        if current_time is None:
            current_time = time.time()
        self.store[key] = value
        if ttl is not None:
            self.expiry[key] = current_time + ttl
        elif key in self.expiry:
            del self.expiry[key]
    
    def get(self, key, current_time=None):
        if current_time is None:
            current_time = time.time()
        
        if key not in self.store:
            return None
        
        # Check expiry
        if key in self.expiry and current_time >= self.expiry[key]:
            del self.store[key]
            del self.expiry[key]
            return None
        
        return self.store[key]
    
    def delete(self, key):
        self.store.pop(key, None)
        self.expiry.pop(key, None)

# Test
kv = KVStore()
kv.set("token", "abc123", ttl=5, current_time=10.0)
assert kv.get("token", current_time=12.0) == "abc123"    # Within TTL
assert kv.get("token", current_time=16.0) is None         # Expired!

kv.set("name", "Sid")  # No TTL — never expires
assert kv.get("name", current_time=99999.0) == "Sid"
print("✅ Exercise 23 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 24: Detect Cycle in a Directed Graph (Using Dict + Set)
# ────────────────────────────────────────────────────────────────────────────
# Given a directed graph as adjacency dict, detect if there's a cycle.
# Example: {"A": ["B"], "B": ["C"], "C": ["A"]} → True (A→B→C→A)
#
# Why asked? Tests DFS + graph representation with dicts/sets.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def has_cycle(graph):
    """DFS-based cycle detection using white-gray-black coloring."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {node: WHITE for node in graph}
    
    def dfs(node):
        color[node] = GRAY  # Currently in recursion stack
        for neighbor in graph.get(node, []):
            if color.get(neighbor) == GRAY:  # Back edge = cycle!
                return True
            if color.get(neighbor) == WHITE and dfs(neighbor):
                return True
        color[node] = BLACK  # Fully processed
        return False
    
    for node in graph:
        if color[node] == WHITE:
            if dfs(node):
                return True
    return False

assert has_cycle({"A": ["B"], "B": ["C"], "C": ["A"]}) == True
assert has_cycle({"A": ["B"], "B": ["C"], "C": []}) == False
assert has_cycle({"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}) == False
print("✅ Exercise 24 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 25: Implement a Task Dependency Resolver (Topological Sort)
# ────────────────────────────────────────────────────────────────────────────
# Given tasks with dependencies, return a valid execution order.
# Example: {"build": ["compile"], "compile": ["parse"], "parse": [], "test": ["build"]}
# → ["parse", "compile", "build", "test"]
#
# Why asked? Topological sort — critical for task scheduling in backends.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution (Kahn's Algorithm — BFS-based):
def resolve_dependencies(tasks):
    """Topological sort using Kahn's algorithm (BFS)."""
    # Build in-degree map
    in_degree = {task: 0 for task in tasks}
    for task, deps in tasks.items():
        for dep in deps:
            if dep in in_degree:
                pass  # dep is a dependency, not the task itself
    
    # Reverse graph: dependency → tasks that depend on it
    dependents = defaultdict(list)
    for task, deps in tasks.items():
        for dep in deps:
            dependents[dep].append(task)
            in_degree[task] = in_degree.get(task, 0)
    
    # Recalculate in-degrees properly
    in_degree = {task: 0 for task in tasks}
    for task, deps in tasks.items():
        in_degree[task] = len(deps)
    
    # Start with tasks that have no dependencies
    queue = deque([task for task, deg in in_degree.items() if deg == 0])
    order = []
    
    while queue:
        task = queue.popleft()
        order.append(task)
        for dependent in dependents[task]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)
    
    if len(order) != len(tasks):
        raise ValueError("Circular dependency detected!")
    
    return order

result = resolve_dependencies({
    "build": ["compile"],
    "compile": ["parse"],
    "parse": [],
    "test": ["build"]
})
# Verify ordering constraints
assert result.index("parse") < result.index("compile")
assert result.index("compile") < result.index("build")
assert result.index("build") < result.index("test")
print("✅ Exercise 25 passed")


# ============================================================================
# BONUS: TRICKY INTERVIEW QUESTIONS (Quick Fire Round)
# ============================================================================

print("\n" + "=" * 60)
print("BONUS: TRICKY QUESTIONS — Predict the Output!")
print("=" * 60)

# ────────────────────────────────────────────────────────────────────────────
# Tricky Q1: Mutable Default Argument Gotcha
# ────────────────────────────────────────────────────────────────────────────
print("\n--- Tricky Q1: What's the output? ---")

def append_to(element, target=[]):
    target.append(element)
    return target

r1 = append_to(1)
r2 = append_to(2)
r3 = append_to(3)

print(f"r1 = {r1}")  # [1, 2, 3]  ← NOT [1]!
print(f"r2 = {r2}")  # [1, 2, 3]  ← Same list!
print(f"r3 = {r3}")  # [1, 2, 3]
print("⚠️  Default mutable args are shared across calls! Use None instead.")

# ✅ Correct version:
def append_to_fixed(element, target=None):
    if target is None:
        target = []
    target.append(element)
    return target


# ────────────────────────────────────────────────────────────────────────────
# Tricky Q2: List multiplication trap
# ────────────────────────────────────────────────────────────────────────────
print("\n--- Tricky Q2: What's the output? ---")

grid = [[0] * 3] * 3
grid[0][0] = 1
print(f"grid = {grid}")  # [[1, 0, 0], [1, 0, 0], [1, 0, 0]]
print("⚠️  All rows are the SAME object! Use list comprehension instead.")

# ✅ Correct version:
grid_correct = [[0] * 3 for _ in range(3)]
grid_correct[0][0] = 1
print(f"grid_correct = {grid_correct}")  # [[1, 0, 0], [0, 0, 0], [0, 0, 0]]


# ────────────────────────────────────────────────────────────────────────────
# Tricky Q3: Dictionary key comparison gotcha
# ────────────────────────────────────────────────────────────────────────────
print("\n--- Tricky Q3: What's the output? ---")

d = {True: "yes", 1: "one", 1.0: "one_float"}
print(f"d = {d}")          # {True: 'one_float'}
print(f"len(d) = {len(d)}")  # 1!
print("⚠️  True == 1 == 1.0 and hash(True) == hash(1) == hash(1.0)")
print("   So they're all the SAME key! Last value wins.")


# ────────────────────────────────────────────────────────────────────────────
# Tricky Q4: Tuple with mutable element
# ────────────────────────────────────────────────────────────────────────────
print("\n--- Tricky Q4: What happens? ---")

t = (1, 2, [3, 4])
try:
    t[2].append(5)
    print(f"t = {t}")  # (1, 2, [3, 4, 5]) — the list INSIDE the tuple changed!
    print("⚠️  Tuple is immutable, but its mutable elements CAN change!")
except TypeError:
    print("TypeError raised")

# But this fails:
try:
    t[2] += [6, 7]  # This raises TypeError AND modifies the list!
except TypeError:
    print(f"t after += error = {t}")  # (1, 2, [3, 4, 5, 6, 7])
    print("⚠️  += on tuple element: raises TypeError but STILL modifies the list!")


# ────────────────────────────────────────────────────────────────────────────
# Tricky Q5: set() vs {} and dict ordering
# ────────────────────────────────────────────────────────────────────────────
print("\n--- Tricky Q5: What's the type? ---")

a = {}
b = set()
print(f"type(a) = {type(a)}")  # <class 'dict'>
print(f"type(b) = {type(b)}")  # <class 'set'>
print("⚠️  Empty {} is a DICT, not a set! Use set() for empty set.")

# ============================================================================
# SECTION 7: SHALLOW COPY vs DEEP COPY (Interview Favourite!)
# ============================================================================

# ────────────────────────────────────────────────────────────────────────────
# Exercise 26: Shallow vs Deep Copy — Spot the Bug
# ────────────────────────────────────────────────────────────────────────────
# A developer copies a nested config dict and modifies the copy.
# But the original also changes! Fix it.
#
# Why asked? Extremely common — tests understanding of references vs copies.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
import copy

# THE BUG:
original = {"db": {"host": "localhost", "port": 5432}, "debug": True}

# Shallow copy — nested dicts are still SHARED references!
shallow = original.copy()   # same as copy.copy(original)
shallow["db"]["port"] = 9999
print(f"⚠️  original after shallow copy mutation: {original['db']['port']}")  # 9999!
assert original["db"]["port"] == 9999  # Original was modified!

# THE FIX — Deep copy:
original2 = {"db": {"host": "localhost", "port": 5432}, "debug": True}
deep = copy.deepcopy(original2)
deep["db"]["port"] = 9999
assert original2["db"]["port"] == 5432  # Original is SAFE!
print("✅ Exercise 26 passed — deep copy protects nested data")

# Key rules:
# - list.copy(), dict.copy(), copy.copy() → SHALLOW (top level only)
# - copy.deepcopy() → DEEP (recursive, handles all nesting)
# - Slicing [:] → SHALLOW copy for lists

# ✅ Bonus: Demonstrate with lists
a = [[1, 2], [3, 4]]
b = a[:]             # Shallow copy
b[0].append(99)
assert a[0] == [1, 2, 99]  # a is affected!

c = [[1, 2], [3, 4]]
d = copy.deepcopy(c)
d[0].append(99)
assert c[0] == [1, 2]      # c is safe!
print("✅ Exercise 26 bonus passed — list shallow vs deep")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 27: Copy Pitfall in Function Arguments
# ────────────────────────────────────────────────────────────────────────────
# A function should process user data without modifying the original.
# Identify and fix the bug.
#
# Why asked? Tests real-world defensive programming patterns.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
# BUGGY version — modifies caller's data!
def process_user_buggy(user):
    user["processed"] = True  # Mutates the original dict!
    return user

# FIXED version — make a copy first
def process_user_safe(user):
    user = copy.deepcopy(user)  # Or user.copy() if not nested
    user["processed"] = True
    return user

original_user = {"name": "Sid", "settings": {"theme": "dark"}}
result = process_user_safe(original_user)
assert result["processed"] == True
assert "processed" not in original_user  # Original untouched!
print("✅ Exercise 27 passed")


# ============================================================================
# SECTION 8: LIST AS STACK AND QUEUE
# ============================================================================

# ────────────────────────────────────────────────────────────────────────────
# Exercise 28: Balanced Parentheses (Stack using List)
# ────────────────────────────────────────────────────────────────────────────
# Given a string with ()[]{}braces, check if they are balanced.
# Example: "({[]})" → True, "([)]" → False
#
# Why asked? THE classic stack problem — asked at every company.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def is_balanced(s):
    """Check balanced brackets using list as a stack."""
    stack = []  # list works as stack: append() = push, pop() = pop
    pairs = {")": "(", "]": "[", "}": "{"}
    
    for char in s:
        if char in "({[":
            stack.append(char)  # Push
        elif char in ")}]":
            if not stack or stack[-1] != pairs[char]:
                return False
            stack.pop()  # Pop
    
    return len(stack) == 0

assert is_balanced("({[]})") == True
assert is_balanced("([)]") == False
assert is_balanced("((()))") == True
assert is_balanced("(") == False
assert is_balanced("") == True
print("✅ Exercise 28 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 29: Implement Queue Using Two Stacks
# ────────────────────────────────────────────────────────────────────────────
# Implement a FIFO queue using only two stacks (lists with append/pop).
# enqueue() and dequeue() should work correctly.
#
# Why asked? Classic interview question — tests understanding of both.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
class QueueUsingStacks:
    """FIFO Queue implemented with two stacks (amortized O(1) dequeue)."""
    
    def __init__(self):
        self.stack_in = []   # For enqueue
        self.stack_out = []  # For dequeue
    
    def enqueue(self, item):
        self.stack_in.append(item)
    
    def dequeue(self):
        if not self.stack_out:
            # Transfer all from stack_in to stack_out (reverses order)
            while self.stack_in:
                self.stack_out.append(self.stack_in.pop())
        if not self.stack_out:
            raise IndexError("Queue is empty")
        return self.stack_out.pop()
    
    def is_empty(self):
        return not self.stack_in and not self.stack_out

q = QueueUsingStacks()
q.enqueue(1)
q.enqueue(2)
q.enqueue(3)
assert q.dequeue() == 1  # FIFO: 1 came first
assert q.dequeue() == 2
q.enqueue(4)
assert q.dequeue() == 3
assert q.dequeue() == 4
assert q.is_empty() == True
print("✅ Exercise 29 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 30: Evaluate Reverse Polish Notation (Stack)
# ────────────────────────────────────────────────────────────────────────────
# Evaluate an expression in Reverse Polish Notation (postfix).
# Example: ["2","1","+","3","*"] → ((2+1)*3) = 9
#
# Why asked? Stack application — tests understanding of stack-based eval.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def eval_rpn(tokens):
    """Evaluate Reverse Polish Notation using a stack."""
    stack = []
    ops = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: int(a / b),  # Truncate toward zero
    }
    
    for token in tokens:
        if token in ops:
            b = stack.pop()  # Second operand popped first!
            a = stack.pop()
            stack.append(ops[token](a, b))
        else:
            stack.append(int(token))
    
    return stack[0]

assert eval_rpn(["2", "1", "+", "3", "*"]) == 9
assert eval_rpn(["4", "13", "5", "/", "+"]) == 6
assert eval_rpn(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]) == 22
print("✅ Exercise 30 passed")


# ============================================================================
# SECTION 9: DICT COMPREHENSIONS & MERGE OPERATOR
# ============================================================================

# ────────────────────────────────────────────────────────────────────────────
# Exercise 31: Dict Comprehension — Transform API Data
# ────────────────────────────────────────────────────────────────────────────
# Given a list of user dicts from an API, create lookup dicts.
#
# Why asked? Tests dict comprehension fluency — daily backend task.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
users = [
    {"id": 1, "name": "Alice", "email": "alice@test.com", "active": True},
    {"id": 2, "name": "Bob", "email": "bob@test.com", "active": False},
    {"id": 3, "name": "Charlie", "email": "charlie@test.com", "active": True},
    {"id": 4, "name": "Dave", "email": "dave@test.com", "active": True},
]

# a) Create id → user lookup
id_lookup = {u["id"]: u for u in users}
assert id_lookup[3]["name"] == "Charlie"

# b) Create email → name lookup (only active users)
email_to_name = {u["email"]: u["name"] for u in users if u["active"]}
assert "bob@test.com" not in email_to_name
assert email_to_name["alice@test.com"] == "Alice"

# c) Invert a simple dict using comprehension
status_codes = {200: "OK", 404: "Not Found", 500: "Server Error"}
inverted = {v: k for k, v in status_codes.items()}
assert inverted["OK"] == 200
assert inverted["Not Found"] == 404

# d) Filter dict — keep only keys in a whitelist
config = {"host": "localhost", "port": 5432, "password": "secret", "debug": True}
public_keys = {"host", "port", "debug"}
safe_config = {k: v for k, v in config.items() if k in public_keys}
assert "password" not in safe_config
assert safe_config == {"host": "localhost", "port": 5432, "debug": True}

print("✅ Exercise 31 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 32: Dict Merge Operator | (Python 3.9+)
# ────────────────────────────────────────────────────────────────────────────
# Merge configurations using the | and |= operators.
#
# Why asked? Tests awareness of modern Python features.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
import sys

if sys.version_info >= (3, 9):
    # | creates a NEW merged dict (right side wins on conflicts)
    defaults = {"host": "localhost", "port": 5432, "debug": False}
    overrides = {"port": 8080, "debug": True, "workers": 4}
    
    merged = defaults | overrides
    assert merged == {"host": "localhost", "port": 8080, "debug": True, "workers": 4}
    assert defaults["port"] == 5432  # Original unchanged!
    
    # |= updates in-place (like dict.update() but cleaner)
    settings = {"a": 1, "b": 2}
    settings |= {"b": 99, "c": 3}
    assert settings == {"a": 1, "b": 99, "c": 3}
    
    # Chaining multiple merges
    base = {"env": "dev"}
    local = {"debug": True}
    prod = {"env": "prod", "workers": 8}
    final = base | local | prod  # Last one wins
    assert final == {"env": "prod", "debug": True, "workers": 8}
    
    print("✅ Exercise 32 passed")
else:
    # Fallback for older Python versions
    defaults = {"host": "localhost", "port": 5432, "debug": False}
    overrides = {"port": 8080, "debug": True, "workers": 4}
    merged = {**defaults, **overrides}  # Pre-3.9 way
    assert merged == {"host": "localhost", "port": 8080, "debug": True, "workers": 4}
    print("✅ Exercise 32 passed (using ** unpacking — Python < 3.9)")


# ============================================================================
# SECTION 10: ChainMap (collections)
# ============================================================================

# ────────────────────────────────────────────────────────────────────────────
# Exercise 33: Configuration Priority with ChainMap
# ────────────────────────────────────────────────────────────────────────────
# Implement a layered configuration system where:
#   command-line args > environment vars > config file > defaults
# First found wins.
#
# Why asked? Tests ChainMap knowledge — real-world config pattern.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
from collections import ChainMap

def get_config(cli_args, env_vars, config_file, defaults):
    """Layered config — first dict in chain has highest priority."""
    return ChainMap(cli_args, env_vars, config_file, defaults)

defaults = {"debug": False, "port": 5432, "host": "localhost", "log_level": "INFO"}
config_file = {"port": 8000, "host": "0.0.0.0"}
env_vars = {"debug": True}
cli_args = {"port": 9999}

config = get_config(cli_args, env_vars, config_file, defaults)

assert config["port"] == 9999        # CLI wins
assert config["debug"] == True       # Env wins
assert config["host"] == "0.0.0.0"   # Config file wins
assert config["log_level"] == "INFO" # Falls back to defaults

# ChainMap is a VIEW — modifying it only affects the FIRST dict
config["new_key"] = "value"
assert "new_key" in cli_args  # Added to first mapping!
assert "new_key" not in defaults

# .maps gives you the list of all dicts in order
assert len(config.maps) == 4

# .new_child() adds a new layer on top (useful for scoped overrides)
request_config = config.new_child({"debug": False})
assert request_config["debug"] == False  # New child overrides
assert config["debug"] == True           # Original unchanged

print("✅ Exercise 33 passed")


# ============================================================================
# SECTION 11: FROZENSET
# ============================================================================

# ────────────────────────────────────────────────────────────────────────────
# Exercise 34: Frozenset as Dict Key — Unique Pair/Group Tracking
# ────────────────────────────────────────────────────────────────────────────
# Track unique UNORDERED pairs of users who interacted.
# (Alice, Bob) should be the same as (Bob, Alice).
#
# Why asked? Tests frozenset hashability — relevant for graph/relationship problems.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def count_unique_interactions(interactions):
    """Count unique unordered pairs using frozenset as dict key."""
    pair_counts = {}
    for user1, user2 in interactions:
        pair = frozenset([user1, user2])  # Order doesn't matter!
        pair_counts[pair] = pair_counts.get(pair, 0) + 1
    return pair_counts

interactions = [
    ("Alice", "Bob"),
    ("Bob", "Alice"),      # Same pair as above!
    ("Alice", "Charlie"),
    ("Charlie", "Alice"),  # Same pair as above!
    ("Alice", "Bob"),      # Third interaction between Alice & Bob
]

result = count_unique_interactions(interactions)
assert result[frozenset(["Alice", "Bob"])] == 3
assert result[frozenset(["Alice", "Charlie"])] == 2
assert len(result) == 2  # Only 2 unique pairs
print("✅ Exercise 34 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 35: Frozenset for Unique Combinations / Deduplication
# ────────────────────────────────────────────────────────────────────────────
# Given a list of permission sets, find unique permission combinations.
# Order within each set should not matter.
#
# Why asked? Tests frozenset in a set — common in RBAC/permission systems.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
def unique_permission_sets(user_permissions):
    """Find unique permission combinations regardless of order."""
    unique = set()
    for perms in user_permissions:
        unique.add(frozenset(perms))  # frozenset is hashable → can go in a set!
    return unique

perms = [
    ["read", "write"],
    ["write", "read"],       # Same as first!
    ["read", "write", "admin"],
    ["admin", "write", "read"],  # Same as above!
    ["read"],
]

result = unique_permission_sets(perms)
assert len(result) == 3  # Only 3 unique combinations
assert frozenset(["read", "write"]) in result
assert frozenset(["read"]) in result
print("✅ Exercise 35 passed")


# ============================================================================
# SECTION 12: SET COMPREHENSIONS
# ============================================================================

# ────────────────────────────────────────────────────────────────────────────
# Exercise 36: Set Comprehensions — Data Cleaning
# ────────────────────────────────────────────────────────────────────────────
# Extract and clean unique data from messy inputs.
#
# Why asked? Tests set comprehension syntax + practical data processing.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
# a) Extract unique domains from email list (case-insensitive)
emails = [
    "alice@Gmail.com", "bob@gmail.com", "charlie@Yahoo.COM",
    "dave@gmail.com", "eve@outlook.com", "frank@YAHOO.com"
]
domains = {email.split("@")[1].lower() for email in emails}
assert domains == {"gmail.com", "yahoo.com", "outlook.com"}

# b) Find unique word lengths in a sentence
sentence = "the quick brown fox jumps over the lazy dog"
word_lengths = {len(word) for word in sentence.split()}
assert word_lengths == {3, 4, 5}

# c) Extract unique first characters (uppercased)
names = ["alice", "bob", "anna", "charlie", "Adam", "bella"]
initials = {name[0].upper() for name in names}
assert initials == {"A", "B", "C"}

# d) Set comprehension with condition — find all factors of a number
n = 36
factors = {i for i in range(1, n + 1) if n % i == 0}
assert factors == {1, 2, 3, 4, 6, 9, 12, 18, 36}

print("✅ Exercise 36 passed")


# ============================================================================
# SECTION 13: ARRAY MODULE & ENUM MODULE
# ============================================================================

# ────────────────────────────────────────────────────────────────────────────
# Exercise 37: array Module — Typed Arrays vs Lists
# ────────────────────────────────────────────────────────────────────────────
# Compare memory usage of array vs list for numeric data.
#
# Why asked? Tests awareness of memory-efficient alternatives to lists.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
from array import array
import sys

# array — stores only ONE type, much more memory-efficient for numbers
int_array = array('i', [1, 2, 3, 4, 5])  # 'i' = signed int
float_array = array('d', [1.0, 2.0, 3.0])  # 'd' = double

# Compare memory
int_list = [1, 2, 3, 4, 5]
print(f"  list of 5 ints:  {sys.getsizeof(int_list)} bytes")
print(f"  array of 5 ints: {sys.getsizeof(int_array)} bytes")

# array supports same operations as list (mostly)
int_array.append(6)
int_array.extend([7, 8])
assert list(int_array) == [1, 2, 3, 4, 5, 6, 7, 8]

# But enforces type!
try:
    int_array.append("hello")  # TypeError!
    assert False, "Should have raised TypeError"
except TypeError:
    pass

# Common type codes:
# 'b' = signed char, 'i' = signed int, 'l' = signed long
# 'f' = float, 'd' = double, 'u' = Unicode char

# When to use array vs list:
# - array: Large numeric data, memory-critical, C interop
# - list: Mixed types, general purpose, most of the time

# Convert between them
back_to_list = int_array.tolist()
assert back_to_list == [1, 2, 3, 4, 5, 6, 7, 8]

print("✅ Exercise 37 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 38: Enum — State Machine for Order Status
# ────────────────────────────────────────────────────────────────────────────
# Model an e-commerce order status using Enum. Implement transitions.
#
# Why asked? Enum is standard for backend status fields — very practical.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
from enum import Enum, auto, IntEnum

class OrderStatus(Enum):
    PENDING = auto()
    CONFIRMED = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()
    RETURNED = auto()

# Valid transitions (state machine)
VALID_TRANSITIONS = {
    OrderStatus.PENDING: {OrderStatus.CONFIRMED, OrderStatus.CANCELLED},
    OrderStatus.CONFIRMED: {OrderStatus.SHIPPED, OrderStatus.CANCELLED},
    OrderStatus.SHIPPED: {OrderStatus.DELIVERED},
    OrderStatus.DELIVERED: {OrderStatus.RETURNED},
    OrderStatus.CANCELLED: set(),
    OrderStatus.RETURNED: set(),
}

class Order:
    def __init__(self, order_id):
        self.order_id = order_id
        self.status = OrderStatus.PENDING
    
    def transition(self, new_status):
        if new_status not in VALID_TRANSITIONS[self.status]:
            raise ValueError(
                f"Cannot transition from {self.status.name} to {new_status.name}"
            )
        self.status = new_status

# Test valid transitions
order = Order("ORD-001")
assert order.status == OrderStatus.PENDING
order.transition(OrderStatus.CONFIRMED)
assert order.status == OrderStatus.CONFIRMED
order.transition(OrderStatus.SHIPPED)
order.transition(OrderStatus.DELIVERED)
assert order.status == OrderStatus.DELIVERED

# Test invalid transition
order2 = Order("ORD-002")
try:
    order2.transition(OrderStatus.DELIVERED)  # Can't jump from PENDING to DELIVERED!
    assert False, "Should have raised ValueError"
except ValueError as e:
    assert "Cannot transition" in str(e)

# Enum features interviewers might ask about:
assert OrderStatus.PENDING.name == "PENDING"       # String name
assert OrderStatus.PENDING.value == 1              # Auto-assigned value
assert OrderStatus["SHIPPED"] == OrderStatus.SHIPPED  # Access by name
assert OrderStatus(3) == OrderStatus.SHIPPED          # Access by value

# Iteration
all_statuses = [s.name for s in OrderStatus]
assert len(all_statuses) == 6

# Comparison — Enum members use `is`, not `==` (though == works)
assert order.status is OrderStatus.DELIVERED

print("✅ Exercise 38 passed")


# ────────────────────────────────────────────────────────────────────────────
# Exercise 39: IntEnum for HTTP Status Codes
# ────────────────────────────────────────────────────────────────────────────
# Use IntEnum for HTTP codes — they can be compared with ints.
#
# Why asked? HTTP status handling is core backend knowledge.
# ────────────────────────────────────────────────────────────────────────────

# YOUR SOLUTION HERE:




# ✅ Solution:
class HTTPStatus(IntEnum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500

def categorize_response(status_code):
    """Categorize HTTP response using IntEnum."""
    try:
        status = HTTPStatus(status_code)
        name = status.name
    except ValueError:
        name = "UNKNOWN"
    
    if 200 <= status_code < 300:
        return "success", name
    elif 400 <= status_code < 500:
        return "client_error", name
    elif 500 <= status_code < 600:
        return "server_error", name
    else:
        return "other", name

# IntEnum can be compared with plain ints!
assert HTTPStatus.OK == 200
assert HTTPStatus.NOT_FOUND > 400

category, name = categorize_response(404)
assert category == "client_error"
assert name == "NOT_FOUND"

category, name = categorize_response(200)
assert category == "success"

# Use in dict/set (IntEnum is hashable)
error_counts = {HTTPStatus.NOT_FOUND: 42, HTTPStatus.INTERNAL_SERVER_ERROR: 3}
assert error_counts[HTTPStatus.NOT_FOUND] == 42
assert error_counts[404] == 42  # Works with plain int too!

print("✅ Exercise 39 passed")


# ============================================================================
# BONUS ROUND 2: MORE TRICKY QUESTIONS
# ============================================================================

print("\n" + "=" * 60)
print("BONUS ROUND 2: MORE TRICKY QUESTIONS")
print("=" * 60)

# ────────────────────────────────────────────────────────────────────────────
# Tricky Q6: Shallow copy with list comprehension
# ────────────────────────────────────────────────────────────────────────────
print("\n--- Tricky Q6: Is this a deep copy? ---")

original = [[1, 2], [3, 4]]
copied = [row[:] for row in original]  # Copies each inner list!
copied[0].append(99)
print(f"original = {original}")    # [[1, 2], [3, 4]] — Safe!
print(f"copied = {copied}")       # [[1, 2, 99], [3, 4]]
print("✅ [row[:] for row in original] IS effectively a deep copy for 2D lists")
print("   But NOT for deeper nesting — use copy.deepcopy() for 3+ levels")

# ────────────────────────────────────────────────────────────────────────────
# Tricky Q7: dict.fromkeys() with mutable default
# ────────────────────────────────────────────────────────────────────────────
print("\n--- Tricky Q7: What's the output? ---")

d = dict.fromkeys(["a", "b", "c"], [])
d["a"].append(1)
print(f"d = {d}")  # {'a': [1], 'b': [1], 'c': [1]} — ALL share same list!
print("⚠️  dict.fromkeys() shares the SAME default object!")
print("   Use dict comprehension instead: {k: [] for k in keys}")

# ✅ Correct:
d_correct = {k: [] for k in ["a", "b", "c"]}
d_correct["a"].append(1)
assert d_correct == {"a": [1], "b": [], "c": []}

# ────────────────────────────────────────────────────────────────────────────
# Tricky Q8: Set ordering surprise
# ────────────────────────────────────────────────────────────────────────────
print("\n--- Tricky Q8: Are these equal? ---")

s1 = {1, 2, 3}
s2 = {3, 2, 1}
print(f"s1 == s2: {s1 == s2}")  # True — sets don't care about order!
print(f"But list(s1) == list(s2): might be True or False — order is implementation-defined")

# ────────────────────────────────────────────────────────────────────────────
# Tricky Q9: Enum identity vs equality
# ────────────────────────────────────────────────────────────────────────────
print("\n--- Tricky Q9: Enum comparison ---")

class Color(Enum):
    RED = 1

print(f"Color.RED == 1: {Color.RED == 1}")        # False! Enum != int
print(f"Color.RED.value == 1: {Color.RED.value == 1}")  # True
print("⚠️  Regular Enum does NOT compare with int. Use IntEnum if you need that.")

print("\n" + "=" * 60)
print("🎉 ALL 39 EXERCISES + 9 TRICKY QUESTIONS COMPLETED! 🎉")
print("   Full Phase 2 Data Structures coverage achieved.")
print("=" * 60)
