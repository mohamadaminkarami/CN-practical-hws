from typing import List

from dns_packet.sections import Additional, Answer, Authority, Header, Question
from dns_packet.serializable import Serializable


class DNSPacket(Serializable):
    def __init__(self, header: Header) -> None:
        self.header: Header = header
        self.questions: List[Question] = []
        self.answers: List[Answer] = []
        self.authorities: List[Authority] = []
        self.additionals: List[Additional] = []

    def add_question(self, question: Question):
        self.questions.append(question)
        self._update_header()

    def add_answer(self, answer: Answer):
        self.answers.append(answer)
        self._update_header()

    def _update_header(self):
        self.header.qdcount = len(self.questions)
        self.header.ancount = len(self.answers)
        self.header.nscount = len(self.authorities)
        self.header.arcount = len(self.additionals)

    @classmethod
    def parse(cls, packet: bytes) -> "DNSPacket":
        header, next_start = Header.parse(packet=packet)
        dns_packet = DNSPacket(header=header)
        question = Question.parse(packet=packet, starting_index=next_start)
        dns_packet.add_question(question)

        return dns_packet

    def pack(self) -> bytes:
        self._update_header()
        data: bytes = self.header.pack()

        for question in self.questions:
            data += question.pack()

        for answer in self.answers:
            data += answer.pack()

        return data
