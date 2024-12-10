from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)


class Map:
    def __init__(self, heights: list[list[int]]):
        self.heights = heights

    def __getitem__(self, position: Point) -> int:
        return self.heights[position.x][position.y]

    @property
    def rows(self):
        return len(self.heights)

    @property
    def cols(self):
        return len(self.heights[0])

    def within_bounds(self, position: Point) -> bool:
        return (0 <= position.x < self.rows) and (0 <= position.y < self.cols)

    @classmethod
    def from_file(cls, path: Path) -> Map:
        return Map(
            [
                list(int(height) for height in line)
                for line in path.read_text().splitlines()
            ]
        )

    def get_neighbors(self, position: Point) -> list[Point]:
        return [
            neighbor
            for direction in (Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0))
            if self.within_bounds(neighbor := (position + direction))
        ]

    def find_zeros(self) -> list[Point]:
        zeros: list[Point] = []
        for i in range(self.rows):
            for j in range(self.cols):
                if self[point := Point(i, j)] == 0:
                    zeros.append(point)
        return zeros

    def bfs(self, source: Point, rating) -> int:
        score = 0
        visited = set([source])
        queue = deque([source])
        while queue:
            current = queue.popleft()
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited and (self[neighbor] - self[current]) == 1:
                    queue.append(neighbor)
                    if not rating:
                        visited.add(neighbor)
                    if self[neighbor] == 9:
                        score += 1
        return score

    def __str__(self) -> str:
        content = ""
        for row in self.heights:
            content += "".join(str(height) for height in row)
            content += "\n"
        return content.rstrip()

    def _solve(self, rating: bool) -> int:
        return sum(self.bfs(zero, rating=rating) for zero in self.find_zeros())

    def part1(self) -> int:
        return self._solve(rating=False)

    def part2(self) -> int:
        return self._solve(rating=True)


def main() -> None:
    map = Map.from_file(Path("example.txt"))
    assert map.part1() == 36
    assert map.part2() == 81

    map = Map.from_file(Path("input.txt"))
    assert map.part1() == 825
    assert map.part2() == 1805

    print("All tests passed.")


if __name__ == "__main__":
    main()
