import asyncio
import re
from dataclasses import dataclass


class Consts:
    Connect = "CONNECT"
    ConnectionEstablished = "HTTP/1.1 200 Connection established\r\n\r\n"


@dataclass(frozen=True)
class Stream:
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter


async def handle_client(
    client_reader: asyncio.StreamReader,
    client_writer: asyncio.StreamWriter,
):
    client_stream = Stream(reader=client_reader, writer=client_writer)

    request = await client_stream.reader.read(8 * 1024)
    decoded_request = request.decode()
    print("Request Recieved to Proxy Server:\n" + decoded_request)

    method = extract_request_method(decoded_request)
    target, target_host, target_port = extract_target_info(decoded_request)

    # Connect to the target server
    target_reader, target_writer = await asyncio.open_connection(
        target_host, target_port
    )
    target_stream = Stream(reader=target_reader, writer=target_writer)
    print(f"Connected to Target: {target_host}:{target_port}")

    if method == Consts.Connect:
        await forward_https(
            request=decoded_request,
            client_stream=client_stream,
            target_stream=target_stream,
        )
    else:
        await forward_http(
            request=decoded_request,
            target=target,
            client_stream=client_stream,
            target_stream=target_stream,
        )

    client_stream.writer.close()
    await client_stream.writer.wait_closed()
    target_stream.writer.close()
    await target_stream.writer.wait_closed()


def extract_request_method(request: str):
    return request.split()[0]


async def forward_http(
    request: str,
    target: str,
    client_stream: Stream,
    target_stream: Stream,
):
    target_request = prepare_target_request(request=request, target=target)
    print("Sending request to Target:\n" + target_request)
    target_stream.writer.write(target_request.encode())
    await target_stream.writer.drain()

    await perform_forwarding(client_stream=client_stream, target_stream=target_stream)


async def forward_https(request, client_stream: Stream, target_stream: Stream):
    response = Consts.ConnectionEstablished
    print("Sending Response to Client:\n" + response)
    client_stream.writer.write(response.encode())
    await client_stream.writer.drain()

    await perform_forwarding(client_stream=client_stream, target_stream=target_stream)


def extract_target_info(request: str):
    host_header = re.search(r"Host: (.+)\r\n", request).group(1)
    host, _, port = host_header.partition(":")
    port = int(port or 80)
    return host_header, host, port


def prepare_target_request(request: str, target: str):
    full_path = request.split()[1]
    path = full_path.split(target)[-1].strip()
    return request.replace(full_path, path)


async def perform_forwarding(client_stream: Stream, target_stream: Stream):
    tasks = [
        _forward(reader=client_stream.reader, writer=target_stream.writer),
        _forward(reader=target_stream.reader, writer=client_stream.writer),
    ]

    await asyncio.gather(*tasks)


async def _forward(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    while True:
        data = await reader.read(8 * 1024)
        if not data:
            return
        writer.write(data)
        await writer.drain()


async def start_proxy_server(host: str, port: int):
    server = await asyncio.start_server(handle_client, host, port)

    async with server:
        print(f"Proxy Server Started at {host}:{port}...")
        await server.serve_forever()


if __name__ == "__main__":
    PROXY_HOST = "127.0.0.1"
    PROXY_PORT = 12345

    asyncio.run(start_proxy_server(PROXY_HOST, PROXY_PORT))
