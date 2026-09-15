"""Single-process state probe: memory nonce is deliberately never persisted."""
import json
import os
from pathlib import Path
import selectors
import socket
import uuid

state = {'memory_nonce': uuid.uuid4().hex, 'counter': 0}
marker = Path('/tmp/book-marker.json')
selector = selectors.DefaultSelector()
listener = socket.socket(socket.AF_UNIX)
socket_path=Path('/tmp/book-control.sock')
if socket_path.exists(): socket_path.unlink()
listener.bind(str(socket_path))
listener.listen()
listener.setblocking(False)
selector.register(listener, selectors.EVENT_READ, None)
while True:
    for key, _ in selector.select():
        if key.fileobj is listener:
            connection, _ = listener.accept()
            connection.setblocking(False)
            selector.register(connection, selectors.EVENT_READ, bytearray())
            continue
        connection, buffer = key.fileobj, key.data
        data = connection.recv(65536)
        if not data:
            selector.unregister(connection)
            connection.close()
            continue
        buffer.extend(data)
        while b'\n' in buffer:
            raw, _, tail = buffer.partition(b'\n')
            buffer[:] = tail
            request = json.loads(raw)
            if request['op'] == 'set':
                marker.write_text(json.dumps(request['marker']))
                state['counter'] += 1
            elif request['op'] == 'add':
                state['counter'] += request['value']
            elif request['op'] != 'get':
                raise ValueError('Unknown operation')
            response = dict(state, file_marker=json.loads(marker.read_text()) if marker.exists() else None,
                hostname=socket.gethostname(), pid=os.getpid(), request_id=request['request_id'])
            connection.sendall(json.dumps(response).encode()+b'\n')
