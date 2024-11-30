import pathlib

SOLUTION = """\
import pathlib


def part1() -> str:
    input_ = pathlib.Path("input.txt").read_text().rstrip()
    return input_


def part2() -> str:
    input_ = pathlib.Path("input.txt").read_text().rstrip()
    return input_


if __name__ == "__main__":
    assert part1() == ""
    assert part2() == ""
    print("All tests passed.")
"""


def main() -> None:
    days = (day.name for day in pathlib.Path("solutions").glob("*"))
    latest = max((int(day[3:]) for day in days if day != ".gitkeep"), default=0)
    if latest == 25:
        print("Merry Christmas!")
        return
    next_ = "day" + f"{latest + 1}".zfill(2)
    dir_ = pathlib.Path(f"solutions/{next_}")
    dir_.mkdir()
    (dir_ / "solution.py").write_text(SOLUTION)
    for name in ["input.txt", "example.txt"]:
        (dir_ / name).open("a").close()
    print("Good luck!")


if __name__ == "__main__":
    main()
