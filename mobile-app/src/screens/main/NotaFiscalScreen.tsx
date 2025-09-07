import React, { useEffect } from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { fetchNotas } from '../../store/slices/notaFiscalSlice';
import { RootState } from '../../store';

const NotaFiscalScreen = () => {
  const dispatch = useDispatch();
  const { notas, isLoading } = useSelector((state: RootState) => (state as any).notaFiscal);

  useEffect(() => {
    dispatch(fetchNotas() as any);
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Notas Fiscais</Text>
      {isLoading ? (
        <Text>Loading...</Text>
      ) : (
        <FlatList
          data={notas}
          keyExtractor={(item) => item.id.toString()}
          renderItem={({ item }) => (
            <View style={styles.item}>
              <Text>Nota {item.id}</Text>
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

export default NotaFiscalScreen;
