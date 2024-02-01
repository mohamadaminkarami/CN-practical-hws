import socket

from dns_packet.helpers import (
    convert_bit_string_to_bytes,
    convert_domain_name_to_bytes,
    convert_number_to_bit_string,
)
from dns_packet.serializable import Serializable


class RR(Serializable):
    def __init__(
        self,
        rname: str,
        rtype: int,
        rclass: int,
        ttl: int,
        rdata: str,
    ) -> None:
        self.rname = rname
        self.rtype = rtype  # 16 bits
        self.rclass = rclass  # 16 bits
        self.ttl = ttl  # 16 bits
        self.rdata = rdata
        self.rdlength = len(socket.inet_aton(self.rdata))  # 16 bits

    def pack(self) -> bytes:
        packed_data: bytes = (
            convert_domain_name_to_bytes(self.rname)
            + convert_bit_string_to_bytes(
                convert_number_to_bit_string(self.rtype, 16)
                + convert_number_to_bit_string(self.rclass, 16)
                + convert_number_to_bit_string(self.ttl, 32)
                + convert_number_to_bit_string(self.rdlength, 16)
            )
            + socket.inet_aton(self.rdata)
        )
        return packed_data

    @classmethod
    def parse(cls, packet: bytes):
        raise NotImplementedError()
