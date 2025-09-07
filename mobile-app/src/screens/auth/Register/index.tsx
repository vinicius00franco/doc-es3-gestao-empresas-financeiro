import React, { useState } from 'react';
import { View, Text, Alert } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { register } from '../../../store/slices/authSlice';
import { RootState } from '../../../store';
import Button from '../../../components/Button';
import Input from '../../../components/Input';
import { styles } from './styles';

const Register = ({ navigation }: any) => {
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [confirmSenha, setConfirmSenha] = useState('');

  const dispatch = useDispatch();
  const { isLoading, error } = useSelector((state: RootState) => (state as any).auth);

  const handleRegister = () => {
    if (!nome || !email || !senha || !confirmSenha) {
      Alert.alert('Erro', 'Preencha todos os campos');
      return;
    }
    if (senha !== confirmSenha) {
      Alert.alert('Erro', 'As senhas não coincidem');
      return;
    }
    dispatch(register({ nome, email, senha }) as any);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Registrar</Text>
      <Input
        placeholder="Nome"
        value={nome}
        onChangeText={setNome}
      />
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
      <Input
        placeholder="Confirmar Senha"
        value={confirmSenha}
        onChangeText={setConfirmSenha}
        secureTextEntry
      />
      <Button
        title={isLoading ? 'Registrando...' : 'Registrar'}
        onPress={handleRegister}
        disabled={isLoading}
        variant="secondary"
      />
      <Button
        title="Já tem conta? Login"
        onPress={() => navigation.goBack()}
      />
      {error && <Text style={styles.error}>{error}</Text>}
    </View>
  );
};

export default Register;
