import re
from pathlib import Path
from typing import Literal

type Point = tuple[int, int]
type Warehouse = list[list[str]]
type Move = Literal[">", "<", "^", "v"]


def read_input(path: Path) -> tuple[Warehouse, list[Move]]:
    warehouse, moves = path.read_text().split("\n\n")
    moves = moves.replace("\n", "")
    return [list(line) for line in warehouse.splitlines()], list(moves)  # pyright: ignore[reportReturnType]


def find_robot(warehouse: Warehouse) -> Point:
    for i in range(len(warehouse)):
        for j in range(len(warehouse[0])):
            if warehouse[i][j] == "@":
                return (i, j)
    raise RuntimeError("could not find the robot")


def traverse(view: list[str]) -> list[str]:
    if view[0] == ".":
        return ["@"] + view[1:]
    elif match := re.match(r"^(O+)(\.)", view_ := "".join(view)):
        _, end = match.span()
        return list("@" + view_[1 : end - 1] + "O" + view_[end:])
    else:
        return view


def get_view_points(move: Move, position: Point, warehouse: Warehouse) -> list[Point]:
    num_rows = len(warehouse)
    num_cols = len(warehouse[0])
    match move:
        case ">":
            return [(position[0], i) for i in range(position[1] + 1, num_cols)]
        case "<":
            return [(position[0], i) for i in range(position[1] - 1, -1, -1)]
        case "v":
            return [(i, position[1]) for i in range(position[0] + 1, num_rows)]
        case "^":
            return [(i, position[1]) for i in range(position[0] - 1, -1, -1)]


def show_warehouse(warehouse: Warehouse) -> None:
    for i in range(len(warehouse)):
        print("".join(warehouse[i]))
    print()


def part1(warehouse: Warehouse, moves: list[Move]) -> int:
    robot_position = find_robot(warehouse)
    for move in moves:
        view_points = get_view_points(move, robot_position, warehouse)
        view = [warehouse[p[0]][p[1]] for p in view_points]
        new_view = traverse(view)
        if new_view[0] == "@":
            warehouse[robot_position[0]][robot_position[1]] = "."
            robot_position = view_points[0]
        for i, point in enumerate(view_points):
            warehouse[point[0]][point[1]] = new_view[i]

    score = 0
    for i in range(len(warehouse)):
        for j in range(len(warehouse[i])):
            if warehouse[i][j] == "O":
                score += 100 * i + j
    return score


def main() -> None:
    warehouse, moves = read_input(Path("input.txt"))
    assert part1(warehouse, moves) == 1490942
    print("All tests passed.")


if __name__ == "__main__":
    main()
