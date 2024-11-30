import pathlib

from click.testing import CliRunner

from good_morning import SOLUTION, setup


def test_good_morning(tmp_path: pathlib.Path):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path) as tf:
        solutions_dir = pathlib.Path(tf) / "solutions"
        solutions_dir.mkdir()
        (solutions_dir / ".gitkeep").open("a").close()
        for i in range(30):
            result = runner.invoke(setup)
            assert result.exit_code == 0
            if i < 25:
                assert result.output == "Good luck!\n"
                day_dir = solutions_dir / ("day" + f"{i + 1}".zfill(2))
                assert (day_dir / "solution.py").read_text() == SOLUTION
                assert (day_dir / "input.txt").read_text() == ""
                assert (day_dir / "example.txt").read_text() == ""
            else:
                assert result.output == "Merry Christmas!\n"
