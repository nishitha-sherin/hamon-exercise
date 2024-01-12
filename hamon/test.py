import random
import math
import itertools

def split(items, ratios):
    total = sum(ratios)
    
    counts = [int(math.floor(len(items) * ratio / total)) for ratio in ratios]
    
    remaining = len(items) - sum(counts)
    
    while remaining > 0:
        index = random.randint(0, len(ratios) - 1)
        counts[index] += 1
        remaining -= 1
    
    subsets = []
    start = 0
    for count in counts:
        end = start + count
        subsets.append(items[start:end])
        start = end
    
    return subsets


def test_split():
    # Test case 1
    items = [1,2,3,4,5,6,7,8,9,10]
    ratios = [2, 3, 5]
    
    result1 = split(items, ratios)
    
    assert sum(len(subset) for subset in result1) == len(items)
    
    expected_counts = [2, 3, 5]
    for subset, count in zip(result1, expected_counts):
        assert len(subset) == count
    
    # Test case 2
    items = [11,12,13]
    ratios = [1, 1, 1]
    
    result2 = split(items, ratios)
    
    assert sum(len(subset) for subset in result2) == len(items)
    
    flattened_result = list(itertools.chain(*result2))
    assert set(flattened_result) == set(items)
    
    for subset in result2:
        assert len(subset) == 1
    
    return result1, result2


# Run the unit tests and get the results
result1, result2 = test_split()
print("Test case 1 result:", result1)
print("Test case 2 result:", result2)