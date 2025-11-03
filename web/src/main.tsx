
import React from 'react'
import { createRoot } from 'react-dom/client'
import { createBrowserRouter, RouterProvider, Link } from 'react-router-dom'

const API = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'

function Home() {
  const [tasks, setTasks] = React.useState<any[]>([])
  const [form, setForm] = React.useState({ date: '', title: '', notes: '', hours_spent: '' })

  async function load() {
    const res = await fetch(`${API}/tasks`)
    const data = await res.json()
    setTasks(data)
  }
  React.useEffect(() => { load() }, [])

  async function addTask(e: React.FormEvent) {
    e.preventDefault()
    await fetch(`${API}/tasks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        date: form.date,
        title: form.title || null,
        notes: form.notes || null,
        hours_spent: form.hours_spent ? Number(form.hours_spent) : null
      })
    })
    setForm({ date: '', title: '', notes: '', hours_spent: '' })
    await load()
  }

  return (
    <div style={{ maxWidth: 720, margin: '20px auto', fontFamily: 'sans-serif' }}>
      <h1>MCG Attendance — Tasks (MVP)</h1>
      <p>API: {API}</p>

      <form onSubmit={addTask} style={{ display: 'grid', gap: 8 }}>
        <input required type="date" value={form.date} onChange={e => setForm({ ...form, date: e.target.value })} />
        <input placeholder="Title (optional)" value={form.title} onChange={e => setForm({ ...form, title: e.target.value })} />
        <textarea placeholder="Notes" value={form.notes} onChange={e => setForm({ ...form, notes: e.target.value })} />
        <input placeholder="Hours (optional)" value={form.hours_spent} onChange={e => setForm({ ...form, hours_spent: e.target.value })} />
        <button type="submit">Add Task</button>
      </form>

      <h2 style={{ marginTop: 24 }}>Recent Tasks</h2>
      <ul>
        {tasks.map(t => <li key={t.id}>{t.date} — <b>{t.title || '(no title)'}</b> — {t.notes}</li>)}
      </ul>
    </div>
  )
}

const router = createBrowserRouter([
  { path: '/', element: <Home /> },
])

const root = createRoot(document.getElementById('root')!)
root.render(<RouterProvider router={router} />)
