import sys


class CPU:
    def __init__(self):
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xf4
        self.flags = 0

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def load(self, path):
        a = 0
        p = []

        try:
            with open(path) as f:
                for line in f:
                    instr = line.split('#', 1)[0].strip()
                    if len(instr):
                        p.append(int(instr, 2))
        except FileNotFoundError:
            print(f"No such file {path}, exiting")
            sys.exit(2)

        for instr in p:
            self.ram[a] = instr
            a += 1

    def alu(self, op, reg_a, reg_b):
        if op == "CMP":
            a, b = self.reg[reg_a], self.reg[reg_b]
            if a == b:
                self.flags = 0b00000001
            elif a < b:
                self.flags = 0b00000100
            else:
                self.flags = 0b00000010

        else:
            raise Exception(f"{op} is not supported! 🚀")

    def run(self):
        self.running = True

        def stop():
            self.running = False

        def load_immediate():
            self.reg[op_a] = op_b

        def print_numeric():
            print(self.reg[op_a])

        def compare():
            self.alu("CMP", op_a, op_b)

        def jump():
            self.pc = self.reg[op_a]

        def jump_eq():
            eq = (self.flags & 0b00000001)
            if eq:
                self.pc = self.reg[op_a]
            else:
                self.pc += 2

        def jump_ne():
            eq = (self.flags & 0b00000001)
            if not eq:
                self.pc = self.reg[op_a]
            else:
                self.pc += 2

        bt = {
            0b00000001: stop,
            0b10000010: load_immediate,
            0b01000111: print_numeric,
            0b10100111: compare,
            0b01010100: jump,
            0b01010101: jump_eq,
            0b01010110: jump_ne,
        }

        while self.running:
            IR = self.ram[self.pc]
            op_count = (IR & 0b11000000) >> 6
            sets_pc = (IR & 0b00010000) >> 4

            op_a = None
            op_b = None
            if op_count > 0:
                op_a = self.ram[self.pc + 1]
            if op_count > 1:
                op_b = self.ram[self.pc + 2]

            command = bt.get(IR)

            if not command:
                print(f'Unknown instruction')
                sys.exit(1)
            command()
            if not sets_pc:
                self.pc += (op_count + 1)