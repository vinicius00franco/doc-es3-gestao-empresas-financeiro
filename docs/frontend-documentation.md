# Frontend Documentation - React Native

Documentação técnica do aplicativo mobile React Native para o sistema de gestão financeira.

## 📱 Visão Geral

O app mobile é desenvolvido em React Native com arquitetura MVC adaptada para mobile, integrado com o backend Django REST Framework.

## 🏗️ Arquitetura

### Padrão MVC Mobile

#### Model (Modelo)
- **Contexts**: Gerenciamento de estado global
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
│   │   ├── Forms/          # Componentes de formulário
│   │   └── Charts/         # Gráficos e visualizações
│   ├── screens/            # Telas da aplicação
│   │   ├── Auth/
│   │   ├── Dashboard/
│   │   ├── Transactions/
│   │   ├── Companies/
│   │   ├── Categories/
│   │   ├── Subscription/
│   │   └── Profile/
│   ├── navigation/         # Configuração de navegação
│   ├── services/          # Serviços de API
│   ├── contexts/          # Contextos React
│   ├── hooks/             # Hooks customizados
│   ├── utils/             # Funções utilitárias
│   ├── types/             # Tipos TypeScript
│   └── styles/            # Estilos globais
├── package.json
└── README.md
```

## 🔐 Autenticação

### AuthContext
```javascript
const AuthContext = createContext({
  user: null,
  tokens: null,
  subscription: null,
  login: async (email, password) => {},
  logout: async () => {},
  register: async (userData) => {},
  isAuthenticated: false,
  loading: false
});
```

### Fluxo de Autenticação
```javascript
// services/authService.js
export const authService = {
  login: async (email, senha) => {
    const response = await api.post('/auth/login/', { email, senha });
    const { access_token, refresh_token, user } = response.data;
    
    await secureStorage.setItem('tokens', { access_token, refresh_token });
    await secureStorage.setItem('user', user);
    
    return { user, tokens: { access_token, refresh_token } };
  },

  register: async (nome, email, senha) => {
    const response = await api.post('/auth/register/', { nome, email, senha });
    return response.data;
  },

  refreshToken: async () => {
    const tokens = await secureStorage.getItem('tokens');
    const response = await api.post('/auth/refresh/', {
      refresh_token: tokens.refresh_token
    });
    
    const newTokens = { ...tokens, access_token: response.data.access_token };
    await secureStorage.setItem('tokens', newTokens);
    
    return newTokens;
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
  loading: false
});
```

### Serviço de Empresas
```javascript
// services/companyService.js
export const companyService = {
  getAll: async () => {
    const response = await api.get('/empresas/');
    return response.data;
  },

  create: async (razao_social, nome_fantasia) => {
    const response = await api.post('/empresas/', {
      razao_social,
      nome_fantasia
    });
    return response.data;
  },

  update: async (id, data) => {
    const response = await api.put(`/empresas/${id}/`, data);
    return response.data;
  }
};
```

## 💰 Gestão de Transações

### Hook useTransactions
```javascript
// hooks/useTransactions.js
export const useTransactions = () => {
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({
    tipo: null,
    data_inicio: null,
    data_fim: null
  });

  const loadTransactions = useCallback(async () => {
    setLoading(true);
    try {
      const response = await transactionService.getAll(filters);
      setTransactions(response.data);
    } catch (error) {
      console.error('Erro ao carregar transações:', error);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  const createTransaction = async (transactionData) => {
    const response = await transactionService.create(transactionData);
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
    categoria_id: null
  });

  const { categories } = useCategories();

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
      
      <Picker
        label="Tipo"
        selectedValue={formData.tipo_transacao}
        onValueChange={(value) => setFormData(prev => ({
          ...prev,
          tipo_transacao: value
        }))}
      >
        <Picker.Item label="Entrada" value="entrada" />
        <Picker.Item label="Saída" value="saida" />
      </Picker>
      
      <CategoryPicker
        categories={categories}
        selectedValue={formData.categoria_id}
        onValueChange={(value) => setFormData(prev => ({
          ...prev,
          categoria_id: value
        }))}
      />
      
      <Button onPress={handleSubmit} title="Salvar" />
    </ScrollView>
  );
};
```

## 📊 Dashboard

### Componente Dashboard
```javascript
// screens/Dashboard/index.js
const Dashboard = () => {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const { subscription } = useAuth();

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const response = await dashboardService.getData();
      setDashboardData(response.data);
    } catch (error) {
      console.error('Erro ao carregar dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <ScrollView style={styles.container}>
      <SubscriptionBanner subscription={subscription} />
      <SummaryCards data={dashboardData.resumo} />
      <IncomeByCategory data={dashboardData.entradas_por_categoria} />
      <ExpenseByCategory data={dashboardData.saidas_por_categoria} />
    </ScrollView>
  );
};
```

### Cards de Resumo
```javascript
// components/SummaryCards.js
const SummaryCards = ({ data }) => {
  return (
    <View style={styles.container}>
      <Card style={[styles.card, styles.incomeCard]}>
        <Text style={styles.cardTitle}>Entradas</Text>
        <Text style={styles.cardValue}>
          {formatCurrency(data.total_entradas)}
        </Text>
      </Card>
      
      <Card style={[styles.card, styles.expenseCard]}>
        <Text style={styles.cardTitle}>Saídas</Text>
        <Text style={styles.cardValue}>
          {formatCurrency(data.total_saidas)}
        </Text>
      </Card>
      
      <Card style={[styles.card, styles.balanceCard]}>
        <Text style={styles.cardTitle}>Saldo</Text>
        <Text style={[
          styles.cardValue,
          parseFloat(data.saldo) >= 0 ? styles.positive : styles.negative
        ]}>
          {formatCurrency(data.saldo)}
        </Text>
      </Card>
    </View>
  );
};
```

## 💳 Sistema de Assinaturas

### SubscriptionContext
```javascript
const SubscriptionContext = createContext({
  plans: [],
  currentSubscription: null,
  upgradePlan: async (planId) => {},
  checkLimits: () => {},
  loading: false
});
```

### Serviço de Assinaturas
```javascript
// services/subscriptionService.js
export const subscriptionService = {
  getPlans: async () => {
    const response = await api.get('/planos/');
    return response.data;
  },

  getCurrentSubscription: async () => {
    const response = await api.get('/assinaturas/atual/');
    return response.data;
  },

  upgrade: async (planId) => {
    const response = await api.post('/assinaturas/upgrade/', {
      plano_id: planId
    });
    return response.data;
  }
};
```

### Tela de Planos
```javascript
// screens/Subscription/PlansScreen.js
const PlansScreen = () => {
  const [plans, setPlans] = useState([]);
  const { currentSubscription } = useSubscription();

  useEffect(() => {
    loadPlans();
  }, []);

  const loadPlans = async () => {
    try {
      const response = await subscriptionService.getPlans();
      setPlans(response);
    } catch (error) {
      console.error('Erro ao carregar planos:', error);
    }
  };

  const handleUpgrade = async (planId) => {
    try {
      const response = await subscriptionService.upgrade(planId);
      // Abrir WebView com URL de pagamento
      openPaymentWebView(response.payment_url);
    } catch (error) {
      Alert.alert('Erro', 'Não foi possível processar o upgrade');
    }
  };

  return (
    <ScrollView style={styles.container}>
      {plans.map(plan => (
        <PlanCard
          key={plan.id}
          plan={plan}
          isActive={currentSubscription?.plano.id === plan.id}
          onUpgrade={() => handleUpgrade(plan.id)}
        />
      ))}
    </ScrollView>
  );
};
```

### Verificação de Limites
```javascript
// hooks/useSubscriptionLimits.js
export const useSubscriptionLimits = () => {
  const { currentSubscription } = useSubscription();
  const { transactions } = useTransactions();

  const checkTransactionLimit = () => {
    if (!currentSubscription?.plano.limite_transacoes) {
      return { canCreate: true, remaining: null };
    }

    const currentMonth = new Date().getMonth();
    const currentYear = new Date().getFullYear();
    
    const monthlyTransactions = transactions.filter(t => {
      const transactionDate = new Date(t.criado_em);
      return transactionDate.getMonth() === currentMonth && 
             transactionDate.getFullYear() === currentYear;
    });

    const used = monthlyTransactions.length;
    const limit = currentSubscription.plano.limite_transacoes;
    const remaining = limit - used;

    return {
      canCreate: remaining > 0,
      remaining,
      limit,
      used
    };
  };

  return { checkTransactionLimit };
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

### Tab Navigator com Verificação de Permissões
```javascript
// navigation/TabNavigator.js
const MainTabNavigator = () => {
  const { currentSubscription } = useSubscription();

  return (
    <Tab.Navigator>
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
        name="Companies" 
        component={CompaniesScreen}
        options={{ title: 'Empresas' }}
      />
      {currentSubscription?.plano.permite_relatorios && (
        <Tab.Screen 
          name="Reports" 
          component={ReportsScreen}
          options={{ title: 'Relatórios' }}
        />
      )}
      <Tab.Screen 
        name="Subscription" 
        component={SubscriptionScreen}
        options={{ title: 'Planos' }}
      />
    </Tab.Navigator>
  );
};
```

## 🎯 Componentes Reutilizáveis

### Button com Estados
```javascript
// components/UI/Button/index.js
const Button = ({ 
  title, 
  onPress, 
  variant = 'primary', 
  disabled = false,
  loading = false,
  ...props 
}) => {
  const buttonStyle = [
    styles.button,
    styles[variant],
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
        <ActivityIndicator color="#fff" />
      ) : (
        <Text style={[styles.text, styles[`${variant}Text`]]}>
          {title}
        </Text>
      )}
    </TouchableOpacity>
  );
};
```

### Input com Validação
```javascript
// components/UI/Input/index.js
const Input = ({ 
  label,
  value,
  onChangeText,
  placeholder,
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
export const formatCurrency = (value) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value);
};

export const formatDate = (date) => {
  return new Date(date).toLocaleDateString('pt-BR');
};
```

### Validadores
```javascript
// utils/validators.js
export const validateEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
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

## 🚀 Configuração de Ambiente

### API Configuration
```javascript
// config/api.js
import axios from 'axios';
import { secureStorage } from '../utils/storage';

const API_BASE_URL = __DEV__ 
  ? 'http://localhost:8000/api/v1'
  : 'https://api.gestaofinanceira.com/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Interceptor para adicionar token
api.interceptors.request.use(async (config) => {
  const tokens = await secureStorage.getItem('tokens');
  if (tokens?.access_token) {
    config.headers.Authorization = `Bearer ${tokens.access_token}`;
  }
  return config;
});

// Interceptor para refresh token
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      try {
        const newTokens = await authService.refreshToken();
        error.config.headers.Authorization = `Bearer ${newTokens.access_token}`;
        return api.request(error.config);
      } catch (refreshError) {
        // Redirect to login
        await authService.logout();
      }
    }
    return Promise.reject(error);
  }
);

export default api;
```

### Armazenamento Seguro
```javascript
// utils/storage.js
import AsyncStorage from '@react-native-async-storage/async-storage';

export const secureStorage = {
  setItem: async (key, value) => {
    try {
      await AsyncStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error('Erro ao salvar no storage:', error);
    }
  },
  
  getItem: async (key) => {
    try {
      const value = await AsyncStorage.getItem(key);
      return value ? JSON.parse(value) : null;
    } catch (error) {
      console.error('Erro ao ler do storage:', error);
      return null;
    }
  },

  removeItem: async (key) => {
    try {
      await AsyncStorage.removeItem(key);
    } catch (error) {
      console.error('Erro ao remover do storage:', error);
    }
  }
};
```