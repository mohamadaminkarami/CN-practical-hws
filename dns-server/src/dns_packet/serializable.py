from abc import ABC, abstractmethod


class Serializable(ABC):
    @classmethod
    @abstractmethod
    def parse(cls, packet: bytes):
        pass

    @abstractmethod
    def pack(self) -> bytes:
        pass
