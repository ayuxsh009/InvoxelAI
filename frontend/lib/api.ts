"use client";

import axios from "axios";

import { API_BASE_URL } from "@/lib/constants";
import type { DashboardData, InvoiceListResponse, User } from "@/types";

const api = axios.create({
  baseURL: API_BASE_URL
});

api.interceptors.request.use((config) => {
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

export const authApi = {
  async register(payload: { name: string; email: string; password: string; role: string }) {
    const { data } = await api.post<User>("/auth/register", payload);
    return data;
  },
  async login(payload: { email: string; password: string }) {
    const { data } = await api.post<{ access_token: string }>("/auth/login", payload);
    return data;
  },
  async me() {
    const { data } = await api.get<User>("/auth/me");
    return data;
  }
};

export const invoiceApi = {
  async upload(file: File, onProgress?: (pct: number) => void) {
    const form = new FormData();
    form.append("file", file);
    const { data } = await api.post("/invoices/upload", form, {
      headers: { "Content-Type": "multipart/form-data" },
      onUploadProgress: (event) => {
        if (!event.total) return;
        const pct = Math.round((event.loaded / event.total) * 100);
        onProgress?.(pct);
      }
    });
    return data;
  },
  async list(params: Record<string, string | number | undefined>) {
    const { data } = await api.get<InvoiceListResponse>("/invoices", { params });
    return data;
  },
  async detail(id: number) {
    const { data } = await api.get(`/invoices/${id}`);
    return data;
  },
  async updateStatus(id: number, payload: { status: string; paid_at?: string | null }) {
    const { data } = await api.patch(`/invoices/${id}/status`, payload);
    return data;
  }
};

export const analyticsApi = {
  async dashboard() {
    const { data } = await api.get<DashboardData>("/analytics/dashboard");
    return data;
  }
};

export const exportApi = {
  csvUrl: `${API_BASE_URL}/exports/csv`,
  excelUrl: `${API_BASE_URL}/exports/excel`,
  jsonUrl: `${API_BASE_URL}/exports/json`
};

export const chatApi = {
  async query(message: string) {
    const { data } = await api.post("/chat/query", { message });
    return data;
  }
};

export default api;
