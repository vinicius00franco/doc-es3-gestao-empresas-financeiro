import React, { useEffect } from 'react';
import { View, Text, FlatList } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { fetchTransacoes } from '../../../store/slices/transacaoSlice';
import { RootState } from '../../../store';
import ListItem from '../../../components/ListItem';
import Loading from '../../../components/Loading';
import { styles } from './styles';

const Transacao = () => {
  const dispatch = useDispatch();
  const { transacoes, isLoading } = useSelector((state: RootState) => (state as any).transacao);

  useEffect(() => {
    dispatch(fetchTransacoes() as any);
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
