import React from 'react';
import { ActivityIndicator, View, Text } from 'react-native';
import { styles } from './styles';

interface LoadingProps {
  message?: string;
}

const Loading = ({ message = 'Carregando...' }: LoadingProps) => {
  return (
    <View style={styles.container}>
      <ActivityIndicator size="large" color="#007bff" />
      <Text style={styles.text}>{message}</Text>
    </View>
  );
};

export default Loading;
