// 1. Get the variable from Vite (or default to localhost)
let apiUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

if (apiUrl && !apiUrl.startsWith('http')) {
    apiUrl = `https://${apiUrl}`;
}

if (apiUrl.endsWith('/')) {
    apiUrl = apiUrl.slice(0, -1);
}

export const API_BASE_URL = apiUrl;