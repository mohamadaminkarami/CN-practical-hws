def convert_number_to_bit_string(number: int, bit_length: int) -> str:
    bit_string = bin(number)[2:]

    bit_string = bit_string.zfill(bit_length)

    return bit_string


def convert_bytes_to_bit_string(byte_sequence):
    bit_string = "".join(format(byte, "08b") for byte in byte_sequence)

    return bit_string


def convert_bit_string_to_bytes(bit_string) -> bytes:
    bit_string = bit_string.zfill((len(bit_string) + 7) // 8 * 8)

    byte_string = bytes(
        int(bit_string[i : i + 8], 2) for i in range(0, len(bit_string), 8)
    )

    return byte_string


def convert_bytes_to_domain_name(bytes: bytes, starting_index: int):
    domain_name = ""
    i = starting_index
    while i < len(bytes):
        label_length = bytes[i]
        if label_length == 0:
            break
        label = bytes[i + 1 : i + 1 + label_length].decode()
        domain_name += label + "."
        i += 1 + label_length

    return domain_name.rstrip("."), i + 1


def convert_domain_name_to_bytes(domain_name: str) -> bytes:
    bytes_sequence = bytearray()
    labels = domain_name.split(".")
    for label in labels:
        label_length = len(label)
        bytes_sequence.append(label_length)
        bytes_sequence.extend(label.encode())
    bytes_sequence.append(0)
    return bytes_sequence
