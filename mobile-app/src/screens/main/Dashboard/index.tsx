import React, { useEffect } from 'react';
import { View, Text } from 'react-native';
import { useAuthStore } from '../../../store/authStore';
import Card from '../../../components/Card';
import { styles } from './styles';

const Dashboard = () => {
  const { user } = useAuthStore();

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
