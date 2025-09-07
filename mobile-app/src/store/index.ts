import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import empresaReducer from './slices/empresaSlice';
import transacaoReducer from './slices/transacaoSlice';
import assinaturaReducer from './slices/assinaturaSlice';
import notaFiscalReducer from './slices/notaFiscalSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    empresa: empresaReducer,
    transacao: transacaoReducer,
    assinatura: assinaturaReducer,
    notaFiscal: notaFiscalReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
