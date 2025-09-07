import { StyleSheet } from 'react-native';
import { theme } from '../../utils/theme';

export const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: theme.spacing.md,
  },
  text: {
    marginTop: theme.spacing.sm,
    fontSize: theme.fonts.sizes.medium,
    color: theme.colors.textSecondary,
  },
});
