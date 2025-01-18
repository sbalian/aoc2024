from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import StrEnum
from functools import cache
from pathlib import Path


class EntityType(StrEnum):
    WALL = "#"
    ROBOT = "@"
    BOX1 = "O"
    BOX2 = "[]"


@cache
def move_to_direction(move: str) -> Vector:
    match move:
        case ">":
            return Vector(0, 1)
        case "<":
            return Vector(0, -1)
        case "v":
            return Vector(1, 0)
        case "^":
            return Vector(-1, 0)
        case _:
            raise ValueError("unknown move")


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: int) -> Vector:
        return Vector(scalar * self.x, scalar * self.y)


@dataclass
class Entity:
    positions: tuple[Vector, ...]
    type: EntityType

    @property
    def is_box(self) -> bool:
        return self.type is EntityType.BOX1 or self.type is EntityType.BOX2


class Warehouse:
    def __init__(self, tiles: list[str], enlarge: bool = False):
        if enlarge:
            new_tiles: list[str] = []
            for row in tiles:
                new_row = ""
                for char in row:
                    match char:
                        case "@":
                            new_row += "@."
                        case "O":
                            new_row += "[]"
                        case "#":
                            new_row += "##"
                        case ".":
                            new_row += ".."
                        case _:
                            raise ValueError("unknown tile type")
                new_tiles.append(new_row)
            tiles = new_tiles

        self.positions: dict[Vector, Entity] = {}
        for x, row in enumerate(tiles):
            y = 0
            while y < len(row):
                tile = row[y]
                position = Vector(x, y)
                match tile:
                    case "#":
                        self.positions[position] = Entity(
                            positions=(position,), type=EntityType.WALL
                        )
                    case "O":
                        self.positions[position] = Entity(
                            positions=(position,), type=EntityType.BOX1
                        )
                    case "[":
                        second_position = position + Vector(0, 1)
                        entity = Entity(
                            positions=(position, second_position), type=EntityType.BOX2
                        )
                        self.positions[position] = entity
                        self.positions[second_position] = entity
                        y += 1
                    case "]":
                        raise ValueError("broken box found")
                    case "@":
                        self.positions[position] = Entity(
                            positions=(position,), type=EntityType.ROBOT
                        )
                        self.robot_position = position
                    case ".":
                        pass
                    case _:
                        raise ValueError("unknown tile")
                y += 1
        self.max_x, self.max_y = (
            max(self.positions, key=lambda p: p.x).x + 1,
            max(self.positions, key=lambda p: p.y).y + 1,
        )

    def show(self) -> None:
        for x in range(self.max_x):
            row = ""
            y = 0
            while y < self.max_y:
                position = Vector(x, y)
                entity = self.positions.get(position)
                if entity is None:
                    row += "."
                else:
                    row += entity.type.value
                    if entity.type is EntityType.BOX2:
                        y += 1
                y += 1
            print(row)

    def get_neighbors(self, direction: Vector, entity: Entity) -> list[Entity]:
        neighbors = list[Entity]()
        match direction:
            case Vector(0, 1):
                if (
                    neighbor := self.positions.get(entity.positions[-1] + direction)
                ) is not None:
                    neighbors.append(neighbor)
            case Vector(0, -1):
                if (
                    neighbor := self.positions.get(entity.positions[0] + direction)
                ) is not None:
                    neighbors.append(neighbor)
            case Vector(1, 0) | Vector(-1, 0):
                for position in entity.positions:
                    if (
                        neighbor := self.positions.get(position + direction)
                    ) is not None:
                        neighbors.append(neighbor)
            case _:
                raise RuntimeError("invalid direction")
        return neighbors

    def evolve(self, direction: Vector) -> None:
        robot = self.positions[self.robot_position]
        queue = deque[Entity]([robot])
        visited: list[Entity] = [robot]
        while queue:
            current = queue.popleft()
            for neighbor in self.get_neighbors(direction, current):
                if neighbor not in visited:
                    if neighbor.type is EntityType.WALL:
                        return
                    queue.append(neighbor)
                    visited.append(neighbor)
        new_entities: list[Entity] = []
        for entity in visited:
            new_entities.append(
                Entity(
                    positions=tuple(
                        position + direction for position in entity.positions
                    ),
                    type=entity.type,
                )
            )
            for position in entity.positions:
                del self.positions[position]
        for entity in new_entities:
            for position in entity.positions:
                self.positions[position] = entity
                if entity.type is EntityType.ROBOT:
                    self.robot_position = position

    def gps_sum_after_moves(self, moves: str) -> int:
        for move in moves:
            self.evolve(move_to_direction(move))
        gps_sum = 0
        seen = set[Vector]()
        for entity in self.positions.values():
            if entity.is_box and (position := entity.positions[0]) not in seen:
                gps_sum += 100 * position.x + position.y
                seen.add(position)
        return gps_sum


def read_input(path: Path) -> tuple[list[str], str]:
    tiles, moves = path.read_text().rstrip().split("\n\n")
    moves = moves.replace("\n", "")
    return tiles.splitlines(), moves


def main() -> None:
    tiles, moves = read_input(Path("example.txt"))
    assert Warehouse(tiles).gps_sum_after_moves(moves) == 10092
    warehouse = Warehouse(tiles, enlarge=True)
    # warehouse.show()
    assert warehouse.gps_sum_after_moves(moves) == 9021
    # warehouse.show()

    tiles, moves = read_input(Path("input.txt"))
    assert Warehouse(tiles).gps_sum_after_moves(moves) == 1490942
    assert Warehouse(tiles, enlarge=True).gps_sum_after_moves(moves) == 1519202
    print("All tests passed.")


if __name__ == "__main__":
    main()
