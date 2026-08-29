const API = "/api";
const state = { session: "", conversation: "", lastMessage: "", timer: null };
const $ = (id) => document.getElementById(id);

function setStatus(message, error = false) {
  const box = $("status");
  box.textContent = message;
  box.classList.toggle("error", error);
}

function pathTarget() {
  const parts = window.location.pathname.split("/").filter(Boolean);
  if (parts[0] !== "f" || !parts[1]) throw new Error("This finder link is incomplete.");
  return parts[1] === "code" ? { endpoint: `/f/code/${encodeURIComponent(parts[2] || "")}` } : { endpoint: `/f/${encodeURIComponent(parts[1])}` };
}

async function json(url, options = {}) {
  const response = await fetch(`${API}${url}`, {
    ...options,
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
  });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body.error || "Something went wrong.");
  return body;
}

function addMessage(message) {
  const li = document.createElement("li");
  const sender = document.createElement("strong");
  sender.textContent = message.sender_role === "finder" ? "You" : "Owner";
  const body = document.createElement("span");
  body.textContent = message.body;
  li.append(sender, body);
  $("messages").append(li);
}

async function refreshMessages() {
  if (!state.conversation) return;
  const body = await json(`/finder/conversations/${encodeURIComponent(state.conversation)}/messages?after=${encodeURIComponent(state.lastMessage)}`, {
    headers: { "X-Finder-Session": state.session },
  });
  for (const message of body.messages) {
    addMessage(message);
    state.lastMessage = message.created_at;
  }
}

async function start() {
  try {
    const target = pathTarget();
    const existing = sessionStorage.getItem(`bwm:${target.endpoint}`);
    const opened = existing ? JSON.parse(existing) : await json(target.endpoint);
    state.session = opened.session_token;
    $("item-label").textContent = opened.label || "Found item";
    $("report").classList.remove("hidden");
    setStatus("Thanks for taking a moment to help.");

    $("authority").addEventListener("change", () => $("organization").classList.toggle("hidden", !$("authority").checked));
    $("report-form").addEventListener("submit", async (event) => {
      event.preventDefault();
      try {
        const report = await json(`/f/sessions/${encodeURIComponent(state.session)}/found`, {
          method: "POST",
          body: JSON.stringify({
            place: $("place").value,
            note: $("note").value,
            authority_organization: $("authority").checked ? $("organization").value : "",
          }),
        });
        state.conversation = report.conversation_ref;
        $("report").classList.add("hidden");
        $("chat").classList.remove("hidden");
        setStatus("The owner has been notified. You can leave a message below.");
        await refreshMessages();
        state.timer = window.setInterval(() => refreshMessages().catch(() => {}), 2500);
      } catch (error) {
        setStatus(error.message, true);
      }
    });
    $("message-form").addEventListener("submit", async (event) => {
      event.preventDefault();
      const input = $("message");
      try {
        await json(`/finder/conversations/${encodeURIComponent(state.conversation)}/messages`, {
          method: "POST",
          headers: { "X-Finder-Session": state.session },
          body: JSON.stringify({ body: input.value }),
        });
        input.value = "";
        await refreshMessages();
      } catch (error) {
        setStatus(error.message, true);
      }
    });
  } catch (error) {
    setStatus(error.message, true);
  }
}

start();
