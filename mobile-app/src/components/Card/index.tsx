import React from 'react';
import { View } from 'react-native';
import { styles } from './styles';

interface CardProps {
  children: any;
  style?: any;
}

const Card = ({ children, style }: CardProps) => {
  return (
    <View style={[styles.card, style]}>
      {children}
    </View>
  );
};

export default Card;
