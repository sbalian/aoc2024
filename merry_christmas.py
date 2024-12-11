import importlib
import os
import pathlib
import time

import click


@click.command()
def run() -> None:
    click.echo(
        "Running all the solutions on my inputs including examples in some cases ...\n"
    )
    times = []
    solutions_dir = pathlib.Path("solutions")
    for day in sorted(
        day.name for day in solutions_dir.glob("*") if day.name != ".gitkeep"
    ):
        click.echo(f"Day: {day[3:]}")
        main = getattr(importlib.import_module(f"solutions.{day}.solution"), "main")
        os.chdir(f"solutions/{day}")
        start = time.perf_counter()
        main()
        seconds = time.perf_counter() - start
        times.append(seconds)
        click.echo(f"Took {seconds} seconds.\n")
        os.chdir("../..")
    click.echo(f"Total time: {sum(times)} seconds")


if __name__ == "__main__":
    run()
