// web/src/pages/Tasks.tsx
import React from "react";
import { api } from "../api";

type Task = { id: string; date: string; title?: string | null; notes?: string | null };

export default function Tasks() {
  const [items, setItems] = React.useState<Task[]>([]);
  const [form, setForm] = React.useState({
    date: "",
    title: "",
    notes: "",
    hours_spent: "",
  });
  const [msg, setMsg] = React.useState<string>("");

  function toIsoDate(d: string) {
    // input type="date" already gives yyyy-mm-dd in most browsers,
    // but enforce it anyway:
    const t = new Date(d);
    if (Number.isNaN(t.getTime())) return d;
    const y = t.getFullYear();
    const m = String(t.getMonth() + 1).padStart(2, "0");
    const dd = String(t.getDate()).padStart(2, "0");
    return `${y}-${m}-${dd}`;
    // alternatively just return d if you're already getting yyyy-mm-dd
  }

  async function load() {
    setMsg("");
    const res = await api("/tasks");
    const data = await res.json();
    setItems(Array.isArray(data) ? data : []);
  }

  React.useEffect(() => {
    load();
  }, []);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setMsg("");

    const body = {
      date: form.date ? toIsoDate(form.date) : null,
      title: form.title || null,
      notes: form.notes || null,
      hours_spent: form.hours_spent ? Number(form.hours_spent) : null,
    };

    const res = await api("/tasks", {
      method: "POST",
      body: JSON.stringify(body),
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      setMsg(
        err?.detail?.[0]?.msg ||
          err?.message ||
          `Task creation failed (HTTP ${res.status})`
      );
      return;
    }

    const data = await res.json().catch(() => ({}));
    setMsg(data?.message || "Task submitted. (Notion sync requested)");

    setForm({ date: "", title: "", notes: "", hours_spent: "" });
    await load();
  }

  return (
    <div style={{ maxWidth: 720, margin: "24px auto", fontFamily: "system-ui" }}>
      <h1>Daily Tasks</h1>

      <form onSubmit={submit} style={{ display: "grid", gap: 8 }}>
        <input
          type="date"
          value={form.date}
          onChange={(e) => setForm((f) => ({ ...f, date: e.target.value }))}
          required
        />
        <input
          placeholder="Title (optional)"
          value={form.title}
          onChange={(e) => setForm((f) => ({ ...f, title: e.target.value }))}
        />
        <textarea
          placeholder="Notes"
          value={form.notes}
          onChange={(e) => setForm((f) => ({ ...f, notes: e.target.value }))}
        />
        <input
          placeholder="Hours (optional)"
          value={form.hours_spent}
          onChange={(e) =>
            setForm((f) => ({ ...f, hours_spent: e.target.value }))
          }
        />
        <button type="submit">Add Task</button>
      </form>

      {msg ? (
        <p style={{ marginTop: 12, padding: 10, background: "#f6f6f6" }}>{msg}</p>
      ) : null}

      <h2 style={{ marginTop: 24 }}>Recent Tasks</h2>
      <ul>
        {items.map((t) => (
          <li key={t.id}>
            {t.date} — <b>{t.title || "(no title)"}</b> — {t.notes}
          </li>
        ))}
      </ul>
    </div>
  );
}
