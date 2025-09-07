import React, { useEffect } from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { fetchEmpresas } from '../../store/slices/empresaSlice';
import { RootState } from '../../store';

const EmpresaScreen = () => {
  const dispatch = useDispatch();
  const { empresas, isLoading } = useSelector((state: RootState) => (state as any).empresa);

  useEffect(() => {
    dispatch(fetchEmpresas() as any);
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Empresas</Text>
      {isLoading ? (
        <Text>Loading...</Text>
      ) : (
        <FlatList
          data={empresas}
          keyExtractor={(item) => item.id.toString()}
          renderItem={({ item }) => (
            <View style={styles.item}>
              <Text>{item.razao_social}</Text>
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

export default EmpresaScreen;
