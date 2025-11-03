// src/auth.ts
import { api, setToken, setUser, clearAuth } from "./api";

type LoginResp = { access_token: string; user?: any };

export async function login(email: string, password: string) {
  const data = (await api("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  })) as LoginResp;

  setToken(data.access_token);
  if (data.user) setUser(data.user);
  return data;
}

export function logout() {
  clearAuth();
}

/** Change password for the currently logged-in user */
export async function changePassword(old_password: string, new_password: string) {
  // Backend expects { old_password, new_password }
  const resp = await api("/auth/change-password", {
    method: "POST",
    body: JSON.stringify({ old_password, new_password }),
  });
  return resp; // usually { ok: true, message: "Password updated" }
}
