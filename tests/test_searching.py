"""Run from project root: python -m unittest discover -s tests -v"""
import unittest

from algorithms.searching import binary_search, hash_table_lookup, linear_search


class TestSearching(unittest.TestCase):
    def test_linear_search(self):
        cases = [([], 2, -1), ([7], 7, 0), ([7], 8, -1),
                 ([3, 1, 3, 2], 3, 0), ([1, 2, 3], 4, -1),
                 ([5, 4, 3, 2, 1], 2, 3)]
        for values, target, expected in cases:
            with self.subTest(values=values, target=target):
                self.assertEqual(linear_search(values, target), expected)

    def test_binary_search(self):
        cases = [([], 4), ([5], 5), ([5], 4),
                 ([1, 2, 3, 4, 5], 3), ([1, 2, 3, 4], 9),
                 ([-4, -1, 0, 0, 0, 8], 0)]
        for values, target in cases:
            with self.subTest(values=values, target=target):
                index = binary_search(values, target)
                if target in values:
                    self.assertGreaterEqual(index, 0)
                    self.assertEqual(values[index], target)
                else:
                    self.assertEqual(index, -1)

    def test_hash_table_lookup(self):
        table = {"a": 5, "b": 0, "c": None, 9: "nine"}
        self.assertEqual(hash_table_lookup(table, "a"), 5)
        self.assertEqual(hash_table_lookup(table, "b"), 0)
        self.assertIsNone(hash_table_lookup(table, "c"))
        self.assertIsNone(hash_table_lookup(table, "missing"))
        self.assertEqual(hash_table_lookup(table, "missing", -1), -1)
        self.assertEqual(hash_table_lookup(table, 9), "nine")
        self.assertEqual(hash_table_lookup({}, "missing", "not found"), "not found")
        self.assertEqual(table, {"a": 5, "b": 0, "c": None, 9: "nine"})


if __name__ == "__main__":
    unittest.main()
