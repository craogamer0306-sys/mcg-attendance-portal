import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { getUser } from "../api";
import { logout } from "../auth";

export default function Navbar() {
  const nav = useNavigate();
  const user = getUser();

  function onLogout() {
    logout();
    nav("/login", { replace: true });
  }

  return (
    <nav style={{display:"flex",gap:14,alignItems:"center",padding:"10px 14px",borderBottom:"1px solid #eee"}}>
      <b>MCG Portal</b>
      <Link to="/dashboard">Dashboard</Link>
      <Link to="/checkin">Check-in</Link>
      <Link to="/tasks">Daily Task</Link>
      <Link to="/change-password">Change password</Link>
      <div style={{marginLeft:"auto",display:"flex",gap:10,alignItems:"center"}}>
        <span style={{opacity:.7}}>{user?.full_name || user?.email}</span>
        <button onClick={onLogout}>Logout</button>
      </div>
    </nav>
  );
}
