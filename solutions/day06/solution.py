import concurrent.futures
import copy
import pathlib
from functools import partial

import tqdm

type Grid = list[list[str]]
type Point = tuple[int, int]


class LoopFoundError(Exception):
    pass


def read_grid(path: pathlib.Path) -> Grid:
    return [list(row) for row in path.read_text().rstrip().splitlines()]


def add(a: Point, b: Point) -> Point:
    return (a[0] + b[0], a[1] + b[1])


def start(grid: Grid) -> Point:
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "^":
                return (i, j)
    raise RuntimeError("no starting position")


def new_grid(grid: Grid, obstruction: Point) -> Grid:
    grid = copy.deepcopy(grid)
    grid[obstruction[0]][obstruction[1]] = "O"
    return grid


def walk(grid: Grid, start: Point) -> set[Point]:
    position = start
    momentum: Point = (-1, 0)
    visited: set[Point] = set([position])
    visited_with_momentum: set[tuple[Point, Point]] = set([(position, momentum)])

    while True:
        next_position = add(position, momentum)
        if not (
            (0 <= next_position[0] < len(grid))
            and (0 <= next_position[1] < len(grid[0]))
        ):
            return visited
        elif grid[next_position[0]][next_position[1]] in (".", "^"):
            position = next_position
            visited.add(position)
            if (position, momentum) in visited_with_momentum:
                raise LoopFoundError
            visited_with_momentum.add((position, momentum))
        else:
            match momentum:
                case (-1, 0):
                    momentum = (0, 1)
                case (0, 1):
                    momentum = (1, 0)
                case (1, 0):
                    momentum = (0, -1)
                case _:
                    momentum = (-1, 0)


def part1(path: pathlib.Path) -> int:
    grid = read_grid(path)
    return len(walk(grid, start(grid)))


def worker(start: Point, grid: Grid, obstruction: Point) -> int:
    try:
        walk(new_grid(grid, obstruction), start)
        return 0
    except LoopFoundError:
        return 1


def part2(path: pathlib.Path, disable_progress: bool = False) -> int:
    # NOTE this can be solved more efficiently by jumping between obstructions, but
    # this brute-force method takes only ~ 15 seconds on my 20 core machine.

    grid = read_grid(path)
    start_ = start(grid)
    obstructions: list[Point] = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] in (".", "^"):
                obstructions.append((i, j))
    worker_ = partial(worker, start_, grid)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        return sum(
            tqdm.tqdm(
                executor.map(worker_, obstructions),
                total=len(obstructions),
                disable=disable_progress,
            )
        )


def main() -> None:
    assert part1(pathlib.Path("example.txt")) == 41
    assert part1(pathlib.Path("input.txt")) == 5086
    assert part2(pathlib.Path("example.txt"), disable_progress=True) == 6
    assert part2(pathlib.Path("input.txt")) == 1770
    print("All tests passed.")


if __name__ == "__main__":
    main()
