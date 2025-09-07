import React from 'react';
import { TouchableOpacity, Text } from 'react-native';
import { styles } from './styles';

interface ButtonProps {
  title: string;
  onPress: () => void;
  disabled?: boolean;
  variant?: 'primary' | 'secondary';
}

const Button = ({ title, onPress, disabled = false, variant = 'primary' }: ButtonProps) => {
  const buttonStyle = variant === 'primary' ? styles.primaryButton : styles.secondaryButton;
  const textStyle = variant === 'primary' ? styles.primaryText : styles.secondaryText;

  return (
    <TouchableOpacity
      style={[buttonStyle, disabled && styles.disabled]}
      onPress={onPress}
      disabled={disabled}
    >
      <Text style={[textStyle, disabled && styles.disabledText]}>{title}</Text>
    </TouchableOpacity>
  );
};

export default Button;
