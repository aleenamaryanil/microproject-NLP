// ─── QUICK OPTION SETS ────────────────────────────────────────────
const QUICK_OPTIONS = {
  2: ["python", "java", "web", "data", "design", "networking"],
  3: ["excellent", "good", "average"],
  4: ["technology", "analytics", "creative", "business", "science"],
  5: ["btech", "mtech", "bsc", "msc", "mba", "diploma"],
};

let currentStep = 0;

// ─── INIT ─────────────────────────────────────────────────────────
window.addEventListener("DOMContentLoaded", () => {
  initChat();
});

async function initChat() {
  await fetch("/reset", { method: "POST" });
  sendMessage("start", true);
}

// ─── SEND ─────────────────────────────────────────────────────────
async function sendMessage(text, hidden = false) {
  const input = document.getElementById("userInput");
  const message = text || input.value.trim();
  if (!message) return;

  if (!hidden) {
    appendMessage(message, "user");
    input.value = "";
  }

  clearQuickOptions();
  showTyping();

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    const data = await res.json();
    removeTyping();
    appendMessage(data.response, "bot");
    currentStep++;
    showQuickOptionsForStep(currentStep);
  } catch (err) {
    removeTyping();
    appendMessage("⚠️ Something went wrong. Please try again.", "bot");
  }
}

function handleKeyPress(e) {
  if (e.key === "Enter") sendMessage();
}

// ─── RESET ────────────────────────────────────────────────────────
async function resetChat() {
  currentStep = 0;
  clearQuickOptions();
  const container = document.getElementById("chatMessages");
  container.innerHTML = `
    <div class="welcome-msg">
      <div class="welcome-icon">🚀</div>
      <p>Starting your personalized career guidance session...</p>
    </div>`;
  await fetch("/reset", { method: "POST" });
  sendMessage("start", true);
}

// ─── RENDER ───────────────────────────────────────────────────────
function appendMessage(text, sender) {
  const container = document.getElementById("chatMessages");

  // Remove welcome message on first real message
  const welcome = container.querySelector(".welcome-msg");
  if (welcome) welcome.remove();

  const row = document.createElement("div");
  row.className = `msg-row ${sender}`;

  const avatar = document.createElement("div");
  avatar.className = "msg-avatar";
  avatar.textContent = sender === "bot" ? "🤖" : "👤";

  const bubble = document.createElement("div");
  bubble.className = "msg-bubble";
  bubble.innerHTML = text;

  row.appendChild(avatar);
  row.appendChild(bubble);
  container.appendChild(row);
  container.scrollTop = container.scrollHeight;
}

// ─── TYPING ───────────────────────────────────────────────────────
function showTyping() {
  const container = document.getElementById("chatMessages");
  const row = document.createElement("div");
  row.className = "msg-row bot";
  row.id = "typingRow";

  const avatar = document.createElement("div");
  avatar.className = "msg-avatar";
  avatar.textContent = "🤖";

  const bubble = document.createElement("div");
  bubble.className = "msg-bubble";
  bubble.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';

  row.appendChild(avatar);
  row.appendChild(bubble);
  container.appendChild(row);
  container.scrollTop = container.scrollHeight;
}

function removeTyping() {
  const row = document.getElementById("typingRow");
  if (row) row.remove();
}

// ─── QUICK OPTIONS ────────────────────────────────────────────────
function showQuickOptionsForStep(step) {
  const options = QUICK_OPTIONS[step];
  if (!options) return;
  const container = document.getElementById("quickOptions");
  container.innerHTML = "";
  options.forEach((opt) => {
    const btn = document.createElement("button");
    btn.className = "quick-btn";
    btn.textContent = opt;
    btn.onclick = () => {
      document.getElementById("userInput").value = opt;
      sendMessage();
    };
    container.appendChild(btn);
  });
}

function clearQuickOptions() {
  document.getElementById("quickOptions").innerHTML = "";
}
