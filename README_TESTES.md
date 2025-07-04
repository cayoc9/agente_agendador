# Testes do Módulo ClickUp

Este documento explica como configurar e executar os testes do módulo ClickUp.

## Estrutura de Testes

```
tests/
├── __init__.py
├── test_clickup_client.py      # Testes do cliente HTTP
├── test_clickup_models.py      # Testes dos modelos de dados
├── test_clickup_crm_service.py # Testes do serviço CRM
└── test_integration.py         # Testes de integração
```

## Configuração

### 1. Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```bash
# Copie o arquivo de exemplo
cp env.example .env

# Edite o arquivo .env com seus dados reais
CLICKUP_API_TOKEN=seu_token_real_aqui
CLICKUP_SPACE_ID=seu_space_id_real_aqui
CLICKUP_FOLDER_ID=seu_folder_id_real_aqui  # Opcional
CLICKUP_CRM_LIST_NAME=CRM Clientes
```

### 2. Como obter os dados do ClickUp

1. **API Token**: 
   - Acesse https://app.clickup.com/settings/tokens
   - Clique em "Generate Token"
   - Copie o token gerado

2. **Space ID**:
   - Abra o ClickUp no navegador
   - Vá para o espaço desejado
   - O ID está na URL: `https://app.clickup.com/[workspace_id]/v/li/[space_id]`

3. **Folder ID** (opcional):
   - Se quiser criar a lista dentro de uma pasta específica
   - O ID está na URL da pasta

## Executando os Testes

### Executar todos os testes

```bash
python run_tests.py
```

### Executar teste específico

```bash
python run_tests.py test_clickup_client
python run_tests.py test_clickup_models
python run_tests.py test_clickup_crm_service
python run_tests.py test_integration
```

### Executar com unittest diretamente

```bash
# Teste específico
python -m unittest tests.test_clickup_client

# Todos os testes
python -m unittest discover tests
```

## Tipos de Teste

### 1. Testes Unitários
- **test_clickup_client.py**: Testa o cliente HTTP
- **test_clickup_models.py**: Testa os modelos de dados
- **test_clickup_crm_service.py**: Testa as funções do serviço CRM

### 2. Testes de Integração
- **test_integration.py**: Testa o fluxo completo do CRM

## Mocks e Simulação

Os testes usam mocks para simular as respostas da API do ClickUp, evitando:
- Chamadas reais à API durante os testes
- Dependência de conexão com internet
- Consumo desnecessário de rate limits

## Exemplo de Uso

```python
from src.clickup_models import Cliente
from src.clickup_crm_service import seed_crm_list, criar_task_cliente

# Criar cliente
cliente = Cliente(
    nome="João Silva",
    email="joao@email.com",
    tipo_servico="Desenvolvimento Web"
)

# Criar lista CRM e task
list_id = seed_crm_list()
task = criar_task_cliente(list_id, cliente)
```

## Troubleshooting

### Erro de importação
Se houver erro ao importar módulos, verifique se:
- O arquivo `.env` está configurado corretamente
- As dependências estão instaladas (`pip install -r requirements.txt`)

### Testes falhando
- Verifique se os mocks estão configurados corretamente
- Confirme se as variáveis de ambiente estão definidas
- Verifique se a estrutura de diretórios está correta

## Próximos Passos

1. Configure o arquivo `.env` com seus dados reais
2. Execute os testes para verificar se tudo está funcionando
3. Integre o módulo ClickUp ao fluxo do bot
4. Teste com dados reais da API do ClickUp 