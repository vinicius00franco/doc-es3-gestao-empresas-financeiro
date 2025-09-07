import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';
import { RootState } from '../index';

const API_BASE_URL = 'http://localhost:8000/api/v1';

interface Transacao {
  id: number;
  // Add fields based on your model
}

interface TransacaoState {
  transacoes: Transacao[];
  isLoading: boolean;
  error: string | null;
}

const initialState: TransacaoState = {
  transacoes: [],
  isLoading: false,
  error: null,
};

export const fetchTransacoes = createAsyncThunk(
  'transacao/fetchTransacoes',
  async (_, { getState }) => {
    const state = getState() as RootState;
    const response = await axios.get(`${API_BASE_URL}/transacoes/`, {
      headers: { Authorization: `Bearer ${(state as any).auth.token}` },
    });
    return response.data;
  }
);

const transacaoSlice = createSlice({
  name: 'transacao',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchTransacoes.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(fetchTransacoes.fulfilled, (state, action) => {
        state.isLoading = false;
        state.transacoes = action.payload;
      })
      .addCase(fetchTransacoes.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to fetch transacoes';
      });
  },
});

export default transacaoSlice.reducer;
