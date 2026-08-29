const accept = document.getElementById("accept-button");
const cases = document.getElementById("cases");
const list = document.getElementById("case-list");
const message = document.getElementById("message");
let session = "";

function showMessage(text, error = false) {
  message.classList.remove("hidden");
  message.textContent = text;
  message.classList.toggle("error", error);
}

async function request(path, options = {}) {
  const response = await fetch(`/api${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${session}`, ...(options.headers || {}) },
  });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(body.error || "Request failed");
  return body;
}

async function loadCases() {
  const body = await request("/authority/cases");
  list.replaceChildren();
  for (const item of body.cases) {
    const card = document.createElement("article");
    card.className = "card";
    const title = document.createElement("h3");
    title.textContent = `Case ${item.case_ref}`;
    const details = document.createElement("p");
    details.textContent = `${item.status} · ${item.place}${item.case_number ? ` · ${item.case_number}` : ""}`;
    const button = document.createElement("button");
    button.textContent = item.status === "requested" ? "Record custody" : "Mark released";
    button.disabled = item.status === "closed";
    button.addEventListener("click", async () => {
      try {
        const next = item.status === "requested" ? "in_custody" : "released";
        await request(`/authority/cases/${encodeURIComponent(item.case_ref)}`, {
          method: "POST",
          body: JSON.stringify({ status: next, case_number: "" }),
        });
        await loadCases();
      } catch (error) {
        showMessage(error.message, true);
      }
    });
    card.append(title, details, button);
    list.append(card);
  }
  cases.classList.remove("hidden");
}

accept.addEventListener("click", async () => {
  try {
    const response = await fetch("/api/authority/accept", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token: document.getElementById("invite").value, name: document.getElementById("name").value }),
    });
    const body = await response.json();
    if (!response.ok) throw new Error(body.error || "Invitation failed");
    session = body.session_token;
    document.getElementById("accept").classList.add("hidden");
    await loadCases();
  } catch (error) {
    showMessage(error.message, true);
  }
});
