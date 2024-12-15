import itertools
import pathlib
from enum import Enum, auto
from typing import NamedTuple

import tqdm


class Equation(NamedTuple):
    id: int
    numbers: tuple[int, ...]
    target: int


class Operation(Enum):
    ADD = auto()
    MULTIPLY = auto()
    CONCAT = auto()


def valid(equation: Equation, include_concat: bool = False) -> bool:
    _, numbers, target = equation
    n = len(numbers)
    operations = [Operation.ADD, Operation.MULTIPLY]
    if include_concat:
        operations.append(Operation.CONCAT)
    for ops in itertools.product(operations, repeat=n - 1):
        j = 0
        current = numbers[j]
        for op in ops:
            match op:
                case Operation.ADD:
                    current = current + numbers[j + 1]
                case Operation.MULTIPLY:
                    current = current * numbers[j + 1]
                case Operation.CONCAT:
                    current = int(f"{current}{numbers[j + 1]}")
            j += 1
        if current == target:
            return True
    return False


def read_equations(path: pathlib.Path) -> list[Equation]:
    equations: list[Equation] = []
    for i, line in enumerate(path.read_text().rstrip().splitlines()):
        target, numbers = line.split(": ")
        equations.append(
            Equation(
                id=i,
                numbers=tuple(int(num) for num in numbers.split()),
                target=int(target),
            )
        )
    return equations


def part1(equations: list[Equation]) -> set[Equation]:
    valid_ = set[Equation]()
    for equation in equations:
        if valid(equation):
            valid_.add(equation)
    return valid_


def part2(
    equations: list[Equation],
    already_valid: set[Equation],
    disable_progress: bool = False,
) -> set[Equation]:
    valid_ = set[Equation]()
    for equation in tqdm.tqdm(equations, disable=disable_progress):
        if equation in already_valid or valid(equation, include_concat=True):
            valid_.add(equation)
    return valid_


def sum_targets(equations: set[Equation]) -> int:
    return sum(equation.target for equation in equations)


def main() -> None:
    equations = read_equations(pathlib.Path("example.txt"))
    valid_from_part1 = part1(equations)
    assert sum_targets(valid_from_part1) == 3749
    assert (
        sum_targets(part2(equations, valid_from_part1, disable_progress=True)) == 11387
    )

    equations = read_equations(pathlib.Path("input.txt"))
    valid_from_part1 = part1(equations)
    assert sum_targets(valid_from_part1) == 66343330034722
    assert sum_targets(part2(equations, valid_from_part1)) == 637696070419031

    print("All tests passed.")


if __name__ == "__main__":
    main()
