from pathlib import Path
import zipfile

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

root = Path("/mnt/data/meowgpt-web")
root.mkdir(exist_ok=True)

html = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MeowGPT 🐾</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <main class="app">
    <header>
      <div class="logo">🐾</div>
      <div>
        <h1>MeowGPT</h1>
        <p>Talk to the meow machine.</p>
      </div>
      <span class="status">● Online</span>
    </header>

    <section id="chat" class="chat">
      <div class="message bot">
        <div class="avatar">🐱</div>
        <div class="bubble">Meow! Send me a message 🐾</div>
      </div>
    </section>

    <form id="form" class="composer">
      <input id="input" type="text" placeholder="Type something..." autocomplete="off">
      <button id="send" type="submit">Send ➤</button>
    </form>

    <div id="error" class="error"></div>
    <footer>Powered by your FastAPI backend</footer>
  </main>

  <script src="script.js"></script>
</body>
</html>
'''

css = r'''* {
  box-sizing: border-box;
}

:root {
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  color: #f5f5f7;
  background: #09090b;
}

body {
  margin: 0;
  min-height: 100vh;
  display: grid;
  place-items: center;
  background:
    radial-gradient(circle at top, #27272a 0, #09090b 45%);
}

.app {
  width: min(720px, 94vw);
  height: min(820px, 92vh);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid #27272a;
  border-radius: 24px;
  background: rgba(15, 15, 18, 0.94);
  box-shadow: 0 24px 80px rgba(0,0,0,.45);
}

header {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 20px 22px;
  border-bottom: 1px solid #27272a;
}

.logo {
  width: 46px;
  height: 46px;
  display: grid;
  place-items: center;
  border-radius: 14px;
  background: #27272a;
  font-size: 24px;
}

h1 {
  margin: 0;
  font-size: 20px;
}

header p {
  margin: 3px 0 0;
  color: #a1a1aa;
  font-size: 13px;
}

.status {
  margin-left: auto;
  color: #86efac;
  font-size: 12px;
}

.chat {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.message {
  display: flex;
  gap: 10px;
  margin-bottom: 18px;
  animation: pop .18s ease-out;
}

.message.user {
  justify-content: flex-end;
}

.avatar {
  width: 32px;
  height: 32px;
  flex: 0 0 32px;
  display: grid;
  place-items: center;
  border-radius: 50%;
  background: #27272a;
  font-size: 16px;
}

.bubble {
  max-width: 75%;
  padding: 12px 15px;
  border-radius: 16px;
  background: #27272a;
  line-height: 1.5;
  white-space: pre-wrap;
  word-break: break-word;
}

.user .bubble {
  background: #f4f4f5;
  color: #09090b;
  border-bottom-right-radius: 5px;
}

.bot .bubble {
  border-bottom-left-radius: 5px;
}

.composer {
  display: flex;
  gap: 10px;
  padding: 16px;
  border-top: 1px solid #27272a;
}

input {
  min-width: 0;
  flex: 1;
  border: 1px solid #3f3f46;
  outline: none;
  border-radius: 14px;
  padding: 13px 15px;
  color: #fff;
  background: #18181b;
  font-size: 15px;
}

input:focus {
  border-color: #71717a;
}

button {
  border: 0;
  border-radius: 14px;
  padding: 0 18px;
  color: #09090b;
  background: #fff;
  font-weight: 700;
  cursor: pointer;
}

button:disabled {
  opacity: .5;
  cursor: wait;
}

.error {
  min-height: 0;
  padding: 0 18px;
  color: #fca5a5;
  font-size: 13px;
  text-align: center;
}

footer {
  padding: 10px;
  color: #52525b;
  font-size: 11px;
  text-align: center;
}

@keyframes pop {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: translateY(0); }
}
'''

js = r'''const API_URL = "https://meowgpt-api.onrender.com/meow";

const form = document.getElementById("form");
const input = document.getElementById("input");
const chat = document.getElementById("chat");
const send = document.getElementById("send");
const errorBox = document.getElementById("error");

function addMessage(text, type) {
  const row = document.createElement("div");
  row.className = `message ${type}`;

  if (type === "bot") {
    row.innerHTML = `
      <div class="avatar">🐱</div>
      <div class="bubble"></div>
    `;
  } else {
    row.innerHTML = `<div class="bubble"></div>`;
  }

  row.querySelector(".bubble").textContent = text;
  chat.appendChild(row);
  chat.scrollTop = chat.scrollHeight;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const text = input.value.trim();
  if (!text || send.disabled) return;

  errorBox.textContent = "";
  addMessage(text, "user");
  input.value = "";
  send.disabled = true;
  send.textContent = "Meowing...";

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json"
      },
      body: JSON.stringify({ text })
    });

    if (!response.ok) {
      throw new Error(`API returned ${response.status}`);
    }

    const data = await response.json();
    addMessage(data.response ?? "meow?", "bot");
  } catch (error) {
    errorBox.textContent =
      "Couldn't reach the MeowGPT API. Check that the API is online and CORS is enabled.";
    console.error(error);
  } finally {
    send.disabled = false;
    send.textContent = "Send ➤";
    input.focus();
  }
});
'''

(root / "index.html").write_text(html)
(root / "style.css").write_text(css)
(root / "script.js").write_text(js)

zip_path = Path("/mnt/data/meowgpt-web-ui.zip")
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for f in root.iterdir():
        z.write(f, f.name)

print(f"Created: {zip_path}")
print("Files:", [f.name for f in root.iterdir()])
