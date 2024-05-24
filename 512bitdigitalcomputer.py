class NPNTransistor:
    def __init__(self):
        self.collector = 0  # Assume 0V is OFF, 1V is ON
        self.base = 0
        self.emitter = 0

    def apply_voltage(self, collector_voltage, base_voltage):
        self.collector = collector_voltage
        self.base = base_voltage if base_voltage is not None else 0
        self.emitter = 0 if self.base < 0.7 else 1  # Simple model, turn on if base voltage > 0.7V

    def get_state(self):
        return {'collector': self.collector, 'base': self.base, 'emitter': self.emitter}

class NMOSFET:
    def __init__(self):
        self.drain = 0  # Assume 0V is OFF, 1V is ON
        self.gate = 0
        self.source = 0

    def apply_voltage(self, drain_voltage, gate_voltage):
        self.drain = drain_voltage
        self.gate = gate_voltage if gate_voltage is not None else 0
        self.source = 0 if self.gate < 2 else 1  # Simple model, turn on if gate voltage > 2V

    def get_state(self):
        return {'drain': self.drain, 'gate': self.gate, 'source': self.source}

class ANDGate:
    def __init__(self):
        self.transistor1 = NPNTransistor()
        self.transistor2 = NPNTransistor()

    def apply_voltage(self, input1, input2):
        input1 = input1 if input1 is not None else 0
        input2 = input2 if input2 is not None else 0
        self.transistor1.apply_voltage(1, input1)
        self.transistor2.apply_voltage(1, input2)
        return self.get_output()

    def get_output(self):
        state1 = self.transistor1.get_state()
        state2 = self.transistor2.get_state()
        return 1 if state1['emitter'] == 1 and state2['emitter'] == 1 else 0

class ORGate:
    def __init__(self):
        self.transistor1 = NPNTransistor()
        self.transistor2 = NPNTransistor()

    def apply_voltage(self, input1, input2):
        input1 = input1 if input1 is not None else 0
        input2 = input2 if input2 is not None else 0
        self.transistor1.apply_voltage(1, input1)
        self.transistor2.apply_voltage(1, input2)
        return self.get_output()

    def get_output(self):
        state1 = self.transistor1.get_state()
        state2 = self.transistor2.get_state()
        return 1 if state1['emitter'] == 1 or state2['emitter'] == 1 else 0

class NOTGate:
    def __init__(self):
        self.transistor = NPNTransistor()

    def apply_voltage(self, input):
        input = input if input is not None else 0
        self.transistor.apply_voltage(1, input)
        return 0 if self.transistor.get_state()['emitter'] == 1 else 1

class XORGate:
    def __init__(self):
        self.and_gate1 = ANDGate()
        self.and_gate2 = ANDGate()
        self.or_gate = ORGate()
        self.not_gate1 = NOTGate()
        self.not_gate2 = NOTGate()

    def apply_voltage(self, input1, input2):
        not_input1 = self.not_gate1.apply_voltage(input1)
        not_input2 = self.not_gate2.apply_voltage(input2)

        self.and_gate1.apply_voltage(input1, not_input2)
        self.and_gate2.apply_voltage(not_input1, input2)

        and1_output = self.and_gate1.get_output()
        and2_output = self.and_gate2.get_output()

        self.or_gate.apply_voltage(and1_output, and2_output)
        return self.or_gate.get_output()

class ALU:
    def __init__(self):
        self.and_gate = ANDGate()
        self.or_gate = ORGate()
        self.xor_gate = XORGate()
        self.not_gate = NOTGate()

    def add(self, a, b):
        max_len = max(len(a), len(b))
        a = [int(bit) for bit in a]  # Convert binary strings to list of integers
        b = [int(bit) for bit in b]

        a = [0] * (max_len - len(a)) + a  # Pad with leading zeros
        b = [0] * (max_len - len(b)) + b

        sum = []
        carry = 0
        for bit_a, bit_b in zip(reversed(a), reversed(b)):
            sum_bit = self.xor_gate.apply_voltage(bit_a, bit_b)
            sum_bit = self.xor_gate.apply_voltage(sum_bit, carry)
            new_carry = self.or_gate.apply_voltage(self.and_gate.apply_voltage(bit_a, bit_b), self.and_gate.apply_voltage(self.xor_gate.apply_voltage(bit_a, bit_b), carry))
            sum.insert(0, sum_bit)
            carry = new_carry
        if carry:
            sum.insert(0, carry)
        return sum, carry



class ControlUnit:
    def __init__(self):
        self.instruction_pointer = 0
        self.instructions = []
        self.alu = ALU()

    def load_instructions(self, instructions):
        self.instructions = instructions

    def fetch_instruction(self):
        if self.instruction_pointer < len(self.instructions):
            instruction = self.instructions[self.instruction_pointer]
            self.instruction_pointer += 1
            return instruction
        return None

    def execute_instruction(self, instruction):
        operation, operands = instruction
        if operation == 'ADD':
            a, b = operands
            result, carry = self.alu.add(a, b)
            print("Executed ADD:", a, "+", b, "=", result, "Carry:", carry)

    def run(self):
        while True:
            instruction = self.fetch_instruction()
            if instruction is None:
                break
            self.execute_instruction(instruction)

class Memory:
    def __init__(self):
        self.memory = []

    def load_data(self, data):
        self.memory = data

    def read_data(self, address):
        return self.memory[address]

    def write_data(self, address, data):
        self.memory[address] = data

def read_input():
    return int(input("Enter a binary number: "), 2)

def write_output(data):
    print("Output:", bin(data)[2:])

class SimpleComputer:
    def __init__(self):
        self.memory = Memory()
        self.control_unit = ControlUnit()

    def load_program(self, program):
        self.memory.load_data(program)
        self.control_unit.load_instructions(program)

    def run(self):
        self.control_unit.run()

# Main function to run the entire computer simulation
def main():
    program = [
    ('ADD', ('0'*512, '1'*512)),  # Adding two 512-bit numbers
    ('ADD', ('1'*256 + '0'*256, '1'*256 + '0'*256)),  # Adding two other 512-bit numbers
    # Add more operations here if needed
]

    computer = SimpleComputer()
    computer.load_program(program)
    computer.run()

if __name__ == "__main__":
    main()
