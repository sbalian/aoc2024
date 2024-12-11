import pathlib
from collections import defaultdict


def read_disk_map(path: pathlib.Path) -> str:
    return path.read_text().rstrip()


def make_blocks(disk_map: str) -> list[int | None]:
    blocks: list[int | None] = []
    file_id = 0
    for i in range(len(disk_map)):
        if i % 2 == 0:
            file_length = int(disk_map[i])
            for _ in range(file_length):
                blocks.append(file_id)
            file_id += 1
        else:
            space_length = int(disk_map[i])
            for _ in range(space_length):
                blocks.append(None)
    return blocks


def move(blocks: list[int | None]):
    n = len(blocks)
    left = 0
    right = n - 1
    while left < right:
        if blocks[left] is not None:
            left += 1
        elif blocks[right] is None:
            right -= 1
        else:
            blocks[left] = blocks[right]
            blocks[right] = None
            left += 1
            right -= 1
    return blocks


def checksum(blocks: list[int | None]) -> int:
    return sum(i * block for i, block in enumerate(blocks) if block is not None)


def part1(disk_map: str) -> int:
    blocks = make_blocks(disk_map)
    move(blocks)
    return checksum(blocks)


def part2(disk_map: str) -> int:
    blocks = make_blocks(disk_map)
    file_start: dict[int, int] = {}
    file_length = defaultdict[int, int](int)
    spaces: list[list[int]] = []
    space: list[int] = []
    for i, block in enumerate(blocks):
        if block is None:
            space.append(i)
        else:
            if space:
                spaces.append(space)
            space = []
            if block not in file_start:
                file_start[block] = i
            file_length[block] += 1

    for file in reversed(file_start):
        for space in spaces:
            if file_length[file] <= len(space) and space[0] <= file_start[file]:
                c = 0
                for i in range(file_start[file], file_start[file] + file_length[file]):
                    blocks[i] = None
                    blocks[space[c]] = file
                    c += 1
                for _ in range(c):
                    space.pop(0)
                break
        if not space:
            spaces.remove(space)
    return checksum(blocks)


def main() -> None:
    disk_map = read_disk_map(pathlib.Path("example.txt"))
    assert part1(disk_map) == 1928
    assert part2(disk_map) == 2858

    disk_map = read_disk_map(pathlib.Path("input.txt"))
    assert part1(disk_map) == 6421128769094
    assert part2(disk_map) == 6448168620520

    print("All tests passed.")


if __name__ == "__main__":
    main()
