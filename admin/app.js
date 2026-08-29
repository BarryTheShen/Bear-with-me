const form = document.getElementById("invite-form");
const result = document.getElementById("result");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  result.classList.remove("hidden");
  result.textContent = "Creating invitation…";
  try {
    const response = await fetch("/api/admin/authority-invites", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Platform-Admin": document.getElementById("admin-token").value,
      },
      body: JSON.stringify({
        organization: document.getElementById("organization").value,
        email: document.getElementById("email").value,
      }),
    });
    const body = await response.json();
    if (!response.ok) throw new Error(body.error || "Invitation failed");
    result.textContent = `Invitation token (show once): ${body.invite_token}`;
  } catch (error) {
    result.textContent = error.message;
    result.classList.add("error");
  }
});
