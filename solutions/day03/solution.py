import pathlib
import re


def read_memory(path: pathlib.Path) -> str:
    return path.read_text().rstrip()


def part1(memory: str) -> int:
    pattern = re.compile(r"mul\((?P<a>\d+),(?P<b>\d+)\)")
    answer = 0
    for match in pattern.finditer(memory):
        gd = match.groupdict()
        answer += int(gd["a"]) * int(gd["b"])
    return answer


def part2(memory: str) -> int:
    pattern = re.compile(
        r"mul\((?P<a>\d+),(?P<b>\d+)\)|(?P<enable>do\(\))|(?P<disable>don't\(\))"
    )
    answer = 0
    enable = True
    for match in pattern.finditer(memory):
        gd = match.groupdict()
        if gd["enable"] is not None:
            enable = True
        elif gd["disable"] is not None:
            enable = False
        elif enable:
            answer += int(gd["a"]) * int(gd["b"])
    return answer


def main() -> None:
    memory = read_memory(pathlib.Path("input.txt"))
    assert part1(memory) == 178886550
    assert part2(memory) == 87163705
    print("All tests passed.")


if __name__ == "__main__":
    main()
