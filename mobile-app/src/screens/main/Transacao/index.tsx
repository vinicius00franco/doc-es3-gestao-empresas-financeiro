import React, { useEffect } from 'react';
import { View, Text, FlatList } from 'react-native';
import { useTransacaoStore } from '../../../store/transacaoStore';
import ListItem from '../../../components/ListItem';
import Loading from '../../../components/Loading';
import { styles } from './styles';

const Transacao = () => {
  const { transacoes, isLoading, fetchTransacoes } = useTransacaoStore();

  useEffect(() => {
    fetchTransacoes();
  }, []);

  if (isLoading) {
    return <Loading />;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Transações</Text>
      <FlatList
        data={transacoes}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <ListItem
            title={`Transação ${item.id}`}
          />
        )}
      />
    </View>
  );
};

export default Transacao;
