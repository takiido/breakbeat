const API_URL = process.env.API_URL;
if (!API_URL) {
  throw new Error("API_URL is not set");
}

async function request<T>(endpoint: string, method: string, params?: Record<string, string>, token?: string, body?: unknown): Promise<T> {
  const url: URL = new URL(API_URL + endpoint);
  if (params) {
    url.search = new URLSearchParams(params).toString();
  }

  const res: Response = await fetch(url, {
    method: method,
    headers: {
      "Content-Type": "application/json",
      "Authorization": token ? `Bearer ${token}` : "",
    },
    body: method !== "GET" ? JSON.stringify(body) : undefined
  });

  if (!res.ok) {
    let detail = "An error occurred";
    try {
      const error = await res.json();
      detail = error.detail || detail;
    } catch {
      detail = await res.text();
    }
    throw new Error(detail);
  }

  return await res.json() as T;
}

export async function post(endpoint: string, body?: unknown, token?: string) {
  return await request(endpoint, "POST", undefined, token, body);
}

export async function get(endpoint: string, params?: Record<string, string>, token?: string) {
  return await request(endpoint, "GET", params, token);
}

export async function patch(endpoint: string, body?: unknown, token?: string) {
  return await request(endpoint, "PATCH", undefined, token, body);
}

export async function put(endpoint: string, body?: unknown, token?: string) {
  return await request(endpoint, "PUT", undefined, token, body);
}

export async function del(endpoint: string, token?: string) {
  return await request(endpoint, "DELETE", undefined, token);
}