import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import DashboardScreen from '../screens/main/DashboardScreen';
import EmpresaScreen from '../screens/main/EmpresaScreen';
import TransacaoScreen from '../screens/main/TransacaoScreen';
import AssinaturaScreen from '../screens/main/AssinaturaScreen';
import NotaFiscalScreen from '../screens/main/NotaFiscalScreen';

const Tab = createBottomTabNavigator();

const MainNavigator = () => {
  return (
    <Tab.Navigator>
      <Tab.Screen name="Dashboard" component={DashboardScreen} />
      <Tab.Screen name="Empresas" component={EmpresaScreen} />
      <Tab.Screen name="Transações" component={TransacaoScreen} />
      <Tab.Screen name="Assinaturas" component={AssinaturaScreen} />
      <Tab.Screen name="Notas Fiscais" component={NotaFiscalScreen} />
    </Tab.Navigator>
  );
};

export default MainNavigator;
