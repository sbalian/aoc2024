import pathlib

import click

SOLUTION = """\
def main() -> None:
    print("All tests passed.")


if __name__ == "__main__":
    main()
"""


@click.command()
def setup() -> None:
    solutions_dir = pathlib.Path("solutions")
    days = (day.name for day in solutions_dir.glob("*"))
    latest = max((int(day[3:]) for day in days if day != ".gitkeep"), default=0)
    if latest == 25:
        click.echo("Merry Christmas!")
        return
    next_ = "day" + f"{latest + 1}".zfill(2)
    dir_ = pathlib.Path(solutions_dir / next_)
    dir_.mkdir()
    (dir_ / "solution.py").write_text(SOLUTION)
    for name in ["input.txt", "example.txt"]:
        (dir_ / name).open("a").close()
    click.echo("Good luck!")


if __name__ == "__main__":
    setup()
