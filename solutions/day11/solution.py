EXAMPLE = "125 17"
INPUT = "2 54 992917 5270417 2514 28561 0 990"


def read(arrangement: str) -> list[int]:
    return [int(stone) for stone in arrangement.split()]


def blink(stones: list[int]) -> list[int]:
    new_config: list[int] = []
    for stone in stones:
        if stone == 0:
            new_config.append(1)
        elif len(stone_str := str(stone)) % 2 == 0:
            mid = len(stone_str) // 2
            left, right = stone_str[:mid], stone_str[mid:]
            new_config.extend([int(left), int(right)])
        else:
            new_config.append(2024 * stone)
    return new_config


def part1(stones: list[int]) -> int:
    for _ in range(25):
        stones = blink(stones)
    return len(stones)


def main() -> None:
    stones = read(EXAMPLE)
    assert part1(stones) == 55312
    stones = read(INPUT)
    assert part1(stones) == 222461
    print("All tests passed.")


if __name__ == "__main__":
    main()
