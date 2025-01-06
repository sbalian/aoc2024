from __future__ import annotations

from collections import defaultdict, deque
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

    @staticmethod
    def num_states(start: State, previous: defaultdict[State, list[State]]) -> int:
        visited = set[State]([start])
        queue = deque[State]([start])
        while queue:
            node = queue.popleft()
            for neighbor in previous[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return len(set(node.position for node in visited))

    def solve(self) -> tuple[int, int]:
        start, end = self.find_start_end()
        start = State(position=start, velocity=Vector(0, 1))
        queue: list[MazePath] = []
        heappush(queue, MazePath(head=start, cost=0))
        costs: dict[State, int] = {}
        previous = defaultdict[State, list[State]](list)
        while queue:
            path = heappop(queue)
            node = path.head
            for neighbor in self.get_neighbors(node):
                if node.velocity != neighbor.velocity:
                    cost = path.cost + 1001
                else:
                    cost = path.cost + 1
                if cost <= costs.get(neighbor, INF):
                    heappush(queue, MazePath(neighbor, cost))
                    costs[neighbor] = cost
                    previous[neighbor].append(node)
        best_final_state, best_cost = min(
            [(node, cost) for node, cost in costs.items() if node.position == end],
            key=lambda item: item[1],
        )
        return best_cost, self.num_states(best_final_state, previous)

    def find_start_end(self) -> tuple[Vector, Vector]:
        start, end = None, None
        for i in range(self.rows):
            for j in range(self.cols):
                if self[Vector(i, j)] == "S":
                    start = Vector(i, j)
                elif self[Vector(i, j)] == "E":
                    end = Vector(i, j)
                if start is not None and end is not None:
                    return start, end
        raise ValueError("start not found")


def main() -> None:
    maze = Maze.from_file(Path("example1.txt"))
    assert maze.solve() == (7036, 45)
    maze = Maze.from_file(Path("example2.txt"))
    assert maze.solve() == (11048, 64)
    maze = Maze.from_file(Path("example3.txt"))
    assert maze.solve() == (1006, 7)
    maze = Maze.from_file(Path("example4.txt"))
    assert maze.solve() == (1025, 26)
    maze = Maze.from_file(Path("input.txt"))
    assert maze.solve() == (98416, 471)
    print("All tests passed.")


if __name__ == "__main__":
    main()
