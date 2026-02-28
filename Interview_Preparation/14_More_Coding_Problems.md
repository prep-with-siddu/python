# 14 — More Coding Problems (Pattern-Wise) — Interview Questions

> **50+ additional coding problems organized by pattern — practice these to build muscle memory**

---

## 🔹 Pattern 1: Two Pointers

### Q1. 🟢 Remove Duplicates from Sorted Array (in-place)

```python
def remove_duplicates(nums):
    if not nums:
        return 0
    i = 0
    for j in range(1, len(nums)):
        if nums[j] != nums[i]:
            i += 1
            nums[i] = nums[j]
    return i + 1

nums = [1, 1, 2, 2, 3]
k = remove_duplicates(nums)
print(nums[:k])  # [1, 2, 3]
```

---

### Q2. 🟢 Valid Palindrome

```python
def is_palindrome(s):
    s = ''.join(c.lower() for c in s if c.isalnum())
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

print(is_palindrome("A man, a plan, a canal: Panama"))  # True
```

---

### Q3. 🟡 Container With Most Water

```python
def max_area(height):
    left, right = 0, len(height) - 1
    max_water = 0
    
    while left < right:
        width = right - left
        h = min(height[left], height[right])
        max_water = max(max_water, width * h)
        
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_water

print(max_area([1,8,6,2,5,4,8,3,7]))  # 49
```

---

### Q4. 🟡 3Sum (Find triplets that sum to 0)

```python
def three_sum(nums):
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:  # Skip duplicates
            continue
        
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
    
    return result

print(three_sum([-1, 0, 1, 2, -1, -4]))  # [[-1,-1,2], [-1,0,1]]
```

---

### Q5. 🟡 Trapping Rain Water

```python
def trap(height):
    left, right = 0, len(height) - 1
    left_max = right_max = 0
    water = 0
    
    while left < right:
        if height[left] < height[right]:
            if height[left] >= left_max:
                left_max = height[left]
            else:
                water += left_max - height[left]
            left += 1
        else:
            if height[right] >= right_max:
                right_max = height[right]
            else:
                water += right_max - height[right]
            right -= 1
    
    return water

print(trap([0,1,0,2,1,0,1,3,2,1,2,1]))  # 6
```

---

## 🔹 Pattern 2: Sliding Window

### Q6. 🟡 Maximum Subarray Sum (Kadane's Algorithm)

```python
def max_subarray(nums):
    max_sum = current_sum = nums[0]
    
    for num in nums[1:]:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    
    return max_sum

print(max_subarray([-2,1,-3,4,-1,2,1,-5,4]))  # 6 ([4,-1,2,1])
```

---

### Q7. 🟡 Minimum Window Substring

```python
from collections import Counter

def min_window(s, t):
    if not s or not t:
        return ""
    
    need = Counter(t)
    have = {}
    formed = 0
    required = len(need)
    
    result = ""
    min_len = float('inf')
    left = 0
    
    for right in range(len(s)):
        char = s[right]
        have[char] = have.get(char, 0) + 1
        
        if char in need and have[char] == need[char]:
            formed += 1
        
        while formed == required:
            # Update result
            if right - left + 1 < min_len:
                min_len = right - left + 1
                result = s[left:right + 1]
            
            # Shrink window
            have[s[left]] -= 1
            if s[left] in need and have[s[left]] < need[s[left]]:
                formed -= 1
            left += 1
    
    return result

print(min_window("ADOBECODEBANC", "ABC"))  # "BANC"
```

---

### Q8. 🟡 Subarray Sum Equals K

```python
def subarray_sum(nums, k):
    count = 0
    prefix_sum = 0
    seen = {0: 1}  # prefix_sum → count
    
    for num in nums:
        prefix_sum += num
        if prefix_sum - k in seen:
            count += seen[prefix_sum - k]
        seen[prefix_sum] = seen.get(prefix_sum, 0) + 1
    
    return count

print(subarray_sum([1, 1, 1], 2))  # 2
print(subarray_sum([1, 2, 3], 3))  # 2 ([1,2] and [3])
```

---

## 🔹 Pattern 3: Binary Search Variations

### Q9. 🟡 Find First and Last Position in Sorted Array

```python
def search_range(nums, target):
    def find_bound(is_left):
        left, right = 0, len(nums) - 1
        result = -1
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                result = mid
                if is_left:
                    right = mid - 1  # Keep searching left
                else:
                    left = mid + 1   # Keep searching right
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return result
    
    return [find_bound(True), find_bound(False)]

print(search_range([5,7,7,8,8,10], 8))  # [3, 4]
```

---

### Q10. 🟡 Find Peak Element

```python
def find_peak(nums):
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[mid + 1]:
            right = mid      # Peak is on left side (or mid)
        else:
            left = mid + 1   # Peak is on right side
    return left

print(find_peak([1, 2, 3, 1]))  # 2 (index of 3)
```

---

### Q11. 🟡 Koko Eating Bananas (Binary Search on Answer)

```python
import math

def min_eating_speed(piles, h):
    left, right = 1, max(piles)
    
    while left < right:
        mid = (left + right) // 2
        hours = sum(math.ceil(p / mid) for p in piles)
        
        if hours <= h:
            right = mid     # Try slower speed
        else:
            left = mid + 1  # Need faster speed
    
    return left

print(min_eating_speed([3,6,7,11], 8))  # 4
```

---

## 🔹 Pattern 4: Stack Problems

### Q12. 🟡 Daily Temperatures (Next Greater Element)

```python
def daily_temperatures(temps):
    n = len(temps)
    result = [0] * n
    stack = []  # Indices of temps waiting for a warmer day
    
    for i, temp in enumerate(temps):
        while stack and temps[stack[-1]] < temp:
            prev = stack.pop()
            result[prev] = i - prev
        stack.append(i)
    
    return result

print(daily_temperatures([73,74,75,71,69,72,76,73]))
# [1, 1, 4, 2, 1, 1, 0, 0]
```

---

### Q13. 🟡 Evaluate Reverse Polish Notation

```python
def eval_rpn(tokens):
    stack = []
    ops = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: int(a / b),  # Truncate towards zero
    }
    
    for token in tokens:
        if token in ops:
            b, a = stack.pop(), stack.pop()
            stack.append(ops[token](a, b))
        else:
            stack.append(int(token))
    
    return stack[0]

print(eval_rpn(["2","1","+","3","*"]))  # 9 → ((2+1)*3)
```

---

### Q14. 🟡 Largest Rectangle in Histogram

```python
def largest_rectangle(heights):
    stack = []  # Indices
    max_area = 0
    
    for i, h in enumerate(heights + [0]):  # Add sentinel
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    
    return max_area

print(largest_rectangle([2,1,5,6,2,3]))  # 10
```

---

## 🔹 Pattern 5: Tree Problems

### Q15. 🟡 Lowest Common Ancestor (BST)

```python
def lca_bst(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root  # Split point = LCA
```

---

### Q16. 🟡 Lowest Common Ancestor (Binary Tree)

```python
def lca(root, p, q):
    if not root or root == p or root == q:
        return root
    
    left = lca(root.left, p, q)
    right = lca(root.right, p, q)
    
    if left and right:
        return root     # p and q on different sides
    return left or right  # Both on same side
```

---

### Q17. 🟡 Serialize and Deserialize Binary Tree

```python
class Codec:
    def serialize(self, root):
        if not root:
            return "null"
        return f"{root.val},{self.serialize(root.left)},{self.serialize(root.right)}"
    
    def deserialize(self, data):
        self.nodes = iter(data.split(","))
        return self._build()
    
    def _build(self):
        val = next(self.nodes)
        if val == "null":
            return None
        node = TreeNode(int(val))
        node.left = self._build()
        node.right = self._build()
        return node
```

---

### Q18. 🟡 Invert Binary Tree

```python
def invert_tree(root):
    if not root:
        return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root
```

---

## 🔹 Pattern 6: Dynamic Programming

### Q19. 🟡 Coin Change (Min coins)

```python
def coin_change(coins, amount):
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1

print(coin_change([1, 5, 10, 25], 30))  # 2 (25 + 5)
```

---

### Q20. 🟡 House Robber (Can't rob adjacent houses)

```python
def rob(nums):
    if not nums:
        return 0
    if len(nums) <= 2:
        return max(nums)
    
    dp = [0] * len(nums)
    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])
    
    for i in range(2, len(nums)):
        dp[i] = max(dp[i - 1], dp[i - 2] + nums[i])
    
    return dp[-1]

# Space optimized
def rob(nums):
    prev2 = prev1 = 0
    for num in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + num)
    return prev1

print(rob([2, 7, 9, 3, 1]))  # 12 (2 + 9 + 1)
```

---

### Q21. 🟡 Longest Increasing Subsequence

```python
# DP: O(n²)
def length_of_lis(nums):
    if not nums:
        return 0
    dp = [1] * len(nums)
    
    for i in range(1, len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)

# Binary Search: O(n log n)
import bisect

def length_of_lis(nums):
    tails = []
    for num in nums:
        pos = bisect.bisect_left(tails, num)
        if pos == len(tails):
            tails.append(num)
        else:
            tails[pos] = num
    return len(tails)

print(length_of_lis([10,9,2,5,3,7,101,18]))  # 4 ([2,3,7,101])
```

---

### Q22. 🔴 Word Break

```python
def word_break(s, word_dict):
    word_set = set(word_dict)
    dp = [False] * (len(s) + 1)
    dp[0] = True
    
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    
    return dp[len(s)]

print(word_break("leetcode", ["leet", "code"]))  # True
print(word_break("applepenapple", ["apple", "pen"]))  # True
```

---

### Q23. 🔴 0/1 Knapsack

```python
def knapsack(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]  # Don't take item
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w], 
                              dp[i - 1][w - weights[i - 1]] + values[i - 1])
    
    return dp[n][capacity]

print(knapsack([1, 3, 4, 5], [1, 4, 5, 7], 7))  # 9
```

---

## 🔹 Pattern 7: Graph Problems

### Q24. 🟡 Course Schedule (Cycle Detection)

```python
from collections import defaultdict, deque

def can_finish(num_courses, prerequisites):
    # Topological sort (Kahn's algorithm)
    graph = defaultdict(list)
    in_degree = [0] * num_courses
    
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    
    queue = deque(i for i in range(num_courses) if in_degree[i] == 0)
    completed = 0
    
    while queue:
        node = queue.popleft()
        completed += 1
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    return completed == num_courses

print(can_finish(2, [[1,0]]))        # True
print(can_finish(2, [[1,0],[0,1]]))  # False (cycle)
```

---

### Q25. 🟡 Clone Graph (Deep Copy)

```python
def clone_graph(node):
    if not node:
        return None
    
    clones = {}
    
    def dfs(node):
        if node in clones:
            return clones[node]
        
        clone = Node(node.val)
        clones[node] = clone
        
        for neighbor in node.neighbors:
            clone.neighbors.append(dfs(neighbor))
        
        return clone
    
    return dfs(node)
```

---

### Q26. 🔴 Dijkstra's Shortest Path

```python
import heapq
from collections import defaultdict

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    heap = [(0, start)]
    
    while heap:
        dist, node = heapq.heappop(heap)
        if dist > distances[node]:
            continue
        
        for neighbor, weight in graph[node]:
            new_dist = dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))
    
    return distances

graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('C', 2), ('D', 6)],
    'C': [('D', 3)],
    'D': []
}
print(dijkstra(graph, 'A'))  # {'A': 0, 'B': 1, 'C': 3, 'D': 6}
```

---

## 🔹 Pattern 8: Backtracking

### Q27. 🟡 Permutations

```python
def permutations(nums):
    result = []
    
    def backtrack(path, remaining):
        if not remaining:
            result.append(path[:])
            return
        for i in range(len(remaining)):
            path.append(remaining[i])
            backtrack(path, remaining[:i] + remaining[i+1:])
            path.pop()
    
    backtrack([], nums)
    return result

print(permutations([1, 2, 3]))
# [[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]]
```

---

### Q28. 🟡 Subsets (Power Set)

```python
def subsets(nums):
    result = []
    
    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()
    
    backtrack(0, [])
    return result

print(subsets([1, 2, 3]))
# [[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]]
```

---

### Q29. 🟡 Combination Sum

```python
def combination_sum(candidates, target):
    result = []
    
    def backtrack(start, path, remaining):
        if remaining == 0:
            result.append(path[:])
            return
        if remaining < 0:
            return
        
        for i in range(start, len(candidates)):
            path.append(candidates[i])
            backtrack(i, path, remaining - candidates[i])  # Can reuse
            path.pop()
    
    backtrack(0, [], target)
    return result

print(combination_sum([2, 3, 6, 7], 7))  # [[2,2,3], [7]]
```

---

### Q30. 🔴 N-Queens

```python
def solve_n_queens(n):
    result = []
    board = [['.' ] * n for _ in range(n)]
    
    def is_safe(row, col):
        for i in range(row):
            if board[i][col] == 'Q':
                return False
        for i, j in zip(range(row-1, -1, -1), range(col-1, -1, -1)):
            if board[i][j] == 'Q':
                return False
        for i, j in zip(range(row-1, -1, -1), range(col+1, n)):
            if board[i][j] == 'Q':
                return False
        return True
    
    def backtrack(row):
        if row == n:
            result.append([''.join(r) for r in board])
            return
        for col in range(n):
            if is_safe(row, col):
                board[row][col] = 'Q'
                backtrack(row + 1)
                board[row][col] = '.'
    
    backtrack(0)
    return result

print(len(solve_n_queens(8)))  # 92 solutions
```

---

## 🔹 Pattern 9: Heap / Priority Queue

### Q31. 🟡 Merge K Sorted Lists

```python
import heapq

def merge_k_lists(lists):
    heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))
    
    result = []
    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
    
    return result

print(merge_k_lists([[1,4,5], [1,3,4], [2,6]]))
# [1, 1, 2, 3, 4, 4, 5, 6]
```

---

### Q32. 🟡 Find Median from Data Stream

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.small = []  # Max heap (negate values)
        self.large = []  # Min heap
    
    def add_num(self, num):
        heapq.heappush(self.small, -num)
        
        # Ensure max of small <= min of large
        if self.small and self.large and -self.small[0] > self.large[0]:
            heapq.heappush(self.large, -heapq.heappop(self.small))
        
        # Balance sizes
        if len(self.small) > len(self.large) + 1:
            heapq.heappush(self.large, -heapq.heappop(self.small))
        elif len(self.large) > len(self.small) + 1:
            heapq.heappush(self.small, -heapq.heappop(self.large))
    
    def find_median(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        elif len(self.large) > len(self.small):
            return self.large[0]
        return (-self.small[0] + self.large[0]) / 2

mf = MedianFinder()
mf.add_num(1); mf.add_num(2)
print(mf.find_median())  # 1.5
mf.add_num(3)
print(mf.find_median())  # 2
```

---

## 🔹 Pattern 10: Greedy

### Q33. 🟡 Jump Game

```python
def can_jump(nums):
    max_reach = 0
    for i, jump in enumerate(nums):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + jump)
    return True

print(can_jump([2, 3, 1, 1, 4]))  # True
print(can_jump([3, 2, 1, 0, 4]))  # False
```

---

### Q34. 🟡 Merge Intervals

```python
def merge_intervals(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    
    return merged

print(merge_intervals([[1,3],[2,6],[8,10],[15,18]]))
# [[1,6], [8,10], [15,18]]
```

---

### Q35. 🟡 Task Scheduler

```python
from collections import Counter

def least_interval(tasks, n):
    counts = Counter(tasks)
    max_count = max(counts.values())
    max_count_tasks = sum(1 for c in counts.values() if c == max_count)
    
    result = (max_count - 1) * (n + 1) + max_count_tasks
    return max(result, len(tasks))

print(least_interval(["A","A","A","B","B","B"], 2))  # 8
# A B _ A B _ A B
```

---

## 🔹 Pattern 11: Trie

### Q36. 🟡 Implement Trie (Prefix Tree)

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word):
        node = self._find(word)
        return node is not None and node.is_end
    
    def starts_with(self, prefix):
        return self._find(prefix) is not None
    
    def _find(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

trie = Trie()
trie.insert("apple")
print(trie.search("apple"))      # True
print(trie.search("app"))        # False
print(trie.starts_with("app"))   # True
```

---

## 🔹 Pattern 12: Bit Manipulation

### Q37. 🟢 Single Number (every element appears twice except one)

```python
def single_number(nums):
    result = 0
    for num in nums:
        result ^= num  # XOR cancels duplicates
    return result

print(single_number([4, 1, 2, 1, 2]))  # 4
```

---

### Q38. 🟡 Count Set Bits (Number of 1s)

```python
def count_bits(n):
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count

# Brian Kernighan's trick
def count_bits(n):
    count = 0
    while n:
        n &= (n - 1)  # Removes lowest set bit
        count += 1
    return count

print(count_bits(11))  # 3 (1011 in binary)
```

---

## 🔹 Pattern Summary — Which Pattern to Use?

| If you see... | Think... | Pattern |
|--------------|---------|---------|
| Sorted array | Binary search | Binary Search |
| Subarray/substring | Sliding window | Sliding Window |
| Two arrays/sorted | Two pointers | Two Pointers |
| Tree traversal | BFS (queue) or DFS (recursion) | BFS/DFS |
| Graph paths | BFS (shortest) or DFS | Graph |
| "All combinations" | Backtracking | Backtracking |
| "Minimum/Maximum" with choices | DP | Dynamic Programming |
| Nested brackets/matching | Stack | Stack |
| "Top K" or stream | Heap | Heap |
| Overlapping intervals | Sort + merge | Greedy |
| Prefix matching | Trie | Trie |
| Bit operations | XOR, AND, OR | Bit Manipulation |

---

## 🔹 LeetCode Practice Plan (100 Problems)

| Week | Problems | Focus |
|------|----------|-------|
| 1 | Easy #1-20 | Two Sum, Valid Parentheses, Merge Lists, Palindrome |
| 2 | Easy #21-40 | Binary Search, Max Depth, Climbing Stairs, Best Time to Buy Stock |
| 3 | Medium #1-20 | 3Sum, Container Water, Longest Substring, Group Anagrams |
| 4 | Medium #21-40 | Coin Change, LRU Cache, Course Schedule, Word Break |
| 5 | Medium #41-60 | Merge Intervals, Subsets, Permutations, Number of Islands |
| 6 | Hard #1-10 | Trapping Rain Water, N-Queens, Merge K Lists, Median Stream |
| 7-8 | Mock contests | Timed practice, 4 problems in 90 minutes |

---

*This completes the extended Interview Preparation series! Keep grinding, Sid! 🚀*
