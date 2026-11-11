# Live bridge: Blender listens on 127.0.0.1:9876, runs Python sent to it on the main thread.
import bpy, socket, traceback, io, contextlib, json
srv = socket.socket(); srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("127.0.0.1", 9876)); srv.listen(1); srv.setblocking(False)
NS = {"bpy": bpy}
def tick():
    try:
        conn, _ = srv.accept()
    except BlockingIOError:
        return 0.2
    conn.setblocking(True)
    data = b""
    while not data.endswith(b"\0END\0"):
        chunk = conn.recv(65536)
        if not chunk: break
        data += chunk
    code = data[:-5].decode("utf-8")
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out):
            exec(compile(code, "<live>", "exec"), NS)
        res = {"ok": True, "out": out.getvalue()}
    except Exception:
        res = {"ok": False, "out": out.getvalue(), "err": traceback.format_exc()[-3000:]}
    conn.sendall(json.dumps(res).encode()); conn.close()
    return 0.05
bpy.app.timers.register(tick, persistent=True)
print("BRIDGE READY 9876")
