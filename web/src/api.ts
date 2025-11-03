// src/api.ts
export const API =
  (import.meta as any).env?.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

let _token: string | null = localStorage.getItem('mcg_token');
let _user: any = null;
try {
  const raw = localStorage.getItem('mcg_user');
  _user = raw ? JSON.parse(raw) : null;
} catch { _user = null; }

export function getToken() {
  return _token;
}
export function setToken(t: string | null) {
  _token = t;
  if (t) localStorage.setItem('mcg_token', t);
  else localStorage.removeItem('mcg_token');
}

export function getUser() {
  return _user;
}
export function setUser(u: any | null) {
  _user = u;
  if (u) localStorage.setItem('mcg_user', JSON.stringify(u));
  else localStorage.removeItem('mcg_user');
}

export function clearAuth() {
  setToken(null);
  setUser(null);
}

export async function api(path: string, options: RequestInit = {}) {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> | undefined),
  };
  if (_token) headers.Authorization = `Bearer ${_token}`;

  const res = await fetch(`${API}${path}`, { ...options, headers });

  if (!res.ok) {
    let msg = `HTTP ${res.status}`;
    try {
      const j = await res.json();
      throw new Error((j && (j.detail || j.message)) || JSON.stringify(j));
    } catch (e: any) {
      throw new Error(e?.message || msg);
    }
  }

  const ct = res.headers.get('content-type') || '';
  return ct.includes('application/json') ? res.json() : res.text();
}
