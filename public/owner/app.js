let token = "";
let selected = null;
let lastMessage = "";
const byId = (id) => document.getElementById(id);

function status(text, error = false) {
  const element = byId("status");
  element.textContent = text;
  element.classList.toggle("error", error);
}

async function api(path, options = {}) {
  const response = await fetch(`/api${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", ...(token ? { Authorization: `Bearer ${token}` } : {}), ...(options.headers || {}) },
  });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body.error || "Request failed");
  return body;
}

async function loadInbox() {
  const body = await api("/owner/inbox");
  const events = byId("events");
  events.replaceChildren();
  for (const event of body.events) {
    const card = document.createElement("article");
    card.className = "card";
    const title = document.createElement("h3");
    title.textContent = event.label;
    const text = document.createElement("p");
    text.textContent = `${event.place}${event.note ? ` — ${event.note}` : ""}`;
    const button = document.createElement("button");
    button.textContent = "Open chat";
    button.addEventListener("click", () => openChat(event));
    card.append(title, text, button);
    events.append(card);
  }
  byId("dashboard").classList.remove("hidden");
}

async function openChat(event) {
  selected = event;
  lastMessage = "";
  byId("chat-title").textContent = `Chat about ${event.label}`;
  byId("chat").classList.remove("hidden");
  byId("messages").replaceChildren();
  await pollMessages();
}

async function pollMessages() {
  if (!selected) return;
  const body = await api(`/owner/conversations/${encodeURIComponent(selected.conversation_ref)}/messages?after=${encodeURIComponent(lastMessage)}`);
  for (const message of body.messages) {
    const line = document.createElement("li");
    line.textContent = `${message.sender_role}: ${message.body}`;
    byId("messages").append(line);
    lastMessage = message.created_at;
  }
}

byId("register").addEventListener("click", async () => {
  try {
    const response = await fetch("/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: byId("name").value, email: byId("email").value }),
    });
    const body = await response.json();
    if (!response.ok) throw new Error(body.error || "Registration failed");
    token = body.session_token;
    byId("login").classList.add("hidden");
    await loadInbox();
    status("Owner web fallback is ready. The native app remains the notification path.");
    window.setInterval(() => pollMessages().catch(() => undefined), 2500);
  } catch (error) {
    status(error.message, true);
  }
});

byId("message-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!selected) return;
  const input = byId("message");
  try {
    await api(`/owner/conversations/${encodeURIComponent(selected.conversation_ref)}/messages`, {
      method: "POST",
      body: JSON.stringify({ body: input.value }),
    });
    input.value = "";
    await pollMessages();
  } catch (error) {
    status(error.message, true);
  }
});
