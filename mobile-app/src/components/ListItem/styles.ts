import { StyleSheet } from 'react-native';
import { theme } from '../../utils/theme';

export const styles = StyleSheet.create({
  item: {
    padding: theme.spacing.md,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.borderLight,
    backgroundColor: theme.colors.background,
  },
  title: {
    fontSize: theme.fonts.sizes.medium,
    fontWeight: theme.fonts.weights.bold,
    color: theme.colors.text,
  },
  subtitle: {
    fontSize: theme.fonts.sizes.small,
    color: theme.colors.textSecondary,
    marginTop: theme.spacing.xs,
  },
});
