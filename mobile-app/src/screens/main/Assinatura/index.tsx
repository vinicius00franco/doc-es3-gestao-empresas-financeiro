import React, { useEffect } from 'react';
import { View, Text, FlatList } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { fetchPlanos } from '../../../store/slices/assinaturaSlice';
import { RootState } from '../../../store';
import ListItem from '../../../components/ListItem';
import Loading from '../../../components/Loading';
import { styles } from './styles';

const Assinatura = () => {
  const dispatch = useDispatch();
  const { planos, isLoading } = useSelector((state: RootState) => (state as any).assinatura);

  useEffect(() => {
    dispatch(fetchPlanos() as any);
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
