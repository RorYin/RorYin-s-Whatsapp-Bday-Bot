const role = document.body.dataset.role;
let people = [];

const $ = (id) => document.getElementById(id);

function toast(message, isError = false) {
    const el = $("toast");
    el.hidden = false;
    el.textContent = message;
    el.classList.toggle("error", isError);
    setTimeout(() => { el.hidden = true; }, 4200);
}

async function api(url, options = {}) {
    const response = await fetch(url, {
        headers: { "Content-Type": "application/json", ...(options.headers || {}) },
        ...options,
    });
    const data = await response.json().catch(() => ({ ok: false, error: "Invalid response" }));
    if (response.status === 401) {
        window.location.href = "/login";
    }
    if (!response.ok || data.ok === false) {
        throw new Error(data.error || data.result || "Request failed");
    }
    return data;
}

function confirmAction({ title, body }) {
    return new Promise((resolve) => {
        const modal = $("confirm-modal");
        $("confirm-title").textContent = title;
        $("confirm-body").textContent = body;
        modal.hidden = false;
        const done = (value) => {
            modal.hidden = true;
            $("confirm-ok").onclick = null;
            $("confirm-cancel").onclick = null;
            resolve(value);
        };
        $("confirm-ok").onclick = () => done(true);
        $("confirm-cancel").onclick = () => done(false);
    });
}

function formatDateDMY(value) {
    if (!value || value === "NA") return "NA";
    const iso = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value);
    if (iso) return `${iso[3]}/${iso[2]}/${iso[1]}`;
    const dmy = /^(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})$/.exec(value);
    if (dmy) {
        const day = dmy[1].padStart(2, "0");
        const month = dmy[2].padStart(2, "0");
        let year = dmy[3];
        if (year.length === 2) year = `20${year}`;
        return `${day}/${month}/${year}`;
    }
    return value;
}

function renderPeople() {
    const query = ($("search").value || "").toLowerCase();
    const body = $("people-body");
    body.innerHTML = "";
    let visible = 0;
    people.forEach((person, index) => {
        const bday = formatDateDMY(person.bday);
        const joined = formatDateDMY(person.joining_date);
        const haystack = [person.name, person.bday, bday, person.joining_date, joined, person.chatid, person.facts]
            .join(" ")
            .toLowerCase();
        if (query && !haystack.includes(query)) return;
        visible += 1;
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${index + 1}</td>
            <td>${escapeHtml(person.name || "")}</td>
            <td>${escapeHtml(bday)}</td>
            <td>${escapeHtml(joined)}</td>
            <td>${escapeHtml(person.chatid || "")}</td>
            <td class="facts">${escapeHtml(person.facts || "")}</td>
            <td class="row-actions">
                <button class="btn" data-edit="${index}" type="button">Edit</button>
                <button class="btn danger" data-delete="${index}" type="button">Delete</button>
            </td>`;
        body.appendChild(tr);
    });
    $("people-count").textContent = `${visible} of ${people.length} records`;
}

function escapeHtml(text) {
    return String(text)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;");
}

async function loadPeople() {
    const data = await api("/api/people");
    people = data.people || [];
    renderPeople();
}

function openPersonModal(index = null) {
    const form = $("person-form");
    const person = index === null ? {} : people[index];
    $("person-title").textContent = index === null ? "Add person" : `Edit ${person.name}`;
    $("person-index").value = index === null ? "" : String(index);
    form.name.value = person.name || "";
    form.bday.value = person.bday && person.bday !== "NA" ? formatDateDMY(person.bday) : "";
    form.joining_date.value = person.joining_date && person.joining_date !== "NA" ? formatDateDMY(person.joining_date) : "";
    form.chatid.value = person.chatid || "";
    form.image_url.value = person.image_url || "";
    form.facts.value = person.facts === "NA" ? "" : (person.facts || "");
    $("person-modal").hidden = false;
}

function orNA(value) {
    return (value || "").trim() || "NA";
}

async function savePerson(event) {
    event.preventDefault();
    const form = event.target;
    const index = form.index.value;
    const payload = {
        name: form.name.value.trim(),
        bday: orNA(form.bday.value),
        joining_date: orNA(form.joining_date.value),
        chatid: orNA(form.chatid.value),
        image_url: orNA(form.image_url.value),
        facts: orNA(form.facts.value),
    };
    const confirmed = await confirmAction({
        title: index === "" ? "Add this person?" : "Save these edits?",
        body: index === ""
            ? `This will add ${payload.name} to data.json.`
            : `This will overwrite ${payload.name} in data.json.`,
    });
    if (!confirmed) return;
    if (index === "") {
        await api("/api/people", { method: "POST", body: JSON.stringify(payload) });
        toast("Person added");
    } else {
        await api(`/api/people/${index}`, { method: "PUT", body: JSON.stringify(payload) });
        toast("Data updated");
    }
    $("person-modal").hidden = true;
    await loadPeople();
}

document.querySelectorAll(".tab").forEach((button) => {
    button.addEventListener("click", () => {
        document.querySelectorAll(".tab").forEach((el) => el.classList.remove("active"));
        document.querySelectorAll(".panel").forEach((el) => el.classList.remove("active"));
        button.classList.add("active");
        $(`panel-${button.dataset.tab}`).classList.add("active");
    });
});

$("search").addEventListener("input", renderPeople);
$("add-person").addEventListener("click", () => openPersonModal());
$("person-cancel").addEventListener("click", () => { $("person-modal").hidden = true; });
$("person-form").addEventListener("submit", (event) => {
    savePerson(event).catch((err) => toast(err.message, true));
});

$("people-body").addEventListener("click", async (event) => {
    const edit = event.target.closest("[data-edit]");
    const del = event.target.closest("[data-delete]");
    try {
        if (edit) {
            openPersonModal(Number(edit.dataset.edit));
        }
        if (del) {
            const index = Number(del.dataset.delete);
            const person = people[index];
            const confirmed = await confirmAction({
                title: "Delete this person?",
                body: `This permanently removes ${person.name} from data.json.`,
            });
            if (!confirmed) return;
            await api(`/api/people/${index}`, { method: "DELETE" });
            toast("Person deleted");
            await loadPeople();
        }
    } catch (err) {
        toast(err.message, true);
    }
});

$("run-task").addEventListener("click", async () => {
    const confirmed = await confirmAction({
        title: "Run the daily task?",
        body: "This sends birthday and work-anniversary WhatsApp messages for anyone matching today, then logs results to the Telegram group. It can message a live WhatsApp group.",
    });
    if (!confirmed) return;
    try {
        const data = await api("/api/actions/run-task", {
            method: "POST",
            body: JSON.stringify({ confirmed: true }),
        });
        const log = $("action-log");
        log.hidden = false;
        log.textContent = (data.log || []).join("\n") || "Done.";
        toast("Task finished");
    } catch (err) {
        toast(err.message, true);
    }
});

$("test-whatsapp").addEventListener("click", async () => {
    const confirmed = await confirmAction({
        title: "Send a WhatsApp API test?",
        body: "This generates a sample card and sends it to the configured test WhatsApp chat through Green API. A real message will appear in that chat.",
    });
    if (!confirmed) return;
    try {
        const data = await api("/api/actions/test-whatsapp", {
            method: "POST",
            body: JSON.stringify({ confirmed: true }),
        });
        const log = $("action-log");
        log.hidden = false;
        log.textContent = data.result || "Done.";
        toast("WhatsApp test sent");
    } catch (err) {
        toast(err.message, true);
    }
});

async function loadSettings() {
    if (role !== "superadmin") return;
    const data = await api("/api/settings");
    const form = $("settings-form");
    Object.entries(data.settings).forEach(([key, value]) => {
        if (form[key]) form[key].value = value;
    });
}

if (role === "superadmin") {
    document.querySelectorAll(".toggle-secret").forEach((button) => {
        button.addEventListener("click", () => {
            const input = button.parentElement.querySelector("input");
            const show = input.type === "password";
            input.type = show ? "text" : "password";
            button.classList.toggle("is-visible", show);
            button.setAttribute("aria-label", show ? "Hide value" : "Show value");
        });
    });

    $("settings-form").addEventListener("submit", async (event) => {
        event.preventDefault();
        const form = event.currentTarget;
        const settings = {};
        Array.from(form.elements).forEach((el) => {
            if (el.name && el.tagName !== "BUTTON") settings[el.name] = el.value;
        });
        const confirmed = await confirmAction({
            title: "Save setup changes?",
            body: "This updates API keys, passwords, chat IDs, and other bot setup in settings.json. A wrong value can stop WhatsApp sending or Telegram logging.",
        });
        if (!confirmed) return;
        try {
            await api("/api/settings", {
                method: "PUT",
                body: JSON.stringify({ confirmed: true, settings }),
            });
            toast("Setup saved");
        } catch (err) {
            toast(err.message, true);
        }
    });
}

loadPeople().catch((err) => toast(err.message, true));
loadSettings().catch((err) => toast(err.message, true));
