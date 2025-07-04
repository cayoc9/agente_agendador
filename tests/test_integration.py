import unittest
from unittest.mock import patch, Mock
import os
from src.clickup_models import Cliente
from src.clickup_crm_service import (
    seed_crm_list,
    buscar_opcoes_servico,
    criar_task_cliente
)

class TestClickUpIntegration(unittest.TestCase):
    """Teste de integração do fluxo completo do CRM"""
    
    def setUp(self):
        # Configura variáveis de ambiente para teste
        os.environ['CLICKUP_API_TOKEN'] = 'test_token'
        os.environ['CLICKUP_SPACE_ID'] = 'test_space'
        os.environ['CLICKUP_CRM_LIST_NAME'] = 'CRM Teste'
        
        self.cliente_teste = Cliente(
            nome="João Silva",
            email="joao@teste.com",
            tipo_servico="Desenvolvimento Web"
        )

    @patch('src.clickup_crm_service.client')
    def test_fluxo_completo_crm(self, mock_client):
        """Testa o fluxo completo: seed -> buscar opções -> criar task"""
        
        # 1. Mock para seed_crm_list (lista já existe)
        mock_client.get.return_value = {
            "lists": [
                {"id": "list_123", "name": "CRM Teste"}
            ]
        }
        
        # 2. Mock para buscar_opcoes_servico
        mock_client.get.return_value = {
            "fields": [
                {
                    "name": "Tipo de Serviço",
                    "type": "drop_down",
                    "type_config": {
                        "options": [
                            {"name": "Desenvolvimento Web"},
                            {"name": "Consultoria"},
                            {"name": "Design"}
                        ]
                    }
                }
            ]
        }
        
        # 3. Mock para criar_task_cliente
        mock_client.post.return_value = {
            "id": "task_456",
            "name": "João Silva",
            "description": "E-mail: joao@teste.com\nTipo de serviço: Desenvolvimento Web"
        }
        
        # Executa o fluxo completo
        list_id = seed_crm_list()
        opcoes = buscar_opcoes_servico(list_id)
        task = criar_task_cliente(list_id, self.cliente_teste)
        
        # Verificações
        self.assertEqual(list_id, "list_123")
        self.assertEqual(opcoes, ["Desenvolvimento Web", "Consultoria", "Design"])
        self.assertEqual(task.id, "task_456")
        self.assertEqual(task.nome, "João Silva")

    @patch('src.clickup_crm_service.client')
    def test_fluxo_criar_nova_lista(self, mock_client):
        """Testa fluxo quando precisa criar nova lista"""
        
        # 1. Mock para seed_crm_list (lista não existe)
        mock_client.get.return_value = {
            "lists": [
                {"id": "list_999", "name": "Outra Lista"}
            ]
        }
        
        # Mock para criação da nova lista
        mock_client.post.return_value = {
            "id": "new_list_123",
            "name": "CRM Teste"
        }
        
        list_id = seed_crm_list()
        
        self.assertEqual(list_id, "new_list_123")
        mock_client.get.assert_called_once()
        mock_client.post.assert_called_once()

    def test_cliente_validation(self):
        """Testa validação dos dados do cliente"""
        # Teste com dados válidos
        cliente_valido = Cliente(
            nome="Maria Santos",
            email="maria@teste.com",
            tipo_servico="Consultoria"
        )
        
        self.assertEqual(cliente_valido.nome, "Maria Santos")
        self.assertEqual(cliente_valido.email, "maria@teste.com")
        self.assertEqual(cliente_valido.tipo_servico, "Consultoria")
        self.assertEqual(cliente_valido.status, "Novo")  # Valor padrão

    def tearDown(self):
        # Limpa variáveis de ambiente após os testes
        if 'CLICKUP_API_TOKEN' in os.environ:
            del os.environ['CLICKUP_API_TOKEN']
        if 'CLICKUP_SPACE_ID' in os.environ:
            del os.environ['CLICKUP_SPACE_ID']
        if 'CLICKUP_CRM_LIST_NAME' in os.environ:
            del os.environ['CLICKUP_CRM_LIST_NAME']

if __name__ == '__main__':
    unittest.main() 