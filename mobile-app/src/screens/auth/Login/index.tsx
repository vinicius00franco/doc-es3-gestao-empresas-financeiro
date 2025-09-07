import React, { useState } from 'react';
import { View, Text, Alert } from 'react-native';
import { useAuthStore } from '../../../store/authStore';
import Button from '../../../components/Button';
import Input from '../../../components/Input';
import { styles } from './styles';

const Login = ({ navigation }: any) => {
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [applicationId] = useState('com.financialapp'); // Default or from config

  const { login, isLoading, error, clearError } = useAuthStore();

  const handleLogin = async () => {
    if (!email || !senha) {
      Alert.alert('Erro', 'Preencha todos os campos');
      return;
    }
    clearError();
    await login(email, senha, applicationId);
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
