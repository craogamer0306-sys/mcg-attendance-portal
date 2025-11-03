import React from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../auth";
import { API_BASE } from "../api";

export default function Login() {
  const nav = useNavigate();
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [err, setErr] = React.useState<string | null>(null);
  const [loading, setLoading] = React.useState(false);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setErr(null); setLoading(true);
    try {
      await login(email, password);
      nav("/dashboard", { replace: true });
    } catch (e:any) { setErr(e.message || "Login failed"); }
    finally { setLoading(false); }
  }

  return (
    <div className="center">
      <h1>MCG Attendance — Login</h1>
      <p style={{opacity:.6}}>API: {API_BASE}</p>
      <form onSubmit={submit} className="card">
        {err && <div className="error">{err}</div>}
        <label>Email</label>
        <input type="email" required value={email} onChange={e=>setEmail(e.target.value)} />
        <label>Password</label>
        <input type="password" required value={password} onChange={e=>setPassword(e.target.value)} />
        <button type="submit" disabled={loading}>{loading? "Signing in..." : "Login"}</button>
      </form>
    </div>
  );
}
