// src/auth.ts
import { api, setToken, setUser, clearAuth } from "./api";

type LoginResp = { access_token: string; user?: any };

export async function login(email: string, password: string) {
  const data = await api("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  }) as LoginResp;

  setToken(data.access_token);
  if (data.user) setUser(data.user);
  return data;
}

export function logout() {
  clearAuth();
}
