import { create } from 'zustand';
import axios from 'axios';
import { useAuthStore } from './authStore';

const API_BASE_URL = 'http://localhost:8000/api/v1';

interface Transacao {
  id: number;
  // Add fields based on your model
}

interface TransacaoState {
  transacoes: Transacao[];
  isLoading: boolean;
  error: string | null;
  fetchTransacoes: () => Promise<void>;
}

export const useTransacaoStore = create<TransacaoState>((set) => ({
  transacoes: [],
  isLoading: false,
  error: null,

  fetchTransacoes: async () => {
    const token = useAuthStore.getState().token;
    if (!token) return;
    set({ isLoading: true, error: null });
    try {
      const response = await axios.get(`${API_BASE_URL}/transacoes/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      set({ transacoes: response.data, isLoading: false });
    } catch (error: any) {
      set({ isLoading: false, error: error.message || 'Failed to fetch transacoes' });
    }
  },
}));
