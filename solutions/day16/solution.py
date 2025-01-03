from __future__ import annotations

from dataclasses import dataclass, field
from heapq import heappop, heappush
from pathlib import Path

INF = 100000000


@dataclass(frozen=True)
class Vector:
    i: int
    j: int

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.i + other.i, self.j + other.j)


@dataclass(frozen=True)
class State:
    position: Vector
    velocity: Vector


@dataclass(order=True)
class MazePath:
    head: State = field(compare=False)
    cost: int = INF


class Maze:
    def __init__(self, tiles: list[str]):
        self.tiles = tiles

    def __getitem__(self, position: Vector) -> str:
        return self.tiles[position.i][position.j]

    @property
    def rows(self):
        return len(self.tiles)

    @property
    def cols(self):
        return len(self.tiles[0])

    @classmethod
    def from_file(cls, path: Path) -> Maze:
        return cls([line for line in path.read_text().rstrip().splitlines()])

    def get_neighbors(self, state: State) -> list[State]:
        match state:
            case State(position=position, velocity=Vector(-1, 0)):
                states = [
                    State(position=position + Vector(-1, 0), velocity=Vector(-1, 0)),
                    State(position=position + Vector(0, 1), velocity=Vector(0, 1)),
                    State(position=position + Vector(0, -1), velocity=Vector(0, -1)),
                ]
            case State(position=position, velocity=Vector(1, 0)):
                states = [
                    State(position=position + Vector(1, 0), velocity=Vector(1, 0)),
                    State(position=position + Vector(0, 1), velocity=Vector(0, 1)),
                    State(position=position + Vector(0, -1), velocity=Vector(0, -1)),
                ]
            case State(position=position, velocity=Vector(0, 1)):
                states = [
                    State(position=position + Vector(0, 1), velocity=Vector(0, 1)),
                    State(position=position + Vector(1, 0), velocity=Vector(1, 0)),
                    State(position=position + Vector(-1, 0), velocity=Vector(-1, 0)),
                ]
            case State(position=position, velocity=Vector(0, -1)):
                states = [
                    State(position=position + Vector(0, -1), velocity=Vector(0, -1)),
                    State(position=position + Vector(1, 0), velocity=Vector(1, 0)),
                    State(position=position + Vector(-1, 0), velocity=Vector(-1, 0)),
                ]
            case _:
                raise RuntimeError("unhandled state")
        return [state for state in states if self[state.position] != "#"]

    def find_min_cost(self, start: State) -> int:
        queue: list[MazePath] = []
        heappush(queue, MazePath(head=start, cost=0))
        costs: dict[State, int] = {start: 0}
        while queue:
            path = heappop(queue)
            node = path.head
            if self[node.position] == "E":
                return path.cost
            else:
                for neighbor in self.get_neighbors(node):
                    if node.velocity != neighbor.velocity:
                        cost = path.cost + 1001
                    else:
                        cost = path.cost + 1
                    if cost < costs.get(neighbor, INF):
                        heappush(queue, MazePath(neighbor, cost))
                        costs[neighbor] = cost
        raise RuntimeError("end not reached")

    def find_start(self) -> Vector:
        for i in range(self.rows):
            for j in range(self.cols):
                if self[Vector(i, j)] == "S":
                    return Vector(i, j)
        raise ValueError("start not found")

    def part1(self):
        start = self.find_start()
        return self.find_min_cost(State(position=start, velocity=Vector(0, 1)))


def main() -> None:
    maze = Maze.from_file(Path("example1.txt"))
    assert maze.part1() == 7036
    maze = Maze.from_file(Path("example2.txt"))
    assert maze.part1() == 11048
    maze = Maze.from_file(Path("example3.txt"))
    assert maze.part1() == 1006
    maze = Maze.from_file(Path("example4.txt"))
    assert maze.part1() == 1025
    maze = Maze.from_file(Path("input.txt"))
    assert maze.part1() == 98416
    print("All tests passed.")


if __name__ == "__main__":
    main()
