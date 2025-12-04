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
"""
def get_combo(rega: int, regb: int, regc: int, operand: int) -> int:
    if operand == 7:
        raise ValueError("Found invalid combo operand: 7")
    elif operand in range(4):
        return operand
    elif operand == 4:
        return rega
    elif operand == 5:
        return regb
    elif operand == 6:
        return regc
    else:
        raise ValueError(f"Found invalid combo operand: {operand}")


def adv(rega: int, regb: int, regc: int, operand: int, pointer: int) -> tuple[int]:
    combo_operand = get_combo(rega, regb, regc, operand)
    newa = rega // 2 ** combo_operand
    return newa, regb, regc, pointer + 2

def bxl(rega: int, regb: int, regc: int, operand: int, pointer: int) -> tuple[int]:
    return rega, regb ^ operand, regc, pointer + 2

def bst(rega: int, regb: int, regc: int, operand: int, pointer: int) -> tuple[int]:
    combo_operand = get_combo(rega, regb, regc, operand)
    return rega, combo_operand % 8, regc, pointer + 2

def jnz(rega: int, regb: int, regc: int, operand: int, pointer: int) -> tuple[int]:
    if rega == 0:
        return rega, regb, regc, pointer + 2
    if operand % 2 != 0:
        raise ValueError(f"Found invalid new pointer value of {operand} at program position {pointer}.")
    return rega, regb, regc, operand

def bxc(rega: int, regb: int, regc: int, operand: int, pointer: int) -> tuple[int]:
    return rega, regb ^ regc, regc, pointer + 2

def out(rega: int, regb: int, regc: int, operand: int) -> int:
    combo_operand = get_combo(rega, regb, regc, operand)
    return combo_operand % 8

def bdv(rega: int, regb: int, regc: int, operand: int, pointer: int) -> tuple[int]:
    regb, _, _, pointer = adv(rega, regb, regc, operand, pointer)
    return rega, regb, regc, pointer

def cdv(rega: int, regb: int, regc: int, operand: int, pointer: int) -> tuple[int]:
    regc, _, _, pointer = adv(rega, regb, regc, operand, pointer)
    return rega, regb, regc, pointer


def do_instructions(program: list[int], rega: int, regb: int, regc: int) -> list[int]:
    mapping = {
        0: adv,
        1: bxl,
        2: bst,
        3: jnz,
        4: bxc,
        5: out,
        6: bdv,
        7: cdv
    }
    output = []
    pointer = 0
    while True:
        if pointer > len(program) - 1:
            break
        assert pointer % 2 == 0
        opcode = program[pointer]
        operand = program[pointer + 1]
        if opcode != 5:
            rega, regb, regc, pointer = mapping[opcode](rega, regb, regc, operand, pointer)
        else:
            output.append(mapping[opcode](rega, regb, regc, operand))
            pointer += 2
    return output

if __name__ == '__main__':
    import re
    with open('input.txt', 'r') as t:
        content = t.read()
    nums = [int(x) for x in re.findall(r'(\d+)', content)]
    rega = nums[0]
    regb = nums[1]
    regc = nums[2]
    program = nums[3:]

    assert len(program) % 2 == 0
    result = do_instructions(program, rega, regb, regc)
    print(','.join(str(x) for x in result))
    