import pathlib
import re

import numpy as np

XMAS = re.compile(r"(?=XMAS)|(?=SAMX)")

MAS = np.array(["M", "A", "S"])
SAM = np.array(["S", "A", "M"])


def read_matrix(path: pathlib.Path) -> np.ndarray:
    return np.array([list(row) for row in path.read_text().rstrip().splitlines()])


def num_xmas_for_vector(vector: np.ndarray) -> int:
    return len(re.findall(XMAS, "".join(vector)))


def part1(matrix: np.ndarray) -> int:
    n, m = matrix.shape
    if n != m:
        raise ValueError("non-square matrix")
    count = 0
    for i in range(-n + 1, n):
        count += num_xmas_for_vector(matrix.diagonal(i)) + num_xmas_for_vector(
            np.fliplr(matrix).diagonal(i)
        )
        if i >= 0:
            count += num_xmas_for_vector(matrix[i, :]) + num_xmas_for_vector(
                matrix[:, i]
            )

    return count


def are_equal(a: np.ndarray, b: np.ndarray) -> bool:
    return np.equal(a, b).all().astype(bool)


def is_xmas(submatrix: np.ndarray) -> bool:
    return all(
        are_equal(diag, SAM) or are_equal(diag, MAS)
        for diag in [submatrix.diagonal(), np.fliplr(submatrix).diagonal()]
    )


def part2(matrix: np.ndarray) -> int:
    n, m = matrix.shape
    if n != m:
        raise ValueError("non-square matrix")
    return sum(
        is_xmas(matrix[i : i + 3, j : j + 3])
        for i in range(n - 2)
        for j in range(n - 2)
    )


def main() -> None:
    example_matrix = read_matrix(pathlib.Path("example.txt"))
    matrix = read_matrix(pathlib.Path("input.txt"))
    assert part1(example_matrix) == 18
    assert part1(matrix) == 2524
    assert part2(example_matrix) == 9
    assert part2(matrix) == 1873
    print("All tests passed.")


if __name__ == "__main__":
    main()
