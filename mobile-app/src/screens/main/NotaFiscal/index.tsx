import React, { useEffect } from 'react';
import { View, Text, FlatList } from 'react-native';
import { useNotaFiscalStore } from '../../../store/notaFiscalStore';
import ListItem from '../../../components/ListItem';
import Loading from '../../../components/Loading';
import { styles } from './styles';

const NotaFiscal = () => {
  const { notas, isLoading, fetchNotas } = useNotaFiscalStore();

  useEffect(() => {
    fetchNotas();
  }, []);

  if (isLoading) {
    return <Loading />;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Notas Fiscais</Text>
      <FlatList
        data={notas}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <ListItem
            title={`Nota ${item.id}`}
          />
        )}
      />
    </View>
  );
};

export default NotaFiscal;
