export const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export const FOOD_ITEMS_URL = `${API_BASE}/v1/food-items`;
export const VISION_DETECT_URL = `${API_BASE}/v1/vision/detect-items`;

export async function apiFetch(url, token, options = {}) {
    const res = await fetch(url, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...(token && { Authorization: `Bearer ${token}` }),
            ...options.headers,
        },
    });

    if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail ?? `Request failed (${res.status})`);
    }
    if (options["method"] == "DELETE") 
        return {}

    return res.json();
}
