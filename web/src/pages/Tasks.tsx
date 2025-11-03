import React from "react";
import { api } from "../api";
type Task = { id: string; date: string; title?: string|null; notes?: string|null; hours_spent?: number|null };

export default function Tasks() {
  const [tasks, setTasks] = React.useState<Task[]>([]);
  const [form, setForm] = React.useState({ date: "", title: "", notes: "", hours_spent: "" });
  const [msg, setMsg] = React.useState<string | null>(null);

  async function load() { const r = await api("/tasks"); setTasks(await r.json()); }
  React.useEffect(()=>{ load(); }, []);

  async function addTask(e: React.FormEvent) {
    e.preventDefault(); setMsg(null);
    const r = await api("/tasks", { method:"POST", body: JSON.stringify({
      date: form.date, title: form.title || null, notes: form.notes || null,
      hours_spent: form.hours_spent ? Number(form.hours_spent) : null,
    })});
    if (!r.ok) { setMsg((await r.json().catch(()=>({})))?.detail || "Failed to add task"); return; }
    setForm({ date:"", title:"", notes:"", hours_spent:"" }); setMsg("Task added ✓"); load();
    setTimeout(()=>setMsg(null), 1500);
  }

  return (
    <div className="page">
      <h2>Daily Task</h2>
      <form onSubmit={addTask} className="card">
        <input required type="date" value={form.date} onChange={e=>setForm({...form, date:e.target.value})}/>
        <input placeholder="Title (optional)" value={form.title} onChange={e=>setForm({...form, title:e.target.value})}/>
        <textarea placeholder="Notes" value={form.notes} onChange={e=>setForm({...form, notes:e.target.value})}/>
        <input placeholder="Hours (optional)" value={form.hours_spent} onChange={e=>setForm({...form, hours_spent:e.target.value})}/>
        <button type="submit">Add Task</button>
        {msg && <div className="ok">{msg}</div>}
      </form>

      <h3 style={{marginTop:24}}>Recent</h3>
      <ul className="list">{tasks.map(t => <li key={t.id}>{t.date} — <b>{t.title || "(no title)"}</b> — {t.notes}</li>)}</ul>
    </div>
  );
}
