import { StyleSheet } from 'react-native';
import { theme } from '../../utils/theme';

export const styles = StyleSheet.create({
  primaryButton: {
    backgroundColor: theme.colors.primary,
    padding: theme.spacing.md,
    borderRadius: theme.borderRadius.medium,
    alignItems: 'center',
    marginBottom: theme.spacing.sm,
  },
  secondaryButton: {
    backgroundColor: theme.colors.secondary,
    padding: theme.spacing.md,
    borderRadius: theme.borderRadius.medium,
    alignItems: 'center',
    marginBottom: theme.spacing.sm,
  },
  primaryText: {
    color: theme.colors.background,
    fontSize: theme.fonts.sizes.medium,
    fontWeight: theme.fonts.weights.bold,
  },
  secondaryText: {
    color: theme.colors.background,
    fontSize: theme.fonts.sizes.medium,
    fontWeight: theme.fonts.weights.bold,
  },
  disabled: {
    backgroundColor: theme.colors.border,
  },
  disabledText: {
    color: theme.colors.textSecondary,
  },
});
