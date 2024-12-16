from __future__ import annotations

import re
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from typing import NamedTuple


class CannotWinError(Exception):
    pass


class Position(NamedTuple):
    x: int
    y: int


@dataclass
class ClawMachine:
    a: Position
    b: Position
    prize: Position

    @classmethod
    def from_config(cls, config: str) -> ClawMachine:
        a_x, a_y, b_x, b_y, p_x, p_y = [int(x) for x in re.findall((r"(\d+)"), config)]
        return cls(Position(a_x, a_y), Position(b_x, b_y), Position(p_x, p_y))

    def correct_prize_position(self) -> None:
        self.prize = Position(
            self.prize.x + 10000000000000, self.prize.y + 10000000000000
        )

    def fewest_tokens_to_win(self) -> int:
        det = self.b.y * self.a.x - self.b.x * self.a.y
        inv = [
            [Fraction(self.b.y, det), Fraction(-self.b.x, det)],
            [Fraction(-self.a.y, det), Fraction(self.a.x, det)],
        ]
        a = inv[0][0] * self.prize.x + inv[0][1] * self.prize.y
        b = inv[1][0] * self.prize.x + inv[1][1] * self.prize.y
        tokens = 3 * a + b
        if tokens.denominator != 1:
            raise CannotWinError
        else:
            return tokens.numerator


def get_machines(path: Path) -> list[ClawMachine]:
    return [
        ClawMachine.from_config(config)
        for config in path.read_text().rstrip().split("\n\n")
    ]


def solve(machines: list[ClawMachine]) -> int:
    answer = 0
    for machine in machines:
        try:
            answer += machine.fewest_tokens_to_win()
        except CannotWinError:
            pass
    return answer


def main() -> None:
    machines = get_machines(Path("example.txt"))
    assert solve(machines) == 480

    machines = get_machines(Path("input.txt"))
    assert solve(machines) == 27157
    for machine in machines:
        machine.correct_prize_position()
    assert solve(machines) == 104015411578548
    print("All tests passed.")


if __name__ == "__main__":
    main()
