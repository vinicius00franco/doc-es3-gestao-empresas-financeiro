import React from 'react';
import { TouchableOpacity, Text, View } from 'react-native';
import { styles } from './styles';

interface ListItemProps {
  title: string;
  subtitle?: string;
  onPress?: () => void;
}

const ListItem = ({ title, subtitle, onPress }: ListItemProps) => {
  const Container = onPress ? TouchableOpacity : View;

  return (
    <Container style={styles.item} onPress={onPress}>
      <Text style={styles.title}>{title}</Text>
      {subtitle && <Text style={styles.subtitle}>{subtitle}</Text>}
    </Container>
  );
};

export default ListItem;
