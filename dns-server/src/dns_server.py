import asyncio
import random
from typing import Any

from dns_database import dns_database
from dns_packet import DNSPacket, RClass, RCode, RType
from dns_packet.sections import Answer, Header

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5353


class DNSServerUDPProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport: asyncio.DatagramTransport) -> None:
        self.transport = transport

    def _create_response_packet(self, request_packet: DNSPacket) -> DNSPacket:
        id = request_packet.header.id
        rd = request_packet.header.rd
        rcode = RCode.NO_ERROR
        header = Header(id=id, rd=rd, rcode=rcode)
        response_packet = DNSPacket(header)

        response_packet.add_question(request_packet.questions[0])

        domain = request_packet.questions[0].qname
        ip = dns_database.get_ip_of_domain(domain)

        if ip:
            ttl = random.randint(10, 2**32 - 1)
            answer = Answer(
                rname=domain,
                rtype=RType.A,
                rclass=RClass.IN,
                ttl=ttl,
                rdata=ip,
            )
            response_packet.add_answer(answer)

        return response_packet

    def datagram_received(self, packet: bytes, addr) -> None:
        print(f"Received packet from {addr}")
        request_packet = DNSPacket.parse(packet)

        response_packet = self._create_response_packet(request_packet=request_packet)

        print(f"Sending response packet to {addr}")
        self.transport.sendto(response_packet.pack(), addr)


async def run_dns_server(ip, port):
    print("Starting DNS server...")
    loop = asyncio.get_running_loop()

    transport, _ = await loop.create_datagram_endpoint(
        lambda: DNSServerUDPProtocol(), local_addr=(ip, port)
    )
    print(f"DNS server started at {ip}:{port}")

    try:
        await asyncio.sleep(24 * 3600)  # Serve for 24 hours.
    finally:
        transport.close()


if __name__ == "__main__":
    asyncio.run(run_dns_server(ip=SERVER_IP, port=SERVER_PORT))
