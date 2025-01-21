class Computer:
    def __init__(self, a: int, b: int, c: int) -> None:
        self.a, self.b, self.c = a, b, c
        self.i = 0
        self.output: list[int] = []

    def combo(self, operand: int) -> int:
        match operand:
            case 0 | 1 | 2 | 3:
                return operand
            case 4:
                return self.a
            case 5:
                return self.b
            case 6:
                return self.c
            case _:
                raise RuntimeError("invalid program")

    def adv(self, operand: int) -> None:
        self.a = self.a // (2 ** self.combo(operand))
        self.i += 2

    def bxl(self, operand: int) -> None:
        self.b = self.b ^ operand
        self.i += 2

    def bst(self, operand: int) -> None:
        self.b = self.combo(operand) % 8
        self.i += 2

    def jnz(self, operand: int) -> None:
        if self.a == 0:
            self.i += 2
            return
        else:
            self.i = operand

    def bxc(self, operand: int) -> None:
        self.b = self.b ^ self.c
        self.i += 2

    def out(self, operand: int) -> None:
        self.output.append(self.combo(operand) % 8)
        self.i += 2

    def bdv(self, operand: int) -> None:
        self.b = self.a // (2 ** self.combo(operand))
        self.i += 2

    def cdv(self, operand: int) -> None:
        self.c = self.a // (2 ** self.combo(operand))
        self.i += 2

    def run_instruction(self, opcode: int, operand: int) -> None:
        match opcode:
            case 0:
                self.adv(operand)
            case 1:
                self.bxl(operand)
            case 2:
                self.bst(operand)
            case 3:
                self.jnz(operand)
            case 4:
                self.bxc(operand)
            case 5:
                self.out(operand)
            case 6:
                self.bdv(operand)
            case 7:
                self.cdv(operand)

    def run(self, program: list[int]):
        while self.i < len(program):
            self.run_instruction(program[self.i], program[self.i + 1])

    def display_output(self) -> str:
        return ",".join(str(x) for x in self.output)


def main() -> None:
    computer = Computer(30899381, 0, 0)
    computer.run([2, 4, 1, 1, 7, 5, 4, 0, 0, 3, 1, 6, 5, 5, 3, 0])
    assert computer.display_output() == "1,6,3,6,5,6,5,1,7"
    print("All tests passed.")


if __name__ == "__main__":
    main()
