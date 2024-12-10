import pathlib
from collections import defaultdict
from typing import Callable

type Point = tuple[int, int]


def read_grid(path: pathlib.Path) -> list[list[str]]:
    return [list(line) for line in path.read_text().rstrip().splitlines()]


def is_inside_grid(a: Point, rows: int, cols: int) -> bool:
    return (0 <= a[0] < rows) and (0 <= a[1] < cols)


def part1(
    positions: list[Point],
    rows: int,
    cols: int,
    antinodes: set[Point],
) -> None:
    for i in range(len(positions)):
        a = positions[i]
        j = 0
        while j < i:
            b = positions[j]
            grad = (b[0] - a[0], b[1] - a[1])
            from_a = (a[0] - grad[0], a[1] - grad[1])
            from_b = (b[0] + grad[0], b[1] + grad[1])
            if is_inside_grid(from_a, rows, cols):
                antinodes.add(from_a)
            if is_inside_grid(from_b, rows, cols):
                antinodes.add(from_b)
            j += 1


def part2(
    positions: list[Point],
    rows: int,
    cols: int,
    antinodes: set[Point],
) -> None:
    for i in range(len(positions)):
        a = positions[i]
        antinodes.add(a)
        j = 0
        while j < i:
            b = positions[j]
            antinodes.add(b)
            grad = (b[0] - a[0], b[1] - a[1])

            from_a = (a[0] - grad[0], a[1] - grad[1])
            from_b = (b[0] + grad[0], b[1] + grad[1])

            k = 1
            while True:
                if is_inside_grid(from_a, rows, cols):
                    antinodes.add(from_a)
                    k += 1
                    from_a = (a[0] - k * grad[0], a[1] - k * grad[1])
                else:
                    break

            k = 1
            while True:
                if is_inside_grid(from_b, rows, cols):
                    antinodes.add(from_b)
                    k += 1
                    from_b = (b[0] + k * grad[0], b[1] + k * grad[1])
                else:
                    break
            j += 1


def find_antenna_positions(grid: list[list[str]]) -> dict[str, list[Point]]:
    positions: dict[str, list[Point]] = defaultdict(list[Point])
    rows = len(grid)
    cols = len(grid[0])
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != ".":
                positions[grid[i][j]].append((i, j))
    return positions


def solve(
    antenna_positions: dict[str, list[Point]],
    rows: int,
    cols: int,
    solver: Callable[[list[Point], int, int, set[Point]], None],
) -> int:
    antinodes: set[Point] = set()
    for positions in antenna_positions.values():
        solver(positions, rows, cols, antinodes)
    return len(antinodes)


def main() -> None:
    grid = read_grid(pathlib.Path("example.txt"))
    antenna_positions = find_antenna_positions(grid)
    assert solve(antenna_positions, len(grid), len(grid[0]), part1) == 14
    assert solve(antenna_positions, len(grid), len(grid[0]), part2) == 34

    grid = read_grid(pathlib.Path("input.txt"))
    antenna_positions = find_antenna_positions(grid)
    assert solve(antenna_positions, len(grid), len(grid[0]), part1) == 276
    assert solve(antenna_positions, len(grid), len(grid[0]), part2) == 991
    print("All tests passed.")


if __name__ == "__main__":
    main()
