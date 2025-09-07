import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';
import { RootState } from '../index';

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
}

const initialState: EmpresaState = {
  empresas: [],
  selectedEmpresa: null,
  isLoading: false,
  error: null,
};

export const fetchEmpresas = createAsyncThunk(
  'empresa/fetchEmpresas',
  async (_, { getState }) => {
    const state = getState() as RootState;
    const response = await axios.get(`${API_BASE_URL}/empresas/`, {
      headers: { Authorization: `Bearer ${state.auth.token}` },
    });
    return response.data;
  }
);

const empresaSlice = createSlice({
  name: 'empresa',
  initialState,
  reducers: {
    selectEmpresa: (state, action) => {
      state.selectedEmpresa = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchEmpresas.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(fetchEmpresas.fulfilled, (state, action) => {
        state.isLoading = false;
        state.empresas = action.payload;
        if (!state.selectedEmpresa && action.payload.length > 0) {
          state.selectedEmpresa = action.payload.find((e: Empresa) => e.empresa_padrao) || action.payload[0];
        }
      })
      .addCase(fetchEmpresas.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to fetch empresas';
      });
  },
});

export const { selectEmpresa } = empresaSlice.actions;
export default empresaSlice.reducer;
