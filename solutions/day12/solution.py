from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from functools import cache
from pathlib import Path

from rich import print


@dataclass(frozen=True)
class Point:
    x: int
    y: int

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)


DIRECTIONS = set([Point(0, 1), Point(1, 0), Point(0, -1), Point(-1, 0)])


@dataclass
class Region:
    plant: str
    area: int
    perimeter: int
    corners: int

    def price_part1(self) -> int:
        return self.area * self.perimeter

    def price_part2(self) -> int:
        return self.area * self.corners


class Garden:
    def __init__(self, plots: list[list[str]]):
        self.plots = plots
        self.all_visited = set[Point]()
        self.regions = list[Region]()
        self.find_regions()

    def __getitem__(self, position: Point) -> str:
        return self.plots[position.x][position.y]

    @property
    def rows(self):
        return len(self.plots)

    @property
    def cols(self):
        return len(self.plots[0])

    def within_bounds(self, position: Point) -> bool:
        return (0 <= position.x < self.rows) and (0 <= position.y < self.cols)

    @classmethod
    def from_file(cls, path: Path) -> Garden:
        return Garden([list(line) for line in path.read_text().splitlines()])

    @cache
    def _get_neighbors_and_walls(
        self, position: Point
    ) -> tuple[list[Point], set[Point]]:
        neighbors: list[Point] = []
        directions = set[Point]()
        for direction in DIRECTIONS:
            neighbor = position + direction
            if self.within_bounds(neighbor) and self[neighbor] == self[position]:
                neighbors.append(neighbor)
                directions.add(direction)
        return neighbors, (DIRECTIONS - directions)

    def get_neighbors(self, position: Point) -> list[Point]:
        neighbors, _ = self._get_neighbors_and_walls(position)
        return neighbors

    def get_walls(self, position: Point) -> set[Point]:
        _, walls = self._get_neighbors_and_walls(position)
        return walls

    @staticmethod
    def inner_corners(walls: set[Point]) -> int:
        if len(walls) == 4:
            return 4
        if len(walls) == 3:
            return 2
        if len(walls) == 2:
            if (
                walls == set([Point(0, 1), Point(1, 0)])
                or walls == set([Point(0, 1), Point(-1, 0)])
                or walls == set([Point(0, -1), Point(1, 0)])
                or walls == set([Point(0, -1), Point(-1, 0)])
            ):
                return 1
        return 0

    @staticmethod
    def outer_corner(
        position: Point,
        direction1: Point,
        direction2: Point,
        in_region: set[Point],
    ) -> bool:
        return (
            (position + direction1) in in_region
            and (position + direction2) in in_region
            and (position + direction1 + direction2) not in in_region
        )

    def outer_corners(self, position: Point, in_region: set[Point]) -> int:
        corners = 0
        corners += int(
            self.outer_corner(position, Point(-1, 0), Point(0, 1), in_region)
        )
        corners += int(
            self.outer_corner(position, Point(-1, 0), Point(0, -1), in_region)
        )
        corners += int(self.outer_corner(position, Point(1, 0), Point(0, 1), in_region))
        corners += int(
            self.outer_corner(position, Point(1, 0), Point(0, -1), in_region)
        )
        return corners

    def find_regions(self) -> None:
        for i in range(self.rows):
            for j in range(self.cols):
                self.find_region(Point(i, j))

    def find_region(self, source: Point) -> None:
        in_region = set[Point]()
        if source in self.all_visited:
            return
        self.all_visited.add(source)
        in_region.add(source)
        perimeter, area = 4 - len(self.get_neighbors(source)), 1
        corners = self.inner_corners(self.get_walls(source))
        queue = deque[Point]([source])
        while queue:
            current = queue.popleft()
            for neighbor in self.get_neighbors(current):
                if neighbor not in self.all_visited:
                    queue.append(neighbor)
                    self.all_visited.add(neighbor)
                    in_region.add(neighbor)
                    perimeter += 4 - len(self.get_neighbors(neighbor))
                    area += 1
                    corners += self.inner_corners(self.get_walls(neighbor))
        for position in in_region:
            corners += self.outer_corners(position, in_region)
        self.regions.append(
            Region(
                plant=self[source],
                area=area,
                perimeter=perimeter,
                corners=corners,
            )
        )
        return

    def part1(self) -> int:
        return sum(region.price_part1() for region in self.regions)

    def part2(self) -> int:
        return sum(region.price_part2() for region in self.regions)


def main() -> None:
    garden = Garden.from_file(Path("example1.txt"))
    assert garden.part1() == 1930
    assert garden.part2() == 1206

    garden = Garden.from_file(Path("example2.txt"))
    assert garden.part1() == 140
    assert garden.part2() == 80

    garden = Garden.from_file(Path("example3.txt"))
    assert garden.part1() == 772
    assert garden.part2() == 436

    garden = Garden.from_file(Path("example4.txt"))
    assert garden.part2() == 236

    garden = Garden.from_file(Path("example5.txt"))
    assert garden.part2() == 368

    garden = Garden.from_file(Path("input.txt"))
    assert garden.part1() == 1477762
    assert garden.part2() == 923480

    print("All tests passed.")


if __name__ == "__main__":
    main()
