# usage: python send.py file.py   (or -c "code")
import socket, sys, json
code = sys.argv[2] if sys.argv[1] == "-c" else open(sys.argv[1], encoding="utf-8").read()
s = socket.create_connection(("127.0.0.1", 9876), timeout=1800)
s.sendall(code.encode() + b"\0END\0")
buf = b""
while True:
    c = s.recv(65536)
    if not c: break
    buf += c
r = json.loads(buf)
print(r["out"], end="")
if not r["ok"]: print(r["err"]); sys.exit(1)
