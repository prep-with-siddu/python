# 12 — Coding Round — Interview Questions & Patterns

> **40+ coding problems covering DSA patterns, time/space complexity, common interview problems**

---

## 🔹 Section 1: Array & String Patterns

### Q1. 🟢 Two Sum

**Problem:** Find two numbers that add up to target.

```python
# Brute force: O(n²)
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]

# Optimal: O(n) — Hash Map
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# Test
print(two_sum([2, 7, 11, 15], 9))  # [0, 1]
```

---

### Q2. 🟢 Reverse a String

```python
# Method 1: Slicing
def reverse_string(s):
    return s[::-1]

# Method 2: Two pointers (in-place for list)
def reverse_string(s):
    s = list(s)
    left, right = 0, len(s) - 1
    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
    return ''.join(s)

# Method 3: Recursion
def reverse_string(s):
    if len(s) <= 1:
        return s
    return reverse_string(s[1:]) + s[0]
```

---

### Q3. 🟡 Longest Substring Without Repeating Characters

```python
# Sliding Window: O(n)
def length_of_longest_substring(s):
    seen = {}
    left = 0
    max_len = 0
    
    for right, char in enumerate(s):
        if char in seen and seen[char] >= left:
            left = seen[char] + 1
        seen[char] = right
        max_len = max(max_len, right - left + 1)
    
    return max_len

# Test
print(length_of_longest_substring("abcabcbb"))  # 3 ("abc")
print(length_of_longest_substring("bbbbb"))      # 1 ("b")
```

---

### Q4. 🟡 Valid Anagram

```python
from collections import Counter

def is_anagram(s, t):
    return Counter(s) == Counter(t)

# Without Counter
def is_anagram(s, t):
    if len(s) != len(t):
        return False
    count = {}
    for c in s:
        count[c] = count.get(c, 0) + 1
    for c in t:
        count[c] = count.get(c, 0) - 1
        if count[c] < 0:
            return False
    return True

print(is_anagram("listen", "silent"))  # True
```

---

### Q5. 🟡 Group Anagrams

```python
from collections import defaultdict

def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = ''.join(sorted(s))
        groups[key].append(s)
    return list(groups.values())

# Alternative: tuple of char counts as key (faster)
def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1
        groups[tuple(count)].append(s)
    return list(groups.values())

print(group_anagrams(["eat","tea","tan","ate","nat","bat"]))
# [["eat","tea","ate"], ["tan","nat"], ["bat"]]
```

---

## 🔹 Section 2: Linked List

### Q6. 🟡 Reverse a Linked List

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Iterative: O(n) time, O(1) space
def reverse_list(head):
    prev = None
    curr = head
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node
    return prev

# Recursive
def reverse_list(head):
    if not head or not head.next:
        return head
    new_head = reverse_list(head.next)
    head.next.next = head
    head.next = None
    return new_head
```

---

### Q7. 🟡 Detect Cycle in Linked List

```python
# Floyd's Tortoise and Hare: O(n) time, O(1) space
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False

# Find cycle start
def detect_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            # Move one pointer to head
            slow = head
            while slow != fast:
                slow = slow.next
                fast = fast.next
            return slow  # Cycle start
    return None
```

---

## 🔹 Section 3: Stack & Queue

### Q8. 🟢 Valid Parentheses

```python
def is_valid(s):
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()
        else:
            stack.append(char)
    
    return len(stack) == 0

print(is_valid("()[]{}"))   # True
print(is_valid("(]"))       # False
print(is_valid("([)]"))     # False
```

---

### Q9. 🟡 Min Stack

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []
    
    def push(self, val):
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)
    
    def pop(self):
        val = self.stack.pop()
        if val == self.min_stack[-1]:
            self.min_stack.pop()
        return val
    
    def getMin(self):
        return self.min_stack[-1]  # O(1)
```

---

## 🔹 Section 4: Hash Map Patterns

### Q10. 🟡 LRU Cache

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # Remove oldest

cache = LRUCache(2)
cache.put(1, "a")
cache.put(2, "b")
cache.get(1)       # "a" — 1 is now most recent
cache.put(3, "c")  # Evicts key 2
```

---

### Q11. 🟡 Top K Frequent Elements

```python
from collections import Counter
import heapq

def top_k_frequent(nums, k):
    count = Counter(nums)
    return heapq.nlargest(k, count.keys(), key=count.get)

# Bucket sort approach: O(n)
def top_k_frequent(nums, k):
    count = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    
    for num, freq in count.items():
        buckets[freq].append(num)
    
    result = []
    for i in range(len(buckets) - 1, 0, -1):
        for num in buckets[i]:
            result.append(num)
            if len(result) == k:
                return result

print(top_k_frequent([1,1,1,2,2,3], 2))  # [1, 2]
```

---

## 🔹 Section 5: Binary Search

### Q12. 🟢 Binary Search

```python
def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Time: O(log n), Space: O(1)
```

---

### Q13. 🟡 Search in Rotated Sorted Array

```python
def search(nums, target):
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        
        # Left half is sorted
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        # Right half is sorted
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return -1

print(search([4,5,6,7,0,1,2], 0))  # 4
```

---

## 🔹 Section 6: Tree Problems

### Q14. 🟢 Maximum Depth of Binary Tree

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Recursive: O(n)
def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))

# Iterative (BFS)
from collections import deque

def max_depth(root):
    if not root:
        return 0
    queue = deque([root])
    depth = 0
    while queue:
        depth += 1
        for _ in range(len(queue)):
            node = queue.popleft()
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    return depth
```

---

### Q15. 🟡 Validate Binary Search Tree

```python
def is_valid_bst(root, min_val=float('-inf'), max_val=float('inf')):
    if not root:
        return True
    if root.val <= min_val or root.val >= max_val:
        return False
    return (is_valid_bst(root.left, min_val, root.val) and
            is_valid_bst(root.right, root.val, max_val))
```

---

### Q16. 🟡 Level Order Traversal (BFS)

```python
from collections import deque

def level_order(root):
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    
    return result

# Output: [[3], [9, 20], [15, 7]]
```

---

## 🔹 Section 7: Dynamic Programming

### Q17. 🟡 Fibonacci — DP approaches

```python
# 1. Recursive (exponential — bad)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)  # O(2^n)

# 2. Memoization (top-down DP)
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)  # O(n)

# 3. Tabulation (bottom-up DP)
def fib(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]  # O(n) time, O(n) space

# 4. Optimized (constant space)
def fib(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b  # O(n) time, O(1) space
```

---

### Q18. 🟡 Climbing Stairs

```python
# Ways to climb n stairs (1 or 2 steps at a time)
def climb_stairs(n):
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b

print(climb_stairs(5))  # 8
# (1+1+1+1+1), (1+1+1+2), (1+1+2+1), (1+2+1+1), (2+1+1+1),
# (1+2+2), (2+1+2), (2+2+1)
```

---

### Q19. 🔴 Longest Common Subsequence

```python
def lcs(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]

print(lcs("abcde", "ace"))  # 3 ("ace")
```

---

## 🔹 Section 8: Graph Problems

### Q20. 🟡 BFS and DFS

```python
from collections import deque

# Graph as adjacency list
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [], 'E': [], 'F': []
}

# BFS — Level by level (Queue)
def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return result

# DFS — Go deep first (Stack/Recursion)
def dfs(graph, node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    result = [node]
    for neighbor in graph[node]:
        if neighbor not in visited:
            result.extend(dfs(graph, neighbor, visited))
    return result

print(bfs(graph, 'A'))  # ['A', 'B', 'C', 'D', 'E', 'F']
print(dfs(graph, 'A'))  # ['A', 'B', 'D', 'E', 'C', 'F']
```

---

### Q21. 🟡 Number of Islands

```python
def num_islands(grid):
    if not grid:
        return 0
    
    rows, cols = len(grid), len(grid[0])
    count = 0
    
    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0':
            return
        grid[r][c] = '0'  # Mark visited
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
    
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)
    
    return count

grid = [
    ["1","1","0","0","0"],
    ["1","1","0","0","0"],
    ["0","0","1","0","0"],
    ["0","0","0","1","1"]
]
print(num_islands(grid))  # 3
```

---

## 🔹 Section 9: Sorting

### Q22. 🟡 Merge Sort

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Time: O(n log n), Space: O(n)
```

---

### Q23. 🟡 Quick Sort

```python
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)

# Time: O(n log n) avg, O(n²) worst
# Space: O(log n)
```

---

## 🔹 Section 10: Common Backend Coding Problems

### Q24. 🟡 Implement a Rate Limiter (Sliding Window)

```python
import time
from collections import deque

class SlidingWindowRateLimiter:
    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window = window_seconds
        self.requests = {}  # client_id -> deque of timestamps
    
    def is_allowed(self, client_id):
        now = time.time()
        if client_id not in self.requests:
            self.requests[client_id] = deque()
        
        window = self.requests[client_id]
        
        # Remove expired timestamps
        while window and window[0] <= now - self.window:
            window.popleft()
        
        if len(window) < self.max_requests:
            window.append(now)
            return True
        return False

# Test
limiter = SlidingWindowRateLimiter(max_requests=5, window_seconds=60)
for i in range(7):
    print(f"Request {i+1}: {limiter.is_allowed('user1')}")
# True, True, True, True, True, False, False
```

---

### Q25. 🟡 Implement a URL Shortener

```python
import hashlib
import string

class URLShortener:
    BASE62 = string.ascii_letters + string.digits
    
    def __init__(self):
        self.url_map = {}    # short -> long
        self.counter = 0
    
    def encode(self, long_url):
        self.counter += 1
        short_code = self._to_base62(self.counter)
        self.url_map[short_code] = long_url
        return f"https://short.ly/{short_code}"
    
    def decode(self, short_url):
        code = short_url.split("/")[-1]
        return self.url_map.get(code)
    
    def _to_base62(self, num):
        if num == 0:
            return self.BASE62[0]
        result = []
        while num:
            result.append(self.BASE62[num % 62])
            num //= 62
        return ''.join(reversed(result))

shortener = URLShortener()
short = shortener.encode("https://example.com/very/long/url")
print(short)                   # https://short.ly/b
print(shortener.decode(short)) # https://example.com/very/long/url
```

---

### Q26. 🟡 Flatten a Nested Dictionary

```python
def flatten_dict(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

nested = {
    "a": 1,
    "b": {
        "c": 2,
        "d": {
            "e": 3
        }
    }
}
print(flatten_dict(nested))
# {'a': 1, 'b.c': 2, 'b.d.e': 3}
```

---

### Q27. 🟡 Implement a Simple Task Scheduler

```python
import heapq
import time

class TaskScheduler:
    def __init__(self):
        self.tasks = []  # min-heap of (priority, timestamp, task)
        self.counter = 0
    
    def add_task(self, task, priority=0):
        self.counter += 1
        heapq.heappush(self.tasks, (priority, self.counter, task))
    
    def get_next_task(self):
        if self.tasks:
            priority, _, task = heapq.heappop(self.tasks)
            return task
        return None

scheduler = TaskScheduler()
scheduler.add_task("Send email", priority=2)
scheduler.add_task("Process payment", priority=1)  # Higher priority
scheduler.add_task("Log analytics", priority=3)

print(scheduler.get_next_task())  # "Process payment"
print(scheduler.get_next_task())  # "Send email"
print(scheduler.get_next_task())  # "Log analytics"
```

---

## 🔹 Section 11: Time & Space Complexity Cheat Sheet

| Structure/Algorithm | Access | Search | Insert | Delete |
|--------------------|--------|--------|--------|--------|
| Array | O(1) | O(n) | O(n) | O(n) |
| Linked List | O(n) | O(n) | O(1) | O(1) |
| Hash Map | - | O(1) avg | O(1) avg | O(1) avg |
| BST | - | O(log n) | O(log n) | O(log n) |
| Heap | - | O(n) | O(log n) | O(log n) |

| Algorithm | Time | Space |
|-----------|------|-------|
| Binary Search | O(log n) | O(1) |
| Merge Sort | O(n log n) | O(n) |
| Quick Sort | O(n log n) avg | O(log n) |
| BFS/DFS | O(V + E) | O(V) |
| Dijkstra | O(E log V) | O(V) |

---

## 🔹 Quick Revision — Must-Know Patterns

| # | Pattern | Example Problem |
|---|---------|----------------|
| 1 | **Two Pointers** | Two Sum (sorted), palindrome check |
| 2 | **Sliding Window** | Longest substring, max subarray |
| 3 | **Hash Map** | Frequency count, two sum, anagrams |
| 4 | **Binary Search** | Search sorted array, find boundary |
| 5 | **BFS/DFS** | Tree traversal, graph search, islands |
| 6 | **Dynamic Programming** | Fibonacci, climbing stairs, LCS |
| 7 | **Stack** | Valid parentheses, min stack |
| 8 | **Heap** | Top K elements, merge K lists |
| 9 | **Recursion** | Tree problems, backtracking |
| 10 | **Greedy** | Interval scheduling, activity selection |

---

*This completes the Interview Preparation series! Good luck, Sid! 🚀*
