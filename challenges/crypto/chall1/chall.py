import socket
import threading

FLAG = "fakeflag{xor_is_not_crypto}"
KEY = 0x42

def handle(conn):
    encrypted = bytes([ord(c) ^ KEY for c in FLAG])
    conn.send(b"Encrypted flag: " + encrypted.hex().encode() + b"\n")
    conn.close()

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", 5001))
server.listen(5)

print("Crypto challenge listening on port 5001")
while True:
    conn, _ = server.accept()
    threading.Thread(target=handle, args=(conn,)).start()
