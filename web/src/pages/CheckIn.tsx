import React from "react";
import { api } from "../api";

export default function CheckIn() {
  const [msg, setMsg] = React.useState<string>("");
  const [busy, setBusy] = React.useState(false);

  async function doCheckIn() {
    setMsg(""); setBusy(true);
    try {
      if (!("geolocation" in navigator)) { setMsg("Location not available on this device."); setBusy(false); return; }
      navigator.geolocation.getCurrentPosition(async (pos) => {
        const { latitude, longitude } = pos.coords;
        const res = await api("/attendance/check-in", {
          method: "POST",
          body: JSON.stringify({ latitude, longitude }),
        });
        const data = await res.json().catch(()=>({}));
        if (res.ok) {
          const office = data.office_name ? ` (${data.office_name})` : "";
          const status = data.status ? ` — ${data.status}` : "";
          setMsg(data.message || `Checked in${office}${status}`);
        } else {
          setMsg(data.detail || data.message || "Check-in failed");
        }
        setBusy(false);
      }, (err) => {
        setMsg(err.message || "Could not get location");
        setBusy(false);
      }, { enableHighAccuracy:true, timeout:10000 });
    } catch (e:any) {
      setMsg(e.message || "Check-in failed");
      setBusy(false);
    }
  }

  return (
    <div className="page">
      <h2>Check-in</h2>
      <p style={{opacity:.7}}>We’ll use your device GPS to verify you’re within the office radius.</p>
      <button onClick={doCheckIn} disabled={busy} className="primary">
        {busy ? "Checking..." : "Tap to Check-in"}
      </button>
      {msg && <div style={{marginTop:14}}>{msg}</div>}
    </div>
  );
}
