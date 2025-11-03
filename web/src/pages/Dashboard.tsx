// web/src/pages/Dashboard.tsx
import React from "react";
import { api } from "../api";

export default function Dashboard() {
  const [checkingIn, setCheckingIn] = React.useState(false);
  const [msg, setMsg] = React.useState<string>("");

  async function doCheckIn() {
    setMsg("");
    setCheckingIn(true);

    function getGeo(): Promise<GeolocationPosition> {
      return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
          reject(new Error("Geolocation not available in this browser"));
          return;
        }
        navigator.geolocation.getCurrentPosition(resolve, reject, {
          enableHighAccuracy: true,
          timeout: 15000,
          maximumAge: 0,
        });
      });
    }

    try {
      const pos = await getGeo();
      const lat = Number(pos.coords.latitude.toFixed(6));
      const lon = Number(pos.coords.longitude.toFixed(6));

      const res = await api("/attendance/check-in", {
        method: "POST",
        body: JSON.stringify({ lat, lon }),
      });

      // API returns { ok: boolean, message?: string, office_name?: string }
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        setMsg(
          err?.detail?.[0]?.msg ||
            err?.message ||
            `Check-in failed (HTTP ${res.status})`
        );
      } else {
        const data = await res.json();
        setMsg(
          data?.message ||
            (data?.ok ? "Checked in successfully." : "Check-in attempted.")
        );
      }
    } catch (e: any) {
      setMsg(e?.message || "Could not get location / reach server.");
    } finally {
      setCheckingIn(false);
    }
  }

  return (
    <div style={{ maxWidth: 720, margin: "24px auto", fontFamily: "system-ui" }}>
      <h1>Check-in</h1>
      <button disabled={checkingIn} onClick={doCheckIn}>
        {checkingIn ? "Checking in..." : "Check-in"}
      </button>

      {msg ? (
        <p style={{ marginTop: 12, padding: 10, background: "#f6f6f6" }}>{msg}</p>
      ) : null}
    </div>
  );
}
