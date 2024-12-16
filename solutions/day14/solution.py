from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)


def read(path: Path) -> list[tuple[Vector, Vector]]:
    output: list[tuple[Vector, Vector]] = []
    for line in path.read_text().rstrip().splitlines():
        left, right = line.split()
        x, y = left.split("p=")[-1].split(",")
        position = Vector(int(x), int(y))
        x, y = right.split("v=")[-1].split(",")
        velocity = Vector(int(x), int(y))
        output.append((position, velocity))
    return output


def part1(path: Path, width: int, height: int) -> int:
    data = read(path)
    final_pos = [
        Vector((pos.x + 100 * vel.x) % width, (pos.y + 100 * vel.y) % height)
        for pos, vel in data
    ]
    mid_width, mid_height, a, b, c, d = width // 2, height // 2, 0, 0, 0, 0
    for pos in final_pos:
        if pos.x < mid_width and pos.y < mid_height:
            a += 1
        elif pos.x < mid_width and pos.y > mid_height:
            b += 1
        elif pos.x > mid_width and pos.y > mid_height:
            c += 1
        elif pos.x > mid_width and pos.y < mid_height:
            d += 1
    return a * b * c * d


def main() -> None:
    assert part1(Path("example.txt"), 11, 7) == 12
    assert part1(Path("input.txt"), 101, 103) == 221655456
    print("All tests passed.")


if __name__ == "__main__":
    main()
