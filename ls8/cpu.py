"""CPU functionality."""

import sys
# HLT = 0b00000001
# LDI = 0b10000010 
# PRN = 0b01000111
# MUL = 0b10100010
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
         # create the ram, registers and program-counter
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        #stack pointer
        self.sp = 256
        self.running = True
        #initiates branchtable
        self.branchtable = {
            0b00000001: self.hlt,
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b10100010: self.mul,
            0b01000101: self.push,
            0b01000110: self.pop
            }
        

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self,filename):
        """Load a program into memory."""

        # address = 0

        # For now, we've just hardcoded a program:
        try:
            address = 0
            with open(filename) as f:
                for line in f:
                    comment_split = line.split("#")
                    n = comment_split[0].strip()

                    if n == '':
                        continue

                    val = int(n, 2)
                    # store val in memory
                    self.ram[address] = val

                    address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")
            sys.exit(2)

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
    



    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b] 
        elif op == "MUL":
            val = self.reg[reg_a] * self.reg[reg_b]
           
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ldi(self, op_a, op_b):
        self.reg[op_a] = op_b
        return(3, True)

    def prn(self, op_a, op_b):
        print(self.reg[op_a])
        return (2, True)

    def hlt(self, op_a, op_b):
        return (0, False)

    def mul(self,op_a,op_b):
        self.alu("MUL",op_a,op_b)
        return(3, True)
    def push(self, op_a, op_b):
        self.sp -= 1
        value = self.reg[op_a]
        self.ram[self.sp] = value
        return (2, True)

    def pop(self, op_a, op_b):
        pop_value = self.ram[self.sp]
        reg_address = op_a
        self.reg[reg_address] = pop_value
        self.sp += 1
        return (2, True)


    def run(self):
        """Run the CPU."""
        while self.running:
            ir = self.ram_read(self.pc)
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)
            try:
                #set branch table variable to current ir
                f = self.branchtable[ir]
                #break down options to avoid keyerror
                operation_op = f(op_a, op_b)
                #run
                running = operation_op[1]
                #increment pc
                self.pc += operation_op[0]
            except:
                print(f"Error: Instruction {ir} not found")
                sys.exit(1)
        


        # while self.running:
        #     ir = self.ram_read(self.pc)
        #     op_a, op_b = self.ram[self.pc + 1] , self.ram[self.pc + 2]
            

        #     if ir == HLT:
        #         self.HLT()
        #     elif ir == LDI:
        #         self.LDI(op_a,op_b)
        #         self.pc += 3
        #     elif ir == PRN:
        #         self.PRN(op_a)
        #         self.pc += 2
        #     elif ir == MUL:
        #         self.MUL(op_a,op_b)
        #     else:
        #         print('instruction error')
        
        # # set variables
        # LDI = 0b10000010
        # PRN = 0b01000111
        # HLT = 0b00000001
        

        # while self.running:
        #     ir = self.ram[self.pc]
        #     operand_a = self.ram_read(self.pc + 1)
        #     operand_b = self.ram_read(self.pc + 2)

        #     if ir == HLT:
        #         # exit
        #         self.running = False
        #     elif ir == LDI:
        #         # Set the value of a register to an integer.
        #         self.reg[operand_a] = [operand_b]
        #         self.pc += 3
        #     elif ir == PRN:
        #         # Print numeric value stored in the given register.
        #         print(self.reg[operand_a])
        #         self.pc += 2
        #     else:
        #         print(f'unknown instruction {ir} at address {self.pc}')
        #         self.running = False
