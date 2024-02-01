from dns_packet.constants import Opcode, RCode
from dns_packet.helpers import (
    convert_bit_string_to_bytes,
    convert_bytes_to_bit_string,
    convert_number_to_bit_string,
)


class Header(object):
    def __init__(self, id: str, rd: int, rcode: int) -> None:
        self.id = id
        self.qr = 1
        self.opcode = Opcode.STANDART_QUERY

        self.aa = 0  # Not considered
        self.tc = 0  # Not considered
        self.rd = rd
        self.ra = 0  # Not considered
        self.z = 0  # Not considered

        self.rcode = rcode

        self.qdcount = 0
        self.ancount = 0
        self.nscount = 0
        self.arcount = 0

    @classmethod
    def parse(cls, packet: bytes, starting_index=0):
        end_index = 12
        header = packet[starting_index:end_index]

        bit_string = convert_bytes_to_bit_string(header)

        id = bit_string[0:16]
        rd = int(bit_string[23])

        return cls(id=id, rd=rd, rcode=RCode.NO_ERROR), end_index

    def pack(self) -> bytes:
        bit_string: str = (
            self.id
            + convert_number_to_bit_string(number=self.qr, bit_length=1)
            + convert_number_to_bit_string(number=self.opcode, bit_length=4)
            + convert_number_to_bit_string(number=self.aa, bit_length=1)
            + convert_number_to_bit_string(number=self.tc, bit_length=1)
            + convert_number_to_bit_string(number=self.rd, bit_length=1)
            + convert_number_to_bit_string(number=self.ra, bit_length=1)
            + convert_number_to_bit_string(number=self.z, bit_length=3)
            + convert_number_to_bit_string(number=self.rcode, bit_length=4)
            + convert_number_to_bit_string(number=self.qdcount, bit_length=16)
            + convert_number_to_bit_string(number=self.ancount, bit_length=16)
            + convert_number_to_bit_string(number=self.nscount, bit_length=16)
            + convert_number_to_bit_string(number=self.arcount, bit_length=16)
        )
        return convert_bit_string_to_bytes(bit_string)
