export const theme = {
  colors: {
    primary: '#007bff',
    secondary: '#28a745',
    background: '#fff',
    surface: '#f8f9fa',
    text: '#333',
    textSecondary: '#666',
    error: '#dc3545',
    success: '#28a745',
    warning: '#ffc107',
    border: '#ccc',
    borderLight: '#eee',
  },
  fonts: {
    sizes: {
      small: 12,
      medium: 16,
      large: 20,
      xlarge: 24,
      xxlarge: 32,
    },
    weights: {
      regular: '400' as const,
      bold: 'bold' as const,
    },
    family: {
      regular: 'System',
      bold: 'System',
    },
  },
  spacing: {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
    xxl: 48,
  },
  borderRadius: {
    small: 4,
    medium: 8,
    large: 12,
    round: 50,
  },
  shadows: {
    light: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 1 },
      shadowOpacity: 0.1,
      shadowRadius: 2,
      elevation: 2,
    },
    medium: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.15,
      shadowRadius: 4,
      elevation: 4,
    },
  },
};
