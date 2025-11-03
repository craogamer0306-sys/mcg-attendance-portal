import React from "react";
import { changePassword } from "../auth";

export default function ChangePassword() {
  const [oldPwd, setOld] = React.useState("");
  const [newPwd, setNew] = React.useState("");
  const [msg, setMsg] = React.useState<string | null>(null);

  async function submit(e: React.FormEvent) {
    e.preventDefault(); setMsg(null);
    try { await changePassword(oldPwd, newPwd); setMsg("Password updated ✓"); setOld(""); setNew(""); }
    catch (e:any) { setMsg(e.message || "Failed to change password"); }
  }

  return (
    <div className="page">
      <h2>Change password</h2>
      <form onSubmit={submit} className="card">
        <input type="password" required placeholder="Old password" value={oldPwd} onChange={e=>setOld(e.target.value)}/>
        <input type="password" required placeholder="New password" value={newPwd} onChange={e=>setNew(e.target.value)}/>
        <button type="submit">Update</button>
        {msg && <div className="ok">{msg}</div>}
      </form>
    </div>
  );
}
