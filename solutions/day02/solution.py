import copy
import pathlib


def get_reports(path: pathlib.Path) -> list[list[int]]:
    return [
        [int(level) for level in report.split()]
        for report in path.read_text().rstrip().splitlines()
    ]


def is_safe(report: list[int]) -> bool:
    prev_is_diff_positive: bool | None = None
    for diff in (end - start for start, end in zip(report, report[1:])):
        is_diff_positive = diff > 0
        if not (0 < abs(diff) < 4):
            return False
        elif prev_is_diff_positive is None:
            prev_is_diff_positive = is_diff_positive
        elif prev_is_diff_positive != is_diff_positive:
            return False
    return True


def is_safe_with_removal(report: list[int]) -> bool:
    safe = is_safe(report)
    if safe:
        return True
    for i in range(len(report)):
        report_clone = copy.copy(report)
        report_clone.pop(i)
        safe = is_safe(report_clone)
        if safe:
            return True
    return False


def part1(reports: list[list[int]]) -> int:
    return sum(is_safe(report) for report in reports)


def part2(reports: list[list[int]]) -> int:
    return sum(is_safe_with_removal(report) for report in reports)


def main() -> None:
    reports = get_reports(pathlib.Path("input.txt"))
    assert part1(reports) == 572
    assert part2(reports) == 612
    print("All tests passed.")


if __name__ == "__main__":
    main()
