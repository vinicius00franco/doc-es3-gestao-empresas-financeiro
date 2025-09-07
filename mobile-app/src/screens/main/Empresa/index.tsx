import React, { useEffect } from 'react';
import { View, Text, FlatList } from 'react-native';
import { useEmpresaStore } from '../../../store/empresaStore';
import ListItem from '../../../components/ListItem';
import Loading from '../../../components/Loading';
import { styles } from './styles';

const Empresa = () => {
  const { empresas, isLoading, fetchEmpresas } = useEmpresaStore();

  useEffect(() => {
    fetchEmpresas();
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
