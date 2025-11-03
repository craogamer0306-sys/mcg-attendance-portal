import { api, setToken, setUser, clearAuth } from "./api";

type LoginResp = { access_token: string; user?: any };

export async function login(email: string, password: string) {
  const res = await api("/auth/login", { method: "POST", body: JSON.stringify({ email, password }) });
  if (!res.ok) throw new Error((await res.json().catch(()=>({})))?.detail || "Login failed");
  const data = (await res.json()) as LoginResp;
  setToken(data.access_token);
  if (data.user) setUser(data.user);
  return data;
}

export function logout() { clearAuth(); }

export async function changePassword(old_password: string, new_password: string) {
  const res = await api("/auth/change-password", { method:"POST", body: JSON.stringify({ old_password, new_password }) });
  if (!res.ok) throw new Error((await res.json().catch(()=>({})))?.detail || "Password change failed");
  return res.json();
}
