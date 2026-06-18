import axios from "axios";

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: 30_000,
});

api.interceptors.request.use(config => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = "Bearer " + token;
  }
  const tenant = localStorage.getItem("tenant_id");
  if (tenant) config.headers["X-Tenant-ID"] = tenant;
  return config;
});

api.interceptors.response.use(
  res => res,
  async err => {
    if (err.response?.status === 401) {
      await refreshAccessToken();
      return api.request(err.config);
    }
    return Promise.reject(err);
  }
);