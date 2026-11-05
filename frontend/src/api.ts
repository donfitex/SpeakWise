const base = import.meta.env.VITE_API_BASE_URL || "/api/v1";
export class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message);
  }
}
export async function api<T>(path: string, init: RequestInit = {}): Promise<T> {
  const csrf =
    document.cookie
      .split("; ")
      .find((c) => c.startsWith("csrftoken="))
      ?.split("=")[1] || "";
  let response: Response;
  try {
    response = await fetch(`${base}${path}`, {
      credentials: "same-origin",
      ...init,
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": decodeURIComponent(csrf),
        ...init.headers,
      },
    });
  } catch {
    throw new ApiError(
      0,
      "You appear to be offline. Check your connection and try again.",
    );
  }
  if (!response.ok) {
    const data = await response.json().catch(() => ({}));
    throw new ApiError(
      response.status,
      data.detail ||
        Object.values(data).flat().join(" ") ||
        "Something went wrong. Please try again.",
    );
  }
  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}
