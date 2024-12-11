from __future__ import annotations

import pathlib
from collections import defaultdict


class PageNumber:
    rules: dict[str, list[str]]

    def __init__(self, value: str) -> None:
        self.value = value

    def __lt__(self, other: PageNumber) -> bool:
        return other.value in self.rules[self.value]


class Update:
    def __init__(self, page_numbers: list[PageNumber]):
        self.page_numbers = page_numbers

    def is_ordered(self) -> bool:
        return all(x < y for x, y in zip(self.page_numbers, self.page_numbers[1:]))

    def sorted(self) -> Update:
        return Update(sorted(self.page_numbers))

    def midpoint(self) -> int:
        return int(self.page_numbers[len(self.page_numbers) // 2].value)


def read_updates_and_set_rules(path: pathlib.Path) -> list[Update]:
    rules: list[tuple[str, str]] = []
    updates: list[Update] = []
    populate_rules = True
    for line in path.read_text().rstrip().splitlines():
        if line == "":
            populate_rules = False
        elif populate_rules:
            x, y = line.split("|")
            rules.append((x, y))
        else:
            updates.append(Update([PageNumber(value) for value in line.split(",")]))
    rules_dict = defaultdict[str, list[str]](list)
    for x, y in rules:
        rules_dict[x].append(y)
    PageNumber.rules = rules_dict
    return updates


def part1(updates: list[Update]) -> int:
    return sum(update.midpoint() for update in updates if update.is_ordered())


def part2(updates: list[Update]) -> int:
    return sum(
        update.sorted().midpoint() for update in updates if not update.is_ordered()
    )


def main() -> None:
    updates = read_updates_and_set_rules(pathlib.Path("example.txt"))
    assert part1(updates) == 143
    assert part2(updates) == 123
    updates = read_updates_and_set_rules(pathlib.Path("input.txt"))
    assert part1(updates) == 7024
    assert part2(updates) == 4151
    print("All tests passed.")


if __name__ == "__main__":
    main()
