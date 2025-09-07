import React, { useEffect } from 'react';
import { View, Text, FlatList } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { fetchNotas } from '../../../store/slices/notaFiscalSlice';
import { RootState } from '../../../store';
import ListItem from '../../../components/ListItem';
import Loading from '../../../components/Loading';
import { styles } from './styles';

const NotaFiscal = () => {
  const dispatch = useDispatch();
  const { notas, isLoading } = useSelector((state: RootState) => (state as any).notaFiscal);

  useEffect(() => {
    dispatch(fetchNotas() as any);
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
