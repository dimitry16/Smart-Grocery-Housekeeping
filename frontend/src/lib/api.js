const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export const FOOD_ITEMS_URL = `${API_BASE}/v1/food-items`;
export const VISION_DETECT_URL = `${API_BASE}/v1/vision/detect`;
export const REPORTS_FREQUENTLY_USED_URL = `${API_BASE}/v1/reports/frequently-used`;
export const REPORTS_FREQUENTLY_WASTED_URL = `${API_BASE}/v1/reports/frequently-wasted`;
export const REPORTS_UNUSED_URL = `${API_BASE}/v1/reports/unused`;
