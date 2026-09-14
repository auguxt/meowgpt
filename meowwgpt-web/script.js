const API_URL = "https://meowgpt-api.onrender.com/meow";

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
