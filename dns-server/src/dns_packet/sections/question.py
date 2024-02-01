from dns_packet.helpers import (
    convert_bit_string_to_bytes,
    convert_bytes_to_bit_string,
    convert_bytes_to_domain_name,
    convert_domain_name_to_bytes,
)


class Question(object):
    def __init__(self, qname: str, qtype: str, qclass: str) -> None:
        self.qname = qname
        self.qtype = qtype
        self.qclass = qclass

    @classmethod
    def parse(cls, packet: bytes, starting_index=12):
        qname, next_start = convert_bytes_to_domain_name(
            packet, starting_index=starting_index
        )
        qname_encoded = packet[starting_index:next_start]
        qtype = convert_bytes_to_bit_string(packet[next_start : next_start + 2])
        next_start += 2
        qclass = convert_bytes_to_bit_string(packet[next_start : next_start + 2])
        next_start += 2

        return Question(
            qname=qname,
            qtype=qtype,
            qclass=qclass,
        )

    def pack(self):
        bit_string = self.qtype + self.qclass
        return convert_domain_name_to_bytes(self.qname) + convert_bit_string_to_bytes(
            bit_string
        )
