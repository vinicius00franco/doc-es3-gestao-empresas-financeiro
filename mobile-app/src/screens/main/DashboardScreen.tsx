import React, { useEffect } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../../store';

const DashboardScreen = () => {
  const dispatch = useDispatch();
  const { user } = useSelector((state: RootState) => (state as any).auth);

  useEffect(() => {
    // Fetch dashboard data if needed
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Dashboard</Text>
      <Text>Bem-vindo, {user?.nome}</Text>
      {/* Add dashboard content */}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
});

export default DashboardScreen;
