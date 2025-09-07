import { create } from 'zustand';
import axios from 'axios';
import { useAuthStore } from './authStore';

const API_BASE_URL = 'http://localhost:8000/api/v1';

interface AssinaturaState {
  planos: any[];
  assinaturaAtual: any | null;
  isLoading: boolean;
  error: string | null;
  fetchPlanos: () => Promise<void>;
}

export const useAssinaturaStore = create<AssinaturaState>((set) => ({
  planos: [],
  assinaturaAtual: null,
  isLoading: false,
  error: null,

  fetchPlanos: async () => {
    const token = useAuthStore.getState().token;
    if (!token) return;
    set({ isLoading: true, error: null });
    try {
      const response = await axios.get(`${API_BASE_URL}/planos/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      set({ planos: response.data, isLoading: false });
    } catch (error: any) {
      set({ isLoading: false, error: error.message || 'Failed to fetch planos' });
    }
  },
}));
