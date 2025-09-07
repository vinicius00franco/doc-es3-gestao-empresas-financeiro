import { create } from 'zustand';
import axios from 'axios';
import { useAuthStore } from './authStore';

const API_BASE_URL = 'http://localhost:8000/api/v1';

interface NotaFiscalState {
  notas: any[];
  isLoading: boolean;
  error: string | null;
  fetchNotas: () => Promise<void>;
}

export const useNotaFiscalStore = create<NotaFiscalState>((set) => ({
  notas: [],
  isLoading: false,
  error: null,

  fetchNotas: async () => {
    const token = useAuthStore.getState().token;
    if (!token) return;
    set({ isLoading: true, error: null });
    try {
      const response = await axios.get(`${API_BASE_URL}/invoices/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      set({ notas: response.data, isLoading: false });
    } catch (error: any) {
      set({ isLoading: false, error: error.message || 'Failed to fetch notas' });
    }
  },
}));
