import pathlib


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


def print_blocks(blocks: list[int | None]) -> None:
    to_print = ""
    for block in blocks:
        if block is None:
            to_print += "."
        else:
            to_print += str(block)
    print(to_print)


def checksum(blocks: list[int | None]) -> int:
    return sum(i * block for i, block in enumerate(blocks) if block is not None)


def part1(disk_map: str) -> int:
    blocks = make_blocks(disk_map)
    move(blocks)
    return checksum(blocks)


def main() -> None:
    disk_map = read_disk_map(pathlib.Path("example.txt"))
    assert part1(disk_map) == 1928

    disk_map = read_disk_map(pathlib.Path("input.txt"))
    assert part1(disk_map) == 6421128769094

    print("All tests passed.")


if __name__ == "__main__":
    main()
