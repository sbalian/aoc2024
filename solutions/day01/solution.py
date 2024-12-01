import collections
import pathlib


def read_lists(path: pathlib.Path) -> tuple[list[int], list[int]]:
    left: list[int] = []
    right: list[int] = []
    for line in path.read_text().rstrip().splitlines():
        a, b = line.split()
        left.append(int(a))
        right.append(int(b))
    return left, right


def part1(left: list[int], right: list[int]) -> int:
    left.sort()
    right.sort()
    return sum(abs(a - b) for a, b in zip(left, right))


def part2(left, right) -> int:
    counter = collections.Counter(right)
    return sum(a * counter.get(a, 0) for a in left)


def main() -> None:
    left, right = read_lists(pathlib.Path("input.txt"))
    assert part1(left, right) == 1197984
    assert part2(left, right) == 23387399
    print("All tests passed.")


if __name__ == "__main__":
    main()
