import React, { useState } from 'react';
import { View, Text, Alert } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { login } from '../../../store/slices/authSlice';
import { RootState } from '../../../store';
import Button from '../../../components/Button';
import Input from '../../../components/Input';
import { styles } from './styles';

const Login = ({ navigation }: any) => {
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [applicationId] = useState('com.financialapp'); // Default or from config

  const dispatch = useDispatch();
  const { isLoading, error } = useSelector((state: RootState) => (state as any).auth);

  const handleLogin = () => {
    if (!email || !senha) {
      Alert.alert('Erro', 'Preencha todos os campos');
      return;
    }
    dispatch(login({ email, senha, applicationId }) as any);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Login</Text>
      <Input
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        keyboardType="email-address"
      />
      <Input
        placeholder="Senha"
        value={senha}
        onChangeText={setSenha}
        secureTextEntry
      />
      <Button
        title={isLoading ? 'Entrando...' : 'Entrar'}
        onPress={handleLogin}
        disabled={isLoading}
      />
      <Button
        title="Não tem conta? Registrar"
        onPress={() => navigation.navigate('Register')}
        variant="secondary"
      />
      {error && <Text style={styles.error}>{error}</Text>}
    </View>
  );
};

export default Login;
