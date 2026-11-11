"""Searching algorithms for Member 1 (CS25BT005).

linear_search and binary_search return a matching index or -1 if not found.
hash_table_lookup returns a dictionary value or a supplied default (None by default).
"""


def linear_search(values, target):
    """Find the first matching index. O(n) time, O(1) extra space."""
    for index, value in enumerate(values):
        if value == target:
            return index
    return -1


def binary_search(values, target):
    """Find a matching index in ASCENDING-SORTED values; O(log n) time, O(1) space.

    The input MUST already be sorted in nondecreasing order.
    If duplicates exist, any matching index may be returned.
    """
    left, right = 0, len(values) - 1
    while left <= right:
        mid = (left + right) // 2
        if values[mid] == target:
            return mid
        if values[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1


def hash_table_lookup(table, key, default=None):
    """Look up a key in a dict. Average O(1), worst O(n) time; O(1) extra space.

    Uses Python's built-in hash table; keys must be hashable. A custom default
    distinguishes an absent key from a present key whose value is None.
    """
    return table.get(key, default)
