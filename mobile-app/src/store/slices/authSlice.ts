import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1'; // Adjust to your API URL

interface AuthState {
  user: any | null;
  token: string | null;
  refreshToken: string | null;
  isLoading: boolean;
  error: string | null;
}

const initialState: AuthState = {
  user: null,
  token: null,
  refreshToken: null,
  isLoading: false,
  error: null,
};

export const login = createAsyncThunk(
  'auth/login',
  async ({ email, senha, applicationId }: { email: string; senha: string; applicationId: string }) => {
    const response = await axios.post(`${API_BASE_URL}/auth/login/`, {
      email,
      senha,
      application_id: applicationId,
    });
    return response.data;
  }
);

export const register = createAsyncThunk(
  'auth/register',
  async ({ nome, email, senha }: { nome: string; email: string; senha: string }) => {
    const response = await axios.post(`${API_BASE_URL}/auth/register/`, {
      nome,
      email,
      senha,
      senha_confirmacao: senha,
    });
    return response.data;
  }
);

export const refreshToken = createAsyncThunk(
  'auth/refreshToken',
  async (refreshToken: string) => {
    const response = await axios.post(`${API_BASE_URL}/auth/refresh/`, {
      refresh: refreshToken,
    });
    return response.data;
  }
);

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    logout: (state) => {
      state.user = null;
      state.token = null;
      state.refreshToken = null;
      AsyncStorage.removeItem('token');
      AsyncStorage.removeItem('refreshToken');
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action) => {
        state.isLoading = false;
        state.user = action.payload.user;
        state.token = action.payload.access;
        state.refreshToken = action.payload.refresh;
        AsyncStorage.setItem('token', action.payload.access);
        AsyncStorage.setItem('refreshToken', action.payload.refresh);
      })
      .addCase(login.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Login failed';
      })
      .addCase(register.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })
      .addCase(register.fulfilled, (state, action) => {
        state.isLoading = false;
        // After register, maybe auto login or redirect
      })
      .addCase(register.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Registration failed';
      })
      .addCase(refreshToken.fulfilled, (state, action) => {
        state.token = action.payload.access;
        AsyncStorage.setItem('token', action.payload.access);
      });
  },
});

export const { logout, clearError } = authSlice.actions;
export default authSlice.reducer;
