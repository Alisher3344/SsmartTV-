import axios from 'axios';

export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// withCredentials: send/receive the HttpOnly session cookie set by the backend.
const apiClient = axios.create({
  baseURL: API_URL,
  withCredentials: true,
});

// Turn a relative backend path (e.g. "/api/stream/russia1") into an absolute
// URL the <video>/hls.js player can load directly.
export const absoluteUrl = (path) =>
  path && path.startsWith('/') ? `${API_URL}${path}` : path;

export default apiClient;
