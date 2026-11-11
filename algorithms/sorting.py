"""Sorting algorithms for Member 1 (CS25BT005).

Common interface: each function accepts a sequence of comparable values and
returns a NEW list sorted in ascending order. Inputs are not modified.
"""


def quick_sort(values):
    """Three-way quicksort. Average O(n log n), worst O(n^2) time; O(n) auxiliary space."""
    items = list(values)

    def sort(part):
        if len(part) <= 1:
            return part
        pivot = part[len(part) // 2]
        lower = [x for x in part if x < pivot]
        equal = [x for x in part if x == pivot]
        higher = [x for x in part if x > pivot]
        return sort(lower) + equal + sort(higher)

    return sort(items)


def merge_sort(values):
    """Stable merge sort. O(n log n) time and O(n) auxiliary space."""
    items = list(values)
    if len(items) <= 1:
        return items

    mid = len(items) // 2
    left = merge_sort(items[:mid])
    right = merge_sort(items[mid:])
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def heap_sort(values):
    """Heap sort. O(n log n) time; O(n) space for the input copy."""
    items = list(values)
    n = len(items)

    def sift_down(root, end):
        while 2 * root + 1 < end:
            child = 2 * root + 1
            if child + 1 < end and items[child] < items[child + 1]:
                child += 1
            if items[root] >= items[child]:
                break
            items[root], items[child] = items[child], items[root]
            root = child

    for root in range(n // 2 - 1, -1, -1):
        sift_down(root, n)
    for end in range(n - 1, 0, -1):
        items[0], items[end] = items[end], items[0]
        sift_down(0, end)
    return items


def insertion_sort(values):
    """Stable insertion sort. Best O(n), average/worst O(n^2) time; O(n) copy space."""
    items = list(values)
    for i in range(1, len(items)):
        key = items[i]
        j = i - 1
        while j >= 0 and items[j] > key:
            items[j + 1] = items[j]
            j -= 1
        items[j + 1] = key
    return items
