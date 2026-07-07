from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import socket
import threading
import time

# ===== YOUR ORIGINAL NETWORK CODE (trimmed a bit) =====
ANNOUNCE_PORT = 50210
CHAT_PORT = 50211
PEER_TIMEOUT = 12

_device_name = f"PiOS-{socket.gethostname()}"

class _Networking:
    def __init__(self):
        self.peers = {}
        self.chats = {}
        self.lock = threading.Lock()
        self._started = False

    def start(self):
        if self._started:
            return
        self._started = True
        threading.Thread(target=self._announce_loop, daemon=True).start()
        threading.Thread(target=self._listen_announce_loop, daemon=True).start()
        threading.Thread(target=self._listen_chat_loop, daemon=True).start()

    def _announce_loop(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        payload = f"PIOS_HELLO:{_device_name}".encode()
        while True:
            sock.sendto(payload, ("255.255.255.255", ANNOUNCE_PORT))
            time.sleep(3)

    def _listen_announce_loop(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("", ANNOUNCE_PORT))
        while True:
            data, (ip, _) = sock.recvfrom(256)
            text = data.decode()
            if text.startswith("PIOS_HELLO:"):
                name = text.split(":", 1)[1]
                with self.lock:
                    self.peers[ip] = {"name": name, "last_seen": time.time()}

    def _listen_chat_loop(self):
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.bind(("", CHAT_PORT))
        srv.listen(5)
        while True:
            conn, (ip, _) = srv.accept()
            data = conn.recv(1024).decode()
            if data.startswith("MSG "):
                msg = data[4:].strip()
                with self.lock:
                    self.chats.setdefault(ip, []).append(("them", msg))
            conn.close()

    def send_text(self, ip, text):
        try:
            with socket.create_connection((ip, CHAT_PORT)) as s:
                s.sendall(f"MSG {text}\n".encode())
            with self.lock:
                self.chats.setdefault(ip, []).append(("me", text))
            return True
        except:
            return False

    def live_peers(self):
        now = time.time()
        with self.lock:
            return {
                ip: p for ip, p in self.peers.items()
                if now - p["last_seen"] < PEER_TIMEOUT
            }

_net = _Networking()

# ===== FLASK =====
app = Flask(__name__)
CORS(app)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>PiOS Chat</title>
</head>
<body style="background:#111;color:white;font-family:sans-serif">

<h2>Peers</h2>
<div id="peers"></div>

<h2>Chat</h2>
<div id="chat"></div>

<input id="msg" placeholder="type message">
<button onclick="send()">Send</button>

<script>
let currentIP = null;

async function loadPeers() {
  const res = await fetch("/peers");
  const peers = await res.json();

  let html = "";
  for (let ip in peers) {
    html += `<button onclick="openChat('${ip}')">
      ${peers[ip].name} (${ip})
    </button><br>`;
  }
  document.getElementById("peers").innerHTML = html;
}

async function openChat(ip) {
  currentIP = ip;
  loadChat();
}

async function loadChat() {
  if (!currentIP) return;
  const res = await fetch(`/chat/${currentIP}`);
  const chat = await res.json();

  let html = "";
  chat.forEach(([who, text]) => {
    html += `<div>${who}: ${text}</div>`;
  });

  document.getElementById("chat").innerHTML = html;
}

async function send() {
  const msg = document.getElementById("msg").value;

  await fetch("/send", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      ip: currentIP,
      message: msg
    })
  });

  document.getElementById("msg").value = "";
  loadChat();
}

setInterval(loadPeers, 3000);
setInterval(loadChat, 2000);
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/peers")
def peers():
    return jsonify(_net.live_peers())

@app.route("/chat/<ip>")
def chat(ip):
    return jsonify(_net.chats.get(ip, []))

@app.route("/send", methods=["POST"])
def send():
    data = request.json
    return jsonify({
        "success": _net.send_text(data["ip"], data["message"])
    })

if __name__ == "__main__":
    _net.start()
    app.run(host="0.0.0.0", port=5000)
