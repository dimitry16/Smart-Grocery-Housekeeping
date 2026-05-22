const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

// Temporary dev user ID — replace with auth-derived user ID once login is implemented
const USER_ID = import.meta.env.VITE_DEV_USER_ID ?? "00000000-0000-0000-0000-000000000000";

export const FOOD_ITEMS_URL = `${API_BASE}/v1/users/${USER_ID}/food-items`;
