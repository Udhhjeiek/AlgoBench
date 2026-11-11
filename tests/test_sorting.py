"""Run from project root: python -m unittest discover -s tests -v"""
import random
import unittest

from algorithms.sorting import heap_sort, insertion_sort, merge_sort, quick_sort


SORTERS = (quick_sort, merge_sort, heap_sort, insertion_sort)


class TestSorting(unittest.TestCase):
    def test_required_edge_cases(self):
        cases = [
            [], [8], [4, 4, 4, 4], [1, 2, 3, 4, 5],
            [5, 4, 3, 2, 1], [3, 1, 3, 2, 1],
            [0, -10, 5, -2, 0], [2.5, -1.5, 2.5, 0.0],
        ]
        for sorter in SORTERS:
            for case in cases:
                with self.subTest(algorithm=sorter.__name__, values=case):
                    original = case.copy()
                    result = sorter(case)
                    self.assertEqual(result, sorted(case))
                    self.assertEqual(case, original, "Input must not be mutated")
                    self.assertIsInstance(result, list)

    def test_repeatable_random_cases(self):
        rng = random.Random(6134)
        for sorter in SORTERS:
            for length in (0, 1, 2, 10, 50):
                case = [rng.randint(-20, 20) for _ in range(length)]
                with self.subTest(algorithm=sorter.__name__, length=length):
                    self.assertEqual(sorter(case), sorted(case))


if __name__ == "__main__":
    unittest.main()
