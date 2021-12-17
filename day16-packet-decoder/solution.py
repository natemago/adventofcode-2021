from functools import reduce

def read_input(inpf):
    with open(inpf) as f:
        return f.read().strip()

def to_bin(hex):
    return ''.join(['{:04b}'.format(int(c, 16)) for c in hex])



class Packet:

    def __init__(self, typ, version, value=None):
        self.type = typ
        self.version = version
        self.value = value
        self.packets = []
        self.is_op = typ != '100'
    
    def version_value(self):
        s = int(self.version, 2)

        if self.is_op:
            for packet in self.packets:
                s += packet.version_value()

        return s
    
    def get_value(self):
        if not self.is_op:
            return int(self.value, 2)
        values = [p.get_value() for p in self.packets]
        op = int(self.type, 2)
        if op == 0:
            return sum(values)
        elif op == 1:
            return reduce(lambda a, b: a*b, values, 1)
        elif op == 2:
            return min(values)
        elif op == 3:
            return max(values)
        elif op == 5:
            if len(values) != 2:
                raise Exception('Wrong number of subpackets - expected 2.')
            return 1 if values[0] > values[1] else 0
        elif op == 6:
            if len(values) != 2:
                raise Exception('Wrong number of subpackets - expected 2.')
            return 1 if values[0] < values[1] else 0
        elif op == 7:
            if len(values) != 2:
                raise Exception('Wrong number of subpackets - expected 2.')
            return 1 if values[0] == values[1] else 0
        else:
            raise Exception('is_op is True, but got a literal value packet.')
    
    def __str__(self):
        return '[{}:{} {}]'.format(
            int(self.version, 2),
            int(self.type, 2),
            int(self.value, 2) if not self.is_op else ', '.join([str(p) for p in self.packets]),
        )
    
    def __repr__(self):
        return self.__str__()


'''
OP packet:

123 456 7 890123456789012 3
VVV TTT I LLLLLLLLLLLLLLL .....

Value packet:
123 456 78901 23456 78901
VVV TTT 1VVVV 1VVVV 0VVVV
'''

def decode_value(packet):
    if len(packet) < 6:
        return None, len(packet)
    version = packet[0:3]
    typ     = packet[3:6]
    i = 6

    value = ''
    while True:
        curr = packet[i: i + 5]
        value += curr[1:]
        i += 5
        if curr[0] == '0':
            break
        if i >= len(packet):
            raise Exception('Invalid value packet!')

    return Packet(typ, version, value), i

def decode_op(packet):
    if len(packet) < 22:
        return None, len(packet)

    version = packet[0:3]
    typ     = packet[3:6]
    
    len_id = packet[6]

    length = None
    if len_id == '0':
        length = int(packet[7:22], 2)
        total_read = 22
    else:
        length = int(packet[7:18], 2)
        total_read = 18
    
    op = Packet(typ, version)
    

    if len_id == '1':
        curr = packet[18:]
        while length:
            sub_packet, i = decode(curr)
            curr = curr[i:]
            if sub_packet:
                op.packets.append(sub_packet)
            length -= 1
            total_read += i
    else:
        curr = packet[22:22+length]
        if length + 22 > len(packet):
            raise Exception('Cannot read another {} bits because there are only {} bits in the package.'.format(length, len(packet)))
        i = 0
        while i < length:
            sub_packet, read = decode(curr)
            curr = curr[read:]
            i += read
            if sub_packet:
                op.packets.append(sub_packet)
            total_read += read
            

    return op, total_read

def decode(packet):
    if len(packet) < 6:
        return None, len(packet)
    typ = packet[3:6]
    if typ == '100':
        return decode_value(packet)
    return decode_op(packet)


def part1(hex):
    packet = to_bin(hex)
    decoded = decode(packet)
    print(decoded)
    return decoded[0].version_value()


def part2(hex):
    packet = to_bin(hex)
    decoded = decode(packet)
    return decoded[0].get_value()

print('Part 1: ', part1(read_input('input')))
print('Part 2: ', part2(read_input('input')))