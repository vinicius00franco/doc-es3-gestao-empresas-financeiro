import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';
import { RootState } from '../index';

const API_BASE_URL = 'http://localhost:8000/api/v1';

interface NotaFiscalState {
  notas: any[];
  isLoading: boolean;
  error: string | null;
}

const initialState: NotaFiscalState = {
  notas: [],
  isLoading: false,
  error: null,
};

export const fetchNotas = createAsyncThunk(
  'notaFiscal/fetchNotas',
  async (_, { getState }) => {
    const state = getState() as RootState;
    const response = await axios.get(`${API_BASE_URL}/invoices/`, {
      headers: { Authorization: `Bearer ${(state as any).auth.token}` },
    });
    return response.data;
  }
);

const notaFiscalSlice = createSlice({
  name: 'notaFiscal',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchNotas.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(fetchNotas.fulfilled, (state, action) => {
        state.isLoading = false;
        state.notas = action.payload;
      })
      .addCase(fetchNotas.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to fetch notas';
      });
  },
});

export default notaFiscalSlice.reducer;
