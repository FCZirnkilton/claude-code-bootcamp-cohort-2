// Shipyard release dashboard (first working version, built from the wireframe).

export function todayIso(now = new Date()) {
  return now.toISOString().slice(0, 10);
}

export function isOverdue(task, today = todayIso()) {
  return task.status !== "done" && Boolean(task.due) && task.due < today;
}

export function filterTasks(tasks, { owner = "", status = "pending" } = {}) {
  return tasks
    .filter((t) => (status === "all" ? true : t.status === status))
    .filter((t) => (owner ? t.owner === owner : true))
    .sort((a, b) => (a.due || "9999-12-31").localeCompare(b.due || "9999-12-31") || a.id - b.id);
}

export function computeKpis(tasks, notes, today = todayIso()) {
  return {
    open: tasks.filter((t) => t.status !== "done").length,
    done: tasks.filter((t) => t.status === "done").length,
    overdue: tasks.filter((t) => isOverdue(t, today)).length,
    notes: notes.length,
  };
}

export function uniqueOwners(tasks) {
  return [...new Set(tasks.map((t) => t.owner).filter(Boolean))].sort();
}

export function allTags(notes) {
  return [...new Set(notes.flatMap((n) => n.tags || []))].sort();
}

export function escapeHtml(text) {
  return String(text ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

export function formatBody(body) {
  return String(body ?? "").replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
}

const state = { tasks: [], notes: [], owner: "", status: "pending", q: "", tag: "" };

async function loadTasks() {
  try {
    const res = await fetch("/api/tasks");
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    state.tasks = await res.json();
  } catch (err) {
    console.error("Could not load tasks", err);
    state.tasks = [];
  }
}

async function loadNotes() {
  try {
    const params = new URLSearchParams();
    if (state.q) params.set("q", state.q);
    if (state.tag) params.set("tag", state.tag);
    const res = await fetch(`/api/notes?${params}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    state.notes = await res.json();
  } catch (err) {
    console.error("Could not load notes", err);
    state.notes = [];
  }
}

function renderKpis() {
  const k = computeKpis(state.tasks, state.notes);
  document.getElementById("kpi-open").textContent = k.open;
  document.getElementById("kpi-done").textContent = k.done;
  document.getElementById("kpi-overdue").textContent = k.overdue;
  document.getElementById("kpi-notes").textContent = k.notes;
}

function renderOwnerFilter() {
  const select = document.getElementById("owner-filter");
  const current = select.value;
  select.innerHTML = '<option value="">All owners</option>' +
    uniqueOwners(state.tasks).map((o) => `<option value="${escapeHtml(o)}">${escapeHtml(o)}</option>`).join("");
  select.value = current;
}

function renderTasks() {
  const rows = filterTasks(state.tasks, state);
  const body = document.getElementById("tasks-body");
  body.innerHTML = rows.map((t) => `
    <tr class="${isOverdue(t) ? "overdue" : ""}">
      <td>${escapeHtml(t.title)}</td>
      <td>${escapeHtml(t.owner || "–")}</td>
      <td>${escapeHtml(t.due || "–")}</td>
      <td><span class="status status-${t.status}">${t.status}</span></td>
    </tr>`).join("");
  document.getElementById("tasks-empty").hidden = rows.length > 0;
}

function renderTags() {
  const box = document.getElementById("tag-chips");
  box.innerHTML = allTags(state.notes).map((tag) =>
    `<button class="chip ${tag === state.tag ? "active" : ""}" data-tag="${escapeHtml(tag)}">#${escapeHtml(tag)}</button>`).join("");
  box.querySelectorAll(".chip").forEach((chip) => chip.addEventListener("click", async () => {
    state.tag = state.tag === chip.dataset.tag ? "" : chip.dataset.tag;
    await loadNotes();
    renderNotes();
    renderTags();
    renderKpis();
  }));
}

function renderNotes() {
  const list = document.getElementById("notes-list");
  list.innerHTML = state.notes.map((n) => `
    <li>
      <h3>${escapeHtml(n.title)}</h3>
      <p>${formatBody(n.body)}</p>
      <div class="note-tags">${(n.tags || []).map((t) => `<span>#${escapeHtml(t)}</span>`).join("")}</div>
    </li>`).join("");
  document.getElementById("notes-empty").hidden = state.notes.length > 0;
}

function renderAll() {
  renderKpis();
  renderOwnerFilter();
  renderTasks();
  renderTags();
  renderNotes();
  document.getElementById("last-updated").textContent = `updated ${new Date().toLocaleTimeString()}`;
}

async function init() {
  document.getElementById("owner-filter").addEventListener("change", (e) => {
    state.owner = e.target.value;
    renderTasks();
  });
  document.getElementById("status-filter").addEventListener("change", (e) => {
    state.status = e.target.value;
    renderTasks();
  });
  let timer;
  document.getElementById("notes-search").addEventListener("input", (e) => {
    clearTimeout(timer);
    timer = setTimeout(async () => {
      state.q = e.target.value.trim();
      await loadNotes();
      renderNotes();
      renderTags();
      renderKpis();
    }, 200);
  });
  await Promise.all([loadTasks(), loadNotes()]);
  renderAll();
}

if (typeof document !== "undefined") init();
