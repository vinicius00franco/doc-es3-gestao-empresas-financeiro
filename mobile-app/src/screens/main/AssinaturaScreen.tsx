import React, { useEffect } from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { fetchPlanos } from '../../store/slices/assinaturaSlice';
import { RootState } from '../../store';

const AssinaturaScreen = () => {
  const dispatch = useDispatch();
  const { planos, isLoading } = useSelector((state: RootState) => (state as any).assinatura);

  useEffect(() => {
    dispatch(fetchPlanos() as any);
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Assinaturas</Text>
      {isLoading ? (
        <Text>Loading...</Text>
      ) : (
        <FlatList
          data={planos}
          keyExtractor={(item) => item.id.toString()}
          renderItem={({ item }) => (
            <View style={styles.item}>
              <Text>{item.nome}</Text>
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

export default AssinaturaScreen;
