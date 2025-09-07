import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Dashboard from '../screens/main/Dashboard';
import Empresa from '../screens/main/Empresa';
import Transacao from '../screens/main/Transacao';
import Assinatura from '../screens/main/Assinatura';
import NotaFiscal from '../screens/main/NotaFiscal';

const Tab = createBottomTabNavigator();

const MainNavigator = () => {
  return (
    <Tab.Navigator>
      <Tab.Screen name="Dashboard" component={Dashboard} />
      <Tab.Screen name="Empresas" component={Empresa} />
      <Tab.Screen name="Transações" component={Transacao} />
      <Tab.Screen name="Assinaturas" component={Assinatura} />
      <Tab.Screen name="Notas Fiscais" component={NotaFiscal} />
    </Tab.Navigator>
  );
};

export default MainNavigator;
