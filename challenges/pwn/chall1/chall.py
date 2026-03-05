import socket
import threading

FLAG = "fakeflag{overflow_go_brrr}"

def handle(conn):
    conn.send(b"Enter the magic word: ")
    data = conn.recv(1024)
    # "buffer overflow" : si on envoie 64 A's ou plus, on obtient le flag
    if len(data) >= 64 and data[:64] == b"A" * 64:
        conn.send(FLAG.encode() + b"\n")
    else:
        conn.send(b"Nope\n")
    conn.close()

server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("0.0.0.0", 5002))
server.listen(5)

print("PWN challenge listening on port 5002")
while True:
    conn, _ = server.accept()
    threading.Thread(target=handle, args=(conn,)).start()
