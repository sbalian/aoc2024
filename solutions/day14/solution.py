from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)


@dataclass
class Robot:
    position: Vector
    velocity: Vector


class World:
    def __init__(self, path: Path, width: int, height: int) -> None:
        self.width, self.height = width, height
        self.robots: list[Robot] = []
        for line in path.read_text().rstrip().splitlines():
            left, right = line.split()
            x, y = left.split("p=")[-1].split(",")
            position = Vector(int(x), int(y))
            vx, vy = right.split("v=")[-1].split(",")
            velocity = Vector(int(vx), int(vy))
            self.robots.append(Robot(position=position, velocity=velocity))
        self.positions = defaultdict[Vector, int](int)
        for robot in self.robots:
            self.positions[robot.position] += 1

    def evolve(self, steps: int = 1) -> None:
        for robot in self.robots:
            self.positions[robot.position] -= 1
            robot.position = Vector(
                x=(robot.position.x + steps * robot.velocity.x) % self.width,
                y=(robot.position.y + steps * robot.velocity.y) % self.height,
            )
            self.positions[robot.position] += 1

    def quadrant_counts(self) -> tuple[int, int, int, int]:
        mid_width, mid_height, a, b, c, d = (
            self.width // 2,
            self.height // 2,
            0,
            0,
            0,
            0,
        )
        for robot in self.robots:
            position = robot.position
            if position.x < mid_width and position.y < mid_height:
                a += 1
            elif position.x < mid_width and position.y > mid_height:
                c += 1
            elif position.x > mid_width and position.y > mid_height:
                d += 1
            elif position.x > mid_width and position.y < mid_height:
                b += 1
        return a, b, c, d

    def safety_factor(self) -> int:
        a, b, c, d = self.quadrant_counts()
        return a * b * c * d

    def show(self) -> None:
        for y in range(self.height):
            row = ""
            for x in range(self.width):
                tiles = self.positions[Vector(x, y)]
                if tiles == 0:
                    row += " "
                else:
                    row += str(tiles)
            print(row)


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
    world = World(path, width, height)
    world.evolve(100)
    return world.safety_factor()


def part2(path: Path, width: int, height: int) -> None:
    world = World(path, width, height)
    t = 81
    dt = 101
    world.evolve(t)
    while True:
        print(f"{t=}")
        world.show()
        input()
        world.evolve(dt)
        t += dt


def main() -> None:
    assert part1(Path("example.txt"), 11, 7) == 12
    assert part1(Path("input.txt"), 101, 103) == 221655456
    print("All tests passed.")
    # part2(Path("input.txt"), 101, 103)  #  ... you will see it at t=7858


if __name__ == "__main__":
    main()
