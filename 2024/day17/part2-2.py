"""
- list of 3 bit integers
- three registers, A, B, and C not limited to 3 bit
- eight instructions, identifies by a 3 bit opcode
- instruction pointer: starts at 0, increases by 2 each time
- 0, 1, 2, 3: opcode 0 with operand 1, opcode 2 with operand 3
two types of operands, specified by opcode:
- literal operand: is the number itself
- combo operands:

    Combo operands 0 through 3 represent literal values 0 through 3.
    Combo operand 4 represents the value of register A.
    Combo operand 5 represents the value of register B.
    Combo operand 6 represents the value of register C.
    Combo operand 7 is reserved and will not appear in valid programs.

instructions:

The adv instruction (opcode 0) performs division. The numerator is the value in the A register. 
The denominator is found by raising 2 to the power of the instruction's combo operand. 
(So, an operand of 2 would divide A by 4 (2^2); an operand of 5 would divide A by 2^B.) The result of the division operation is
truncated to an integer and then written to the A register.

The `bxl` instruction (opcode 1) calculates the bitwise XOR of register B and the instruction's literal operand, 
then stores the result in register B.

The `bst` instruction (opcode 2) calculates the value of its combo operand modulo 8 (thereby keeping only its lowest 3 bits), 
then writes that value to the B register.

The `jnz` instruction (opcode 3) does nothing if the A register is 0. However, if the A register is not zero, it jumps by setting 
the instruction pointer to the value of its literal operand; if this instruction jumps, the instruction pointer is not increased by 2 after this instruction.

The `bxc` instruction (opcode 4) calculates the bitwise XOR of register B and register C, then stores the result in register B. 
(For legacy reasons, this instruction reads an operand but ignores it.)

The `out` instruction (opcode 5) calculates the value of its combo operand modulo 8, then outputs that value. 
(If a program outputs multiple values, they are separated by commas.)

The `bdv` instruction (opcode 6) works exactly like the `adv` instruction except that the result is stored in the B register. 
(The numerator is still read from the A register.)

The `cdv` instruction (opcode 7) works exactly like the `adv` instruction except that the result is stored in the C register.
(The numerator is still read from the A register.)

program [2, 4, 1, 3, 7, 5, 0, 3, 1, 5, 4, 1, 5, 5, 3, 0]

First element(2):

Initial rega: 4 | Current rega: 0 | correct nums: [2]
Initial rega: 12 | Current rega: 1 | correct nums: [2]
Initial rega: 20 | Current rega: 2 | correct nums: [2]
Initial rega: 28 | Current rega: 3 | correct nums: [2]
Initial rega: 32 | Current rega: 4 | correct nums: [2]

opcode: 2 | operand: 4  -> bst: RegB = RegA % 8
opcode: 1 | operand: 3  -> bxl: RegB = RegA % 8 XOR 3
opcode: 7 | operand: 5  -> cdv: RegC = RegA // (2**((RegA % 8) XOR 3))
opcode: 0 | operand: 3  -> adv: RegA = RegA/ 2**3 = RegA // 8                   RegA = RegA // 8, RegB = RegA % 8 XOR 3, RegC = RegA // (2**((RegA % 8) XOR 3))
opcode: 1 | operand: 5  -> bxl: RegB = RegB XOR 5                               RegA = RegA // 8, RegB = ((RegA % 8) XOR 3) XOR 5 , RegC = RegA // (2**((RegA % 8) XOR 3))
opcode: 4 | operand: 1  -> bxc: RegB = RegB XOR RegC                            RegA = RegA // 8, RegB = (((RegA % 8) XOR 3) XOR 5) XOR (RegA // (2**((RegA % 8) XOR 3))) , RegC = RegA // (2**((RegA % 8) XOR 3))
                                                                                out = (((RegA % 8) ^ 3) ^ 5) ^ (RegA // (2**((RegA % 8) ^ 3))) % 8
# this is the only `out` operation
# --> we are only ever outputting the value
# of RegB bc of operand == 5.
----> Only correct if RegB % 8 == 2 --> only correct if RegC == 2
opcode: 5 | operand: 5 -> out: output = RegB % 8 -----> out = ((RegA % 8 ^ 3) ^ 5) ^ (RegA // (2**((RegA % 8) ^ 3))) % 8

opcode: 3 | operand: 0 -> go to start




second elemenet (4):

opcode: 2 | operand: 4  -> bst: RegB = (RegA // 8) % 8
opcode: 1 | operand: 3  -> bxl: RegB = ((RegA // 8) % 8) XOR 3
opcode: 7 | operand: 5  -> cdv: RegC = RegA // 2 ** RegB = (RegA // 8) // (2**(((RegA // 8) % 8) XOR 3)
opcode: 0 | operand: 3  -> adv: RegA = RegA/ 2**3 = RegA // 8  // 8
opcode: 1 | operand: 5  -> bxl: RegB = (((RegA // 8) % 8) XOR 3) XOR 5 
opcode: 4 | operand: 1  -> bxc: RegB = ((((RegA // 8) % 8) XOR 3) XOR 5)  XOR ((RegA // 8) // (2**(((RegA // 8) % 8) XOR 3))
out: RegB % 8 = ((((RegA // 8) % 8) XOR 3) XOR 5)  XOR ((RegA // 8) // (2**(((RegA // 8) % 8) XOR 3)) % 8 == 4
"""
# def get_combo(rega: int, regb: int, regc: int, operand: int) -> int:
#     if operand == 7:
#         raise ValueError("Found invalid combo operand: 7")
#     elif operand in range(4):
#         return operand
#     elif operand == 4:
#         return rega
#     elif operand == 5:
#         return regb
#     elif operand == 6:
#         return regc
#     else:
#         raise ValueError(f"Found invalid combo operand: {operand}")


# def adv(rega: int, regb: int, regc: int, operand: int, pointer: int) -> tuple[int]:
#     combo_operand = get_combo(rega, regb, regc, operand)
#     newa = rega // 2 ** combo_operand
#     return newa, regb, regc, pointer + 2

# def bxl(rega: int, regb: int, regc: int, operand: int, pointer: int) -> tuple[int]:
#     return rega, regb ^ operand, regc, pointer + 2

# def bst(rega: int, regb: int, regc: int, operand: int, pointer: int) -> tuple[int]:
#     combo_operand = get_combo(rega, regb, regc, operand)
#     return rega, combo_operand % 8, regc, pointer + 2

# def jnz(rega: int, regb: int, regc: int, operand: int, pointer: int) -> tuple[int]:
#     if rega == 0:
#         return rega, regb, regc, pointer + 2
#     if operand % 2 != 0:
#         raise ValueError(f"Found invalid new pointer value of {operand} at program position {pointer}.")
#     return rega, regb, regc, operand

# def bxc(rega: int, regb: int, regc: int, operand: int, pointer: int) -> tuple[int]:
#     return rega, regb ^ regc, regc, pointer + 2

# def out(rega: int, regb: int, regc: int, operand: int) -> int:
#     combo_operand = get_combo(rega, regb, regc, operand)
#     return combo_operand % 8

# def bdv(rega: int, regb: int, regc: int, operand: int, pointer: int) -> tuple[int]:
#     regb, _, _, pointer = adv(rega, regb, regc, operand, pointer)
#     return rega, regb, regc, pointer

# def cdv(rega: int, regb: int, regc: int, operand: int, pointer: int) -> tuple[int]:
#     regc, _, _, pointer = adv(rega, regb, regc, operand, pointer)
#     return rega, regb, regc, pointer


def do_instructions_inline(program: list[int], rega: int, regb: int, regc: int) -> list[int]:
    initial_rega = rega
    output = []
    pointer = 0
    out_count = -1
    while pointer < len(program):
        opcode = program[pointer]
        operand = program[pointer + 1]
        
        if opcode == 0:  # adv
            combo_operand = rega if operand == 4 else regb if operand == 5 else regc if operand == 6 else operand
            rega //= 2 ** combo_operand
            pointer += 2
        elif opcode == 1:  # bxl
            regb ^= operand
            pointer += 2
        elif opcode == 2:  # bst
            combo_operand = rega if operand == 4 else regb if operand == 5 else regc if operand == 6 else operand
            regb = combo_operand % 8
            pointer += 2
        elif opcode == 3:  # jnz
            if rega != 0:
                pointer = operand
            else:
                pointer += 2
        elif opcode == 4:  # bxc
            regb ^= regc
            pointer += 2
        elif opcode == 5:  # out
            combo_operand = rega if operand == 4 else regb if operand == 5 else regc if operand == 6 else operand
            new_out = combo_operand % 8
            out_count += 1
            if program[out_count] != new_out:  # early break condition
                break
            output.append(new_out)
            # if len(output) == 1:
            #     print(f"Initial rega: {initial_rega} | Current rega: {rega} | correct nums: {output}")
            pointer += 2
        elif opcode == 6:  # bdv
            combo_operand = rega if operand == 4 else regb if operand == 5 else regc if operand == 6 else operand
            regb = rega // 2 ** combo_operand
            pointer += 2
        elif opcode == 7:  # cdv
            combo_operand = rega if operand == 4 else regb if operand == 5 else regc if operand == 6 else operand
            regc = rega // 2 ** combo_operand
            pointer += 2
    
    return output

"""
RegA = RegA // 8, RegB = RegA % 8 XOR 3, RegC = RegA // (2**((RegA % 8) XOR 3))
RegA = RegA // 8, RegB = ((RegA % 8) XOR 3) XOR 5 , RegC = RegA // (2**((RegA % 8) XOR 3))
RegA = RegA // 8, RegB = (((RegA % 8) XOR 3) XOR 5) XOR (RegA // (2**((RegA % 8) XOR 3))) , RegC = RegA // (2**((RegA % 8) XOR 3))
out = (((RegA % 8) ^ 3) ^ 5) ^ (RegA // (2**((RegA % 8) ^ 3))) % 8
"""

# def solve(program: list[int]) -> int:
#     for i, num in enumerate(program):




if __name__ == '__main__':
    import re
    import time
    with open('input.txt', 'r') as t:
        content = t.read()
    nums = [int(x) for x in re.findall(r'(\d+)', content)]
    rega =  2**45
    regb = nums[1]
    regc = nums[2]
    program = nums[3:]

    assert len(program) % 2 == 0
    start = time.time()
    while True:
        if rega % 1000000000 == 0:
            stop = time.time()
            print(f"Current step: {rega}, time per 1b steps: {stop - start:.4f}s.")
            start = time.time()
        if (((( (rega // (8^15)) % 8 ) ^ 3 ) ^ 5 ) ^ ((rega // (8^15)) // (2^(((rega // (8^15)) % 8 ) ^ 3))) ) % 8 != 0:
            rega = ((rega >> 45) + 1) << 45
            continue
        print(rega)
        break
        result = do_instructions_inline(program, rega, regb, regc)
        if result == program:
            break
        rega = ((rega >> 45) + 1) << 45
    print(len(program))

    print(f"Rega: {rega}")
    print(program)
    print('\n'.join(f'opcode: {x} | operand: {y}' for x, y in zip(program[::2], program[1::2])))

"""
(((( (rega // (8^15)) % 8 ) ^ 3 ) ^ 5 ) ^ ((rega // (8^15)) // (2^(((rega // (8^15)) % 8 ) ^ 3))) ) % 8
"""