import React from "react";
import { Link, useNavigate } from "react-router-dom";

export default function Dashboard() {
  const nav = useNavigate();
  return (
    <div className="page">
      <h2>Dashboard</h2>
      <div className="grid2">
        <button onClick={()=>nav("/checkin")} className="primary">🟢 Check-in</button>
        <button onClick={()=>nav("/tasks")} className="secondary">📝 Daily Task</button>
      </div>
      <p style={{marginTop:16}}>Need to update your password? <Link to="/change-password">Change password</Link>.</p>
    </div>
  );
}
