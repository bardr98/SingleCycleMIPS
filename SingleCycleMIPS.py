class MIPSProcessor:
    def __init__(self, memory):
        self.memory = memory
        self.registers = [0] * 32
        self.pc = 0

    def run(self):
        output = []

        while self.pc < len(self.memory):
            # Fetch instruction from memory
            instr = self.memory[self.pc]
            self.pc += 1

            # Decode instruction
            opcode = (instr & 0xfc000000) >> 26
            rs = (instr & 0x03e00000) >> 21
            rt = (instr & 0x001f0000) >> 16
            rd = (instr & 0x0000f800) >> 11
            shift = (instr & 0x000007c0) >> 6
            funct = instr & 0x0000003f
            imm = instr & 0x0000ffff
            target = instr & 0x03ffffff

            # Execute instruction
            if opcode == 0:
                if funct == 32:  # add
                    self.registers[rd] = self.registers[rs] + self.registers[rt]
                elif funct == 34:  # sub
                    self.registers[rd] = self.registers[rs] - self.registers[rt]
                elif funct == 36:  # and
                    self.registers[rd] = self.registers[rs] & self.registers[rt]
                elif funct == 37:  # or
                    self.registers[rd] = self.registers[rs] | self.registers[rt]
                elif funct == 42:  # slt
                    self.registers[rd] = 1 if self.registers[rs] < self.registers[rt] else 0
            elif opcode == 8:  # addi
                self.registers[rt] = self.registers[rs] + imm
            elif opcode == 35:  # lw
                address = self.registers[rs] + imm
                self.registers[rt] = self.memory[address]
            elif opcode == 43:  # sw
                address = self.registers[rs] + imm
                self.memory[address] = self.registers[rt]
            elif opcode == 4:  # beq
                if self.registers[rs] == self.registers[rt]:
                    self.pc += imm << 2
            elif opcode == 2:  # j
                self.pc = (self.pc & 0xf0000000) | (target << 2)

            # Check for halt instruction
            if instr == 0xffffffff:
                break

            # Append output to list
            output.append({
                'opcode': opcode,
                'rs': rs,
                'rt': rt,
                'rd': rd,
                'imm': imm,
                'pc': self.pc,
                'registers': list(self.registers)
            })
            return output


# Create MIPSProcessor instance and initialize memory
# 0x2008000c: addi $t0, $zero, 12
# 0x20090004: addi $t1, $zero, 4
# 0x00431020: add $v0, $a0, $v1
# 0x00831822: sub $v1, $a0, $v1
# 0x03ffffff: halt
processor = MIPSProcessor([0x2008000c, 0x20090004, 0x00431020, 0x00831822, 0x03ffffff])

# Run processor simulation
print(processor.run())
