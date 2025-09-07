import React, { useEffect } from 'react';
import { View, Text } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../../../store';
import Card from '../../../components/Card';
import { styles } from './styles';

const Dashboard = () => {
  const dispatch = useDispatch();
  const { user } = useSelector((state: RootState) => (state as any).auth);

  useEffect(() => {
    // Fetch dashboard data if needed
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Dashboard</Text>
      <Card>
        <Text>Bem-vindo, {user?.nome}</Text>
      </Card>
      {/* Add more dashboard content */}
    </View>
  );
};

export default Dashboard;
