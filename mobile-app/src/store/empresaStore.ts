import { create } from 'zustand';
import axios from 'axios';
import { useAuthStore } from './authStore';

const API_BASE_URL = 'http://localhost:8000/api/v1';

interface Empresa {
  id: number;
  cnpj: string;
  razao_social: string;
  nome_fantasia: string;
  tipo_empresa: string;
  ativa: boolean;
  empresa_padrao: boolean;
}

interface EmpresaState {
  empresas: Empresa[];
  selectedEmpresa: Empresa | null;
  isLoading: boolean;
  error: string | null;
  fetchEmpresas: () => Promise<void>;
  selectEmpresa: (empresa: Empresa) => void;
}

export const useEmpresaStore = create<EmpresaState>((set, get) => ({
  empresas: [],
  selectedEmpresa: null,
  isLoading: false,
  error: null,

  fetchEmpresas: async () => {
    const token = useAuthStore.getState().token;
    if (!token) return;
    set({ isLoading: true, error: null });
    try {
      const response = await axios.get(`${API_BASE_URL}/empresas/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const empresas = response.data;
      set({ empresas, isLoading: false });
      if (!get().selectedEmpresa && empresas.length > 0) {
        const defaultEmpresa = empresas.find((e: Empresa) => e.empresa_padrao) || empresas[0];
        set({ selectedEmpresa: defaultEmpresa });
      }
    } catch (error: any) {
      set({ isLoading: false, error: error.message || 'Failed to fetch empresas' });
    }
  },

  selectEmpresa: (empresa) => set({ selectedEmpresa: empresa }),
}));
