import React, { useEffect } from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { fetchTransacoes } from '../../store/slices/transacaoSlice';
import { RootState } from '../../store';

const TransacaoScreen = () => {
  const dispatch = useDispatch();
  const { transacoes, isLoading } = useSelector((state: RootState) => (state as any).transacao);

  useEffect(() => {
    dispatch(fetchTransacoes() as any);
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Transações</Text>
      {isLoading ? (
        <Text>Loading...</Text>
      ) : (
        <FlatList
          data={transacoes}
          keyExtractor={(item) => item.id.toString()}
          renderItem={({ item }) => (
            <View style={styles.item}>
              <Text>Transação {item.id}</Text>
            </View>
          )}
        />
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  item: {
    padding: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
  },
});

export default TransacaoScreen;
