import socket
import json
import asyncio
import json

class SocksClientError(Exception):
    pass

def _prepare_payload(cmd, payload):
    if not isinstance(cmd, str):
        raise SocksClientError("Command must be a string.")
    if not isinstance(payload, dict):
        raise SocksClientError("Payload must be a dictionary.")
    return {"_cmd": cmd, **payload}

def _process_response(raw_response):
    try:
        response = json.loads(raw_response)
    except json.JSONDecodeError:
        raise SocksClientError("Received invalid JSON.")

    if not response.get("_success", False):
        raise SocksClientError(response.get("_msg", "Unknown error"))

    return response

def send_unix(cmd, payload, socket_path="/tmp/socks.sock"):
    payload_with_cmd = _prepare_payload(cmd, payload)
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.connect(socket_path)
        s.sendall(json.dumps(payload_with_cmd).encode())
        response = s.recv(2048)
        return _process_response(response)

class SocksServerError(Exception):
    pass

class SocksServer:
    def __init__(self, socket_path="/tmp/wtp_ui.sock"):
        self.socket_path = socket_path
        self.handlers = {}

    def add_handler(self, cmd, handler):
        if not callable(handler):
            raise SocksServerError("Handler must be callable")
        self.handlers[cmd] = handler

    async def handle_client(self, reader, writer):
        try:
            data = await reader.read(2048)
            message = json.loads(data.decode())

            cmd = message.get("_cmd")
            if cmd not in self.handlers:
                raise SocksServerError(f"No handler for command: {cmd}")

            # pass the full original message, including _cmd
            response_data = self.handlers[cmd](message)
            response = {"_success": True, **response_data}

        except Exception as e:
            response = {"_success": False, "_msg": str(e)}

        writer.write(json.dumps(response).encode())
        await writer.drain()
        writer.close()
        await writer.wait_closed()

    async def start(self):
        server = await asyncio.start_unix_server(
            self.handle_client, path=self.socket_path
        )
        print(f"Socks server running on {self.socket_path}")
        async with server:
            await server.serve_forever()
