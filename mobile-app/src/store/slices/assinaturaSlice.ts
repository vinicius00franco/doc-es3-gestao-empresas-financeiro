import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';
import { RootState } from '../index';

const API_BASE_URL = 'http://localhost:8000/api/v1';

interface AssinaturaState {
  planos: any[];
  assinaturaAtual: any | null;
  isLoading: boolean;
  error: string | null;
}

const initialState: AssinaturaState = {
  planos: [],
  assinaturaAtual: null,
  isLoading: false,
  error: null,
};

export const fetchPlanos = createAsyncThunk(
  'assinatura/fetchPlanos',
  async (_, { getState }) => {
    const state = getState() as RootState;
    const response = await axios.get(`${API_BASE_URL}/planos/`, {
      headers: { Authorization: `Bearer ${(state as any).auth.token}` },
    });
    return response.data;
  }
);

const assinaturaSlice = createSlice({
  name: 'assinatura',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchPlanos.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(fetchPlanos.fulfilled, (state, action) => {
        state.isLoading = false;
        state.planos = action.payload;
      })
      .addCase(fetchPlanos.rejected, (state, action) => {
        state.isLoading = false;
        state.error = action.error.message || 'Failed to fetch planos';
      });
  },
});

export default assinaturaSlice.reducer;
