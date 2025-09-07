import { StyleSheet } from 'react-native';
import { theme } from '../../../utils/theme';

export const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: theme.spacing.lg,
    backgroundColor: theme.colors.background,
  },
  title: {
    fontSize: theme.fonts.sizes.xlarge,
    fontWeight: theme.fonts.weights.bold,
    textAlign: 'center',
    marginBottom: theme.spacing.lg,
    color: theme.colors.text,
  },
  error: {
    color: theme.colors.error,
    textAlign: 'center',
    marginTop: theme.spacing.sm,
  },
});
