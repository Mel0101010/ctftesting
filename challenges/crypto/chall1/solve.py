import socket

KEY = 0x42

s = socket.socket()
s.connect(("challenge", 5001))
data = s.recv(1024).decode().strip()
s.close()

hex_flag = data.split(": ")[1]
flag = bytes([b ^ KEY for b in bytes.fromhex(hex_flag)]).decode()

print(flag)
