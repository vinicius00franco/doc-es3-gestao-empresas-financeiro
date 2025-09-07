import React, { useEffect } from 'react';
import { View, Text, FlatList } from 'react-native';
import { useAssinaturaStore } from '../../../store/assinaturaStore';
import ListItem from '../../../components/ListItem';
import Loading from '../../../components/Loading';
import { styles } from './styles';

const Assinatura = () => {
  const { planos, isLoading, fetchPlanos } = useAssinaturaStore();

  useEffect(() => {
    fetchPlanos();
  }, []);

  if (isLoading) {
    return <Loading />;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Assinaturas</Text>
      <FlatList
        data={planos}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <ListItem
            title={item.nome}
          />
        )}
      />
    </View>
  );
};

export default Assinatura;
