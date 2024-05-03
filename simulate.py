from sys import argv, exit

class Simulator:
    def __init__(self):
        # Internal processor state
        self.PC = 0                     # Program Counter
        self.C = 0                      # Carry Flag
        self.Z = 0                      # Zero Flag
        self.stack = [0] * 32           # Internal Hardware Stack (32 deep?)
        self.SP = 0                     # Stack Pointer (index)
        self.reg = [0] * 16             # Registers (Note: index 0 is not writable)

        self.datamem = [0] * 256        # Data Memory
        self.instmem = [0x1000] * 2048  # Instruction Memory (preload with HLT instructions)

        self.pixel_X = 0
        self.pixel_Y = 0
        self.screen = [0] * (32*32)
        self.screenbuf = [0] * (32*32)

    def load(self, filename):
        print(f'Loading instruction memory from file {filename}...')
        with open(filename,'r') as f:
            instaddr = 0
            while True:
                # Each line in the file is 16 characters, '0' or '1'
                line = f.readline().strip('\n')         # Get rid of any extra stuff
                if len(line) != 16:                     # Break at end of file
                    break
                self.instmem[instaddr] = int(line,2)    # Convert binary string to integer
                instaddr += 1

    def execute(self, steps=None):
        print(f'Executing Instructions...')
        step = 1
        while steps==None or step <= steps:
            inst = self.instmem[self.PC]
            # Break into 4 nybbles
            opcode = (inst & 0xf000) >> 12
            arg1 = (inst & 0x0f00) >> 8
            arg2 = (inst & 0x00f0) >> 4
            arg3 = (inst & 0x000f)
            if opcode == 0:
                print(f'PC={self.PC}: NOP')
                self.PC += 1
            elif opcode == 1:
                print(f'PC={self.PC}: HLT')
                return step
            elif opcode == 2:
                print(f'PC={self.PC}: ADD r{arg1} r{arg2} r{arg3}')
                temp = self.reg[arg2] + self.reg[arg3]
                self.C = (temp & 0x100) >> 8
                self.Z = 1 if (temp & 0xff) == 0 else 1
                if arg1 != 0:
                    self.reg[arg1] = temp & 0xff
                self.PC += 1
            elif opcode == 3:
                print(f'PC={self.PC}: SUB r{arg1} r{arg2} r{arg3}')
                # TBD - check carry flag behavior!
                self.C = 1 if self.reg[arg2] >= self.reg[arg3] else 0
                temp = self.reg[arg2] - self.reg[arg3]
                self.Z = 1 if (temp & 0xff) == 0 else 0
                if arg1 != 0:
                    self.reg[arg1] = temp & 0xff
                self.PC += 1
            elif opcode == 4:
                print(f'PC={self.PC}: NOR r{arg1} r{arg2} r{arg3}')
                temp = (self.reg[arg2] | self.reg[arg3]) ^ 0xff
                self.Z = 1 if temp == 0 else 0
                if arg1 != 0:
                    self.reg[arg1] = temp
                self.PC += 1
            elif opcode == 5:
                print(f'PC={self.PC}: AND r{arg1} r{arg2} r{arg3}')
                temp = self.reg[arg2] & self.reg[arg3]
                self.Z = 1 if temp == 0 else 0
                if arg1 != 0:
                    self.reg[arg1] = temp
                self.PC += 1
            elif opcode == 6:
                print(f'PC={self.PC}: XOR r{arg1} r{arg2} r{arg3}')
                temp = self.reg[arg2] ^ self.reg[arg3]
                self.Z = 1 if temp == 0 else 0
                if arg1 != 0:
                    self.reg[arg1] = temp
                self.PC += 1
            elif opcode == 7:
                print(f'PC={self.PC}: RSH r{arg1} r{arg2}')
                temp = self.reg[arg2] >> 1
                #self.Z = 1 if temp == 0 else 0
                if arg1 != 0:
                    self.reg[arg1] = temp
                self.PC += 1
            elif opcode == 8:
                imm = arg2*0x10+arg3
                print(f'PC={self.PC}: LDI r{arg1} #{imm}')
                temp = imm
                #self.Z = 1 if (temp & 0xff) == 0 else 1
                if arg1 != 0:
                    self.reg[arg1] = temp
                self.PC += 1
            elif opcode == 9:
                imm = arg2*0x10+arg3
                print(f'PC={self.PC}: ADI r{arg1} #{imm}')
                temp = self.reg[arg1] + imm
                self.C = (temp & 0x100) >> 8
                self.Z = 1 if (temp & 0xff) == 0 else 1
                if arg1 != 0:
                    self.reg[arg1] = temp & 0xff
                self.PC += 1
            elif opcode == 10:
                addr = (arg1&3)*0x100 + arg2*0x10 + arg3
                print(f'PC={self.PC}: JMP {addr}')
                self.PC = addr
            elif opcode == 11:
                addr = (arg1&3)*0x100 + arg2*0x10 + arg3
                cond = arg1 >> 2
                code = ['EQ','NE','GE','LT'][cond]
                print(f'PC={self.PC}: B{code} #{addr}')
                if cond==0 and self.Z == 1:
                    self.PC = addr
                elif cond==1 and self.Z == 0:
                    self.PC = addr
                elif cond==2 and self.C == 1:
                    self.PC = addr
                elif cond==3 and self.C == 0:
                    self.PC = addr
                else:
                    self.PC += 1
            elif opcode == 12:
                addr = (arg1&3)*0x100 + arg2*0x10 + arg3
                print(f'PC={self.PC}: CAL {addr}')
                self.stack[self.SP] = self.PC+1
                self.SP += 1
                if self.SP > 31:
                    pass # Stack overflow!
                self.PC = addr
            elif opcode == 13:
                print(f'PC={self.PC}: RET')
                self.SP -= 1
                if self.SP < 0:
                    pass # Stack underflow!
                self.PC = self.stack[self.SP]
            elif opcode == 14:
                if arg3 > 7:
                    arg3 -= 16
                print(f'PC={self.PC}: LOD r{arg1} mem[r{arg2}+{arg3}]')
                temp = self.datamem[self.reg[arg2] + arg3]
                if arg1 != 0:
                    self.reg[arg1] = temp
                self.PC += 1
            elif opcode == 15:
                if arg3 > 7:
                    arg3 -= 16
                addr = self.reg[arg2] + arg3
                data = self.reg[arg1]
                print(f'PC={self.PC}: STR r{arg1} mem[r{arg2}+{arg3}]')
                self.datamem[addr] = data
                #print(f'writing {data} to {addr}')
                if addr >= 240:
                    self.write(addr, data)
                self.PC += 1
            #for i in range(0,8):
            #    print(f'r[{i}]={self.reg[i]} ',end='')
            #print(f'C={self.C} Z={self.Z}')
            step += 1
        return step-1

    def write(self, addr, data):
        if addr == 240:
            self.pixel_X = data & 0x1f
        elif addr == 241:
            self.pixel_Y = data & 0x1f
        elif addr == 242:
            self.screenbuf[self.pixel_Y*32 + self.pixel_X] = 1
            #self.print_screenbuf()
        elif addr == 243:
            self.screenbuf[self.pixel_Y*32 + self.pixel_X] = 0
            #self.print_screenbuf()
        elif addr == 245:
            self.screen = self.screenbuf.copy()
            self.print_screen()
        elif addr == 246:
            self.screen = [0] * (32*32)

    def print_screen(self):
        print('Screen:')
        for y in range(0,32):
            for x in range(0,32):
                if self.screen[y*32+x] == 1:
                    print('1',end='')
                else:
                    print('0',end='')
            print()
        print()

    def print_screenbuf(self):
        for y in range(0,32):
            for x in range(0,32):
                if self.screenbuf[y*32+x] == 1:
                    print('1',end='')
                else:
                    print('0',end='')
            print()
        print()

def main():
    if len(argv) < 2:
        print('Usage: python simulate.py <FILENAME.MC> (numsteps)')
        exit(-1)
    else:
        filename = argv[1]
    
    if len(argv) == 3:
        steps = int(argv[2])
    else:
        steps = -1
    
    sim = Simulator()
    sim.load(filename)
    if steps == -1:
        instructions = sim.execute()
    else:
        instructions = sim.execute(steps)
    
    print(f'Exiting, executed {instructions} instructions.')

if __name__ == '__main__':
    main()