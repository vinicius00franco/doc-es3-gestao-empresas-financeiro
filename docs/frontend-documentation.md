# Frontend Documentation - React Native

Documentação técnica do aplicativo mobile React Native para o sistema de gestão financeira.

## 📱 Visão Geral

O app mobile é desenvolvido em React Native com arquitetura MVC adaptada para mobile, proporcionando uma experiência nativa tanto para iOS quanto Android.

## 🏗️ Arquitetura

### Padrão MVC Mobile

#### Model (Modelo)
- **Contexts**: Gerenciamento de estado global
- **Reducers**: Lógica de estado complexa
- **AsyncStorage**: Persistência local
- **Types**: Interfaces TypeScript

#### View (Visão)
- **Screens**: Telas principais da aplicação
- **Components**: Componentes reutilizáveis
- **Navigation**: Estrutura de navegação

#### Controller (Controlador)
- **Services**: Comunicação com APIs
- **Hooks**: Lógica de negócio customizada
- **Utils**: Funções auxiliares

## 📁 Estrutura de Pastas

```
mobile_app/
├── src/
│   ├── components/          # Componentes reutilizáveis
│   │   ├── UI/             # Componentes básicos de UI
│   │   │   ├── Button/
│   │   │   ├── Input/
│   │   │   ├── Card/
│   │   │   └── Modal/
│   │   ├── Forms/          # Componentes de formulário
│   │   │   ├── TransactionForm/
│   │   │   ├── CompanyForm/
│   │   │   └── LoginForm/
│   │   └── Charts/         # Gráficos e visualizações
│   │       ├── PieChart/
│   │       ├── LineChart/
│   │       └── BarChart/
│   ├── screens/            # Telas da aplicação
│   │   ├── Auth/
│   │   │   ├── Login/
│   │   │   ├── Register/
│   │   │   └── ForgotPassword/
│   │   ├── Dashboard/
│   │   ├── Transactions/
│   │   │   ├── List/
│   │   │   ├── Create/
│   │   │   └── Edit/
│   │   ├── Companies/
│   │   ├── Categories/
│   │   ├── Reports/
│   │   ├── Subscription/
│   │   └── Profile/
│   ├── navigation/         # Configuração de navegação
│   │   ├── AppNavigator.js
│   │   ├── AuthNavigator.js
│   │   └── TabNavigator.js
│   ├── services/          # Serviços de API
│   │   ├── api.js         # Cliente HTTP base
│   │   ├── authService.js
│   │   ├── transactionService.js
│   │   ├── companyService.js
│   │   └── reportService.js
│   ├── contexts/          # Contextos React
│   │   ├── AuthContext.js
│   │   ├── CompanyContext.js
│   │   └── ThemeContext.js
│   ├── hooks/             # Hooks customizados
│   │   ├── useAuth.js
│   │   ├── useCompany.js
│   │   ├── useTransactions.js
│   │   └── useDebounce.js
│   ├── utils/             # Funções utilitárias
│   │   ├── formatters.js  # Formatação de dados
│   │   ├── validators.js  # Validações
│   │   ├── constants.js   # Constantes
│   │   └── storage.js     # AsyncStorage helpers
│   ├── types/             # Tipos TypeScript
│   │   ├── auth.ts
│   │   ├── transaction.ts
│   │   └── company.ts
│   ├── assets/            # Recursos estáticos
│   │   ├── images/
│   │   ├── icons/
│   │   └── fonts/
│   └── styles/            # Estilos globais
│       ├── theme.js
│       ├── colors.js
│       └── typography.js
├── android/               # Configurações Android
├── ios/                   # Configurações iOS
├── package.json
└── README.md
```

## 🎨 Design System

### Cores Principais
```javascript
const colors = {
  primary: '#2196F3',
  secondary: '#4CAF50',
  accent: '#FF9800',
  success: '#4CAF50',
  warning: '#FF9800',
  error: '#F44336',
  text: {
    primary: '#212121',
    secondary: '#757575',
    disabled: '#BDBDBD'
  },
  background: {
    default: '#FAFAFA',
    paper: '#FFFFFF',
    dark: '#121212'
  },
  divider: '#E0E0E0'
};
```

### Tipografia
```javascript
const typography = {
  h1: { fontSize: 32, fontWeight: 'bold' },
  h2: { fontSize: 28, fontWeight: 'bold' },
  h3: { fontSize: 24, fontWeight: '600' },
  h4: { fontSize: 20, fontWeight: '600' },
  body1: { fontSize: 16, fontWeight: 'normal' },
  body2: { fontSize: 14, fontWeight: 'normal' },
  caption: { fontSize: 12, fontWeight: 'normal' },
  button: { fontSize: 16, fontWeight: '600', textTransform: 'uppercase' }
};
```

### Espaçamento
```javascript
const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48
};
```

## 🔐 Autenticação

### AuthContext
```javascript
const AuthContext = createContext({
  user: null,
  tokens: null,
  login: async (email, password) => {},
  logout: async () => {},
  register: async (userData) => {},
  isAuthenticated: false,
  loading: false
});
```

### Fluxo de Autenticação
1. Usuário insere credenciais
2. App envia para API
3. API retorna JWT tokens
4. Tokens são armazenados de forma segura
5. User é redirecionado para tela principal
6. Refresh automático dos tokens

### Armazenamento Seguro
```javascript
// utils/storage.js
import AsyncStorage from '@react-native-async-storage/async-storage';
import { encrypt, decrypt } from './encryption';

export const secureStorage = {
  setItem: async (key, value) => {
    const encrypted = encrypt(JSON.stringify(value));
    await AsyncStorage.setItem(key, encrypted);
  },
  
  getItem: async (key) => {
    const encrypted = await AsyncStorage.getItem(key);
    if (encrypted) {
      return JSON.parse(decrypt(encrypted));
    }
    return null;
  }
};
```

## 🏢 Gestão de Empresas

### CompanyContext
```javascript
const CompanyContext = createContext({
  companies: [],
  activeCompany: null,
  setActiveCompany: (company) => {},
  createCompany: async (companyData) => {},
  updateCompany: async (id, data) => {},
  deleteCompany: async (id) => {},
  loading: false
});
```

### Componente de Seleção
```javascript
// components/CompanySelector.js
const CompanySelector = () => {
  const { companies, activeCompany, setActiveCompany } = useCompany();
  
  return (
    <Picker
      selectedValue={activeCompany?.id}
      onValueChange={(value) => {
        const company = companies.find(c => c.id === value);
        setActiveCompany(company);
      }}
    >
      {companies.map(company => (
        <Picker.Item 
          key={company.id} 
          label={company.nome_fantasia || company.razao_social}
          value={company.id} 
        />
      ))}
    </Picker>
  );
};
```

## 💰 Gestão de Transações

### Hook useTransactions
```javascript
// hooks/useTransactions.js
export const useTransactions = (companyId) => {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({
    tipo: null,
    categoria_id: null,
    data_inicio: null,
    data_fim: null
  });

  const loadTransactions = useCallback(async () => {
    setLoading(true);
    try {
      const response = await transactionService.getAll({
        empresa_id: companyId,
        ...filters
      });
      setTransactions(response.data.results);
    } catch (error) {
      // Handle error
    } finally {
      setLoading(false);
    }
  }, [companyId, filters]);

  const createTransaction = async (transactionData) => {
    const response = await transactionService.create({
      ...transactionData,
      empresa_id: companyId
    });
    setTransactions(prev => [response.data, ...prev]);
    return response.data;
  };

  return {
    transactions,
    loading,
    filters,
    setFilters,
    loadTransactions,
    createTransaction
  };
};
```

### Formulário de Transação
```javascript
// components/Forms/TransactionForm.js
const TransactionForm = ({ onSubmit, initialData }) => {
  const [formData, setFormData] = useState({
    descricao: '',
    valor: '',
    data_transacao: new Date(),
    tipo_transacao: 'entrada',
    categoria_id: null,
    forma_pagamento: 'dinheiro',
    observacoes: ''
  });

  const handleSubmit = () => {
    const validatedData = validateTransaction(formData);
    if (validatedData.isValid) {
      onSubmit(formData);
    } else {
      showValidationErrors(validatedData.errors);
    }
  };

  return (
    <ScrollView style={styles.form}>
      <Input
        label="Descrição"
        value={formData.descricao}
        onChangeText={(text) => setFormData(prev => ({
          ...prev,
          descricao: text
        }))}
        required
      />
      
      <CurrencyInput
        label="Valor"
        value={formData.valor}
        onChangeValue={(value) => setFormData(prev => ({
          ...prev,
          valor: value
        }))}
        required
      />
      
      <DatePicker
        label="Data da Transação"
        value={formData.data_transacao}
        onChange={(date) => setFormData(prev => ({
          ...prev,
          data_transacao: date
        }))}
      />
      
      <Button onPress={handleSubmit} title="Salvar" />
    </ScrollView>
  );
};
```

## 📊 Relatórios e Dashboard

### Componente Dashboard
```javascript
// screens/Dashboard/index.js
const Dashboard = () => {
  const { activeCompany } = useCompany();
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, [activeCompany]);

  const loadDashboardData = async () => {
    try {
      const response = await reportService.getDashboard({
        empresa_id: activeCompany.id,
        periodo: '30d'
      });
      setDashboardData(response.data);
    } catch (error) {
      // Handle error
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <ScrollView style={styles.container}>
      <SummaryCards data={dashboardData.resumo} />
      <IncomeByCategory data={dashboardData.entradas_por_categoria} />
      <ExpenseByCategory data={dashboardData.saidas_por_categoria} />
      <CashFlowChart data={dashboardData.fluxo_diario} />
    </ScrollView>
  );
};
```

### Gráfico de Pizza
```javascript
// components/Charts/PieChart.js
import { PieChart } from 'react-native-chart-kit';

const CategoryPieChart = ({ data, title }) => {
  const chartData = data.map((item, index) => ({
    name: item.categoria,
    population: parseFloat(item.valor),
    color: CHART_COLORS[index % CHART_COLORS.length],
    legendFontColor: colors.text.primary,
    legendFontSize: 12
  }));

  return (
    <Card style={styles.chartCard}>
      <Text style={styles.chartTitle}>{title}</Text>
      <PieChart
        data={chartData}
        width={screenWidth - 32}
        height={220}
        chartConfig={{
          color: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`
        }}
        accessor="population"
        backgroundColor="transparent"
        paddingLeft="15"
        absolute
      />
    </Card>
  );
};
```

## 🔄 Navegação

### Stack Navigator Principal
```javascript
// navigation/AppNavigator.js
const AppNavigator = () => {
  const { isAuthenticated } = useAuth();

  return (
    <NavigationContainer>
      {isAuthenticated ? (
        <MainTabNavigator />
      ) : (
        <AuthStackNavigator />
      )}
    </NavigationContainer>
  );
};
```

### Tab Navigator
```javascript
// navigation/TabNavigator.js
const Tab = createBottomTabNavigator();

const MainTabNavigator = () => (
  <Tab.Navigator
    screenOptions={({ route }) => ({
      tabBarIcon: ({ focused, color, size }) => {
        const iconName = getTabIconName(route.name, focused);
        return <Ionicons name={iconName} size={size} color={color} />;
      },
    })}
  >
    <Tab.Screen 
      name="Dashboard" 
      component={DashboardScreen}
      options={{ title: 'Início' }}
    />
    <Tab.Screen 
      name="Transactions" 
      component={TransactionsNavigator}
      options={{ title: 'Transações' }}
    />
    <Tab.Screen 
      name="Reports" 
      component={ReportsScreen}
      options={{ title: 'Relatórios' }}
    />
    <Tab.Screen 
      name="Profile" 
      component={ProfileScreen}
      options={{ title: 'Perfil' }}
    />
  </Tab.Navigator>
);
```

## 🎯 Componentes Reutilizáveis

### Button Component
```javascript
// components/UI/Button/index.js
const Button = ({ 
  title, 
  onPress, 
  variant = 'primary', 
  size = 'medium',
  disabled = false,
  loading = false,
  icon,
  ...props 
}) => {
  const buttonStyle = [
    styles.button,
    styles[variant],
    styles[size],
    disabled && styles.disabled
  ];

  return (
    <TouchableOpacity
      style={buttonStyle}
      onPress={onPress}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? (
        <ActivityIndicator color={colors.background.paper} />
      ) : (
        <View style={styles.content}>
          {icon && <Icon name={icon} style={styles.icon} />}
          <Text style={[styles.text, styles[`${variant}Text`]]}>
            {title}
          </Text>
        </View>
      )}
    </TouchableOpacity>
  );
};
```

### Input Component
```javascript
// components/UI/Input/index.js
const Input = ({ 
  label,
  value,
  onChangeText,
  placeholder,
  secureTextEntry = false,
  keyboardType = 'default',
  required = false,
  error,
  ...props 
}) => {
  return (
    <View style={styles.container}>
      {label && (
        <Text style={styles.label}>
          {label}
          {required && <Text style={styles.required}> *</Text>}
        </Text>
      )}
      <TextInput
        style={[styles.input, error && styles.inputError]}
        value={value}
        onChangeText={onChangeText}
        placeholder={placeholder}
        secureTextEntry={secureTextEntry}
        keyboardType={keyboardType}
        {...props}
      />
      {error && <Text style={styles.errorText}>{error}</Text>}
    </View>
  );
};
```

## 🔧 Utilitários

### Formatadores
```javascript
// utils/formatters.js
export const formatCurrency = (value, currency = 'BRL') => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: currency
  }).format(value);
};

export const formatDate = (date, format = 'DD/MM/YYYY') => {
  return moment(date).format(format);
};

export const formatCNPJ = (cnpj) => {
  return cnpj.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
};
```

### Validadores
```javascript
// utils/validators.js
export const validateEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

export const validateCNPJ = (cnpj) => {
  // Implementação completa da validação de CNPJ
  const cleanCNPJ = cnpj.replace(/\D/g, '');
  return cleanCNPJ.length === 14 && isValidCNPJChecksum(cleanCNPJ);
};

export const validateTransaction = (transaction) => {
  const errors = {};
  
  if (!transaction.descricao?.trim()) {
    errors.descricao = 'Descrição é obrigatória';
  }
  
  if (!transaction.valor || parseFloat(transaction.valor) <= 0) {
    errors.valor = 'Valor deve ser maior que zero';
  }
  
  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
};
```

## 📲 Notificações Push

### Configuração
```javascript
// services/notificationService.js
import PushNotification from 'react-native-push-notification';

export const notificationService = {
  configure: () => {
    PushNotification.configure({
      onRegister: function(token) {
        // Enviar token para o backend
        authService.updatePushToken(token.token);
      },
      
      onNotification: function(notification) {
        // Lidar com notificação recebida
        handleNotification(notification);
      },
    });
  },
  
  showLocal: (title, message) => {
    PushNotification.localNotification({
      title,
      message,
    });
  }
};
```

## 🧪 Testes

### Estrutura de Testes
```
__tests__/
├── components/
│   ├── Button.test.js
│   └── Input.test.js
├── screens/
│   ├── Dashboard.test.js
│   └── Login.test.js
├── services/
│   ├── authService.test.js
│   └── transactionService.test.js
└── utils/
    ├── formatters.test.js
    └── validators.test.js
```

### Exemplo de Teste
```javascript
// __tests__/components/Button.test.js
import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import Button from '../src/components/UI/Button';

describe('Button Component', () => {
  it('renders correctly', () => {
    const { getByText } = render(
      <Button title="Test Button" onPress={() => {}} />
    );
    expect(getByText('Test Button')).toBeTruthy();
  });

  it('calls onPress when pressed', () => {
    const mockOnPress = jest.fn();
    const { getByText } = render(
      <Button title="Test Button" onPress={mockOnPress} />
    );
    
    fireEvent.press(getByText('Test Button'));
    expect(mockOnPress).toHaveBeenCalledTimes(1);
  });
});
```

## 🚀 Build e Deploy

### Scripts Package.json
```json
{
  "scripts": {
    "start": "react-native start",
    "android": "react-native run-android",
    "ios": "react-native run-ios",
    "test": "jest",
    "lint": "eslint . --ext .js,.jsx,.ts,.tsx",
    "build:android": "cd android && ./gradlew assembleRelease",
    "build:ios": "xcodebuild -workspace ios/GestaoFinanceira.xcworkspace -scheme GestaoFinanceira -configuration Release"
  }
}
```

### Configuração de Ambiente
```javascript
// config/env.js
const configs = {
  development: {
    API_URL: 'http://localhost:8000/api/v1',
    DEBUG: true
  },
  production: {
    API_URL: 'https://api.gestaofinanceira.com/v1',
    DEBUG: false
  }
};

export default configs[process.env.NODE_ENV || 'development'];
```
