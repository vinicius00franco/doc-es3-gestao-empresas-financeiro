import React, { useEffect } from 'react';
import { View, Text, FlatList } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { fetchEmpresas } from '../../../store/slices/empresaSlice';
import { RootState } from '../../../store';
import ListItem from '../../../components/ListItem';
import Loading from '../../../components/Loading';
import { styles } from './styles';

const Empresa = () => {
  const dispatch = useDispatch();
  const { empresas, isLoading } = useSelector((state: RootState) => (state as any).empresa);

  useEffect(() => {
    dispatch(fetchEmpresas() as any);
  }, []);

  if (isLoading) {
    return <Loading />;
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Empresas</Text>
      <FlatList
        data={empresas}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <ListItem
            title={item.razao_social}
            subtitle={item.cnpj}
          />
        )}
      />
    </View>
  );
};

export default Empresa;
