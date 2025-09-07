import { StyleSheet } from 'react-native';
import { theme } from '../../../utils/theme';

export const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: theme.spacing.lg,
    backgroundColor: theme.colors.surface,
  },
  title: {
    fontSize: theme.fonts.sizes.xlarge,
    fontWeight: theme.fonts.weights.bold,
    marginBottom: theme.spacing.lg,
    color: theme.colors.text,
  },
});
