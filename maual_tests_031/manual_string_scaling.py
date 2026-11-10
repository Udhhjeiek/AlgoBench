
from data_generation_031.string_generator import (
    generate_random_string,
    generate_string_pair,
    generate_identical_string_pair,
    generate_no_common_string_pair,
)

# Dataset sizes for scaling verification
sizes = [100, 1000, 5000, 10000]

print("STRING GENERATOR SCALING TEST")
print("=" * 45)

for size in sizes:
    # 1. Generate a random string
    s = generate_random_string(size, seed=42)
    assert len(s) == size

    # 2. Check reproducibility
    s_again = generate_random_string(size, seed=42)
    assert s == s_again

    # 3. Generate a pair of random strings
    a, b = generate_string_pair(size, seed=42)
    assert len(a) == size
    assert len(b) == size

    # 4. Generate identical strings
    x, y = generate_identical_string_pair(size, seed=42)
    assert x == y
    assert len(x) == size

    # 5. Generate strings with no common characters
    p, q = generate_no_common_string_pair(size, seed=42)
    assert len(p) == size
    assert len(q) == size
    assert set(p).isdisjoint(set(q))

    print(f"Size: {size:>5} | All checks PASSED")

print("=" * 45)
print("ALL STRING SCALING CHECKS PASSED!")
