from collections import defaultdict


def read(arrangement: str) -> list[int]:
    return [int(stone) for stone in arrangement.split()]


def blink(stone_counts: dict[int, int]) -> dict[int, int]:
    next_counts: dict[int, int] = defaultdict(int)
    for stone, count in stone_counts.items():
        if count > 0:
            next_counts[stone] = count
    for stone in list(next_counts.keys()):
        count = stone_counts[stone]
        if stone == 0:
            next_counts[1] += count
            next_counts[0] -= count
        elif len(brittle_stone := str(stone)) % 2 == 0:
            mid = len(brittle_stone) // 2
            left_stone, right_stone = brittle_stone[:mid], brittle_stone[mid:]
            left_stone = int(left_stone)
            right_stone = int(right_stone)
            next_counts[stone] -= count
            next_counts[left_stone] += count
            next_counts[right_stone] += count
        else:
            next_counts[stone] -= count
            next_counts[2024 * stone] += count
    return next_counts


def blink_many_times(stones: list[int], n: int) -> int:
    stone_counts: dict[int, int] = defaultdict(int)
    for stone in stones:
        stone_counts[stone] += 1
    for _ in range(n):
        stone_counts = blink(stone_counts)
    return sum(stone_counts.values())


def main() -> None:
    stones = read("125 17")
    assert blink_many_times(stones, 25) == 55312
    assert blink_many_times(stones, 75) == 65601038650482
    stones = read("2 54 992917 5270417 2514 28561 0 990")
    assert blink_many_times(stones, 25) == 222461
    assert blink_many_times(stones, 75) == 264350935776416
    print("All tests passed.")


if __name__ == "__main__":
    main()
