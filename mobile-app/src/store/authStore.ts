import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

interface AuthState {
  user: any | null;
  token: string | null;
  refreshToken: string | null;
  isLoading: boolean;
  error: string | null;
  login: (email: string, senha: string, applicationId: string) => Promise<void>;
  register: (nome: string, email: string, senha: string) => Promise<void>;
  refreshAccessToken: () => Promise<void>;
  logout: () => void;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  token: null,
  refreshToken: null,
  isLoading: false,
  error: null,

  login: async (email, senha, applicationId) => {
    set({ isLoading: true, error: null });
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/login/`, {
        email,
        senha,
        application_id: applicationId,
      });
      const { access, refresh, user } = response.data;
      set({ user, token: access, refreshToken: refresh, isLoading: false });
      await AsyncStorage.setItem('token', access);
      await AsyncStorage.setItem('refreshToken', refresh);
    } catch (error: any) {
      set({ isLoading: false, error: error.message || 'Login failed' });
    }
  },

  register: async (nome, email, senha) => {
    set({ isLoading: true, error: null });
    try {
      await axios.post(`${API_BASE_URL}/auth/register/`, {
        nome,
        email,
        senha,
        senha_confirmacao: senha,
      });
      set({ isLoading: false });
      // Optionally auto-login after register
    } catch (error: any) {
      set({ isLoading: false, error: error.message || 'Registration failed' });
    }
  },

  refreshAccessToken: async () => {
    const { refreshToken } = get();
    if (!refreshToken) return;
    try {
      const response = await axios.post(`${API_BASE_URL}/auth/refresh/`, {
        refresh: refreshToken,
      });
      const { access } = response.data;
      set({ token: access });
      await AsyncStorage.setItem('token', access);
    } catch (error) {
      // Handle refresh failure, maybe logout
    }
  },

  logout: () => {
    set({ user: null, token: null, refreshToken: null });
    AsyncStorage.removeItem('token');
    AsyncStorage.removeItem('refreshToken');
  },

  clearError: () => set({ error: null }),
}));
