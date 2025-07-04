import unittest
from unittest.mock import patch, Mock
from src.clickup_crm_service import (
    seed_crm_list, 
    buscar_opcoes_servico, 
    criar_task_cliente, 
    atualizar_task
)
from src.clickup_models import Cliente, Task

class TestClickUpCRMService(unittest.TestCase):
    
    def setUp(self):
        self.cliente_teste = Cliente(
            nome="Teste Cliente",
            email="teste@email.com",
            tipo_servico="Desenvolvimento"
        )

    @patch('src.clickup_crm_service.client')
    def test_seed_crm_list_existing(self, mock_client):
        """Testa seed quando a lista já existe"""
        # Mock da resposta da API
        mock_client.get.return_value = {
            "lists": [
                {"id": "list_123", "name": "CRM Clientes"},
                {"id": "list_456", "name": "Outra Lista"}
            ]
        }
        
        result = seed_crm_list()
        
        self.assertEqual(result, "list_123")
        mock_client.get.assert_called_once()

    @patch('src.clickup_crm_service.client')
    def test_seed_crm_list_create_new(self, mock_client):
        """Testa seed quando precisa criar nova lista"""
        # Mock da resposta da API - lista não existe
        mock_client.get.return_value = {
            "lists": [
                {"id": "list_456", "name": "Outra Lista"}
            ]
        }
        
        # Mock da criação da nova lista
        mock_client.post.return_value = {
            "id": "new_list_789",
            "name": "CRM Clientes"
        }
        
        result = seed_crm_list()
        
        self.assertEqual(result, "new_list_789")
        mock_client.get.assert_called_once()
        mock_client.post.assert_called_once()

    @patch('src.clickup_crm_service.client')
    def test_buscar_opcoes_servico(self, mock_client):
        """Testa busca de opções de serviço"""
        # Mock da resposta da API com custom fields
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
                },
                {
                    "name": "Outro Campo",
                    "type": "text"
                }
            ]
        }
        
        result = buscar_opcoes_servico("list_123")
        
        expected = ["Desenvolvimento Web", "Consultoria", "Design"]
        self.assertEqual(result, expected)
        mock_client.get.assert_called_once_with("/list/list_123/field")

    @patch('src.clickup_crm_service.client')
    def test_buscar_opcoes_servico_empty(self, mock_client):
        """Testa busca quando não há opções de serviço"""
        mock_client.get.return_value = {
            "fields": [
                {
                    "name": "Outro Campo",
                    "type": "text"
                }
            ]
        }
        
        result = buscar_opcoes_servico("list_123")
        
        self.assertEqual(result, [])
        mock_client.get.assert_called_once()

    @patch('src.clickup_crm_service.client')
    def test_criar_task_cliente(self, mock_client):
        """Testa criação de task para cliente"""
        # Mock da resposta da API
        mock_client.post.return_value = {
            "id": "task_123",
            "name": "Teste Cliente",
            "description": "E-mail: teste@email.com\nTipo de serviço: Desenvolvimento"
        }
        
        result = criar_task_cliente("list_123", self.cliente_teste)
        
        self.assertIsInstance(result, Task)
        self.assertEqual(result.id, "task_123")
        self.assertEqual(result.nome, "Teste Cliente")
        
        # Verifica se a API foi chamada com os dados corretos
        expected_data = {
            "name": "Teste Cliente",
            "description": "E-mail: teste@email.com\nTipo de serviço: Desenvolvimento"
        }
        mock_client.post.assert_called_once_with("/list/list_123/task", expected_data)

    @patch('src.clickup_crm_service.client')
    def test_atualizar_task(self, mock_client):
        """Testa atualização de task"""
        # Mock da resposta da API
        mock_client.put.return_value = {
            "id": "task_123",
            "name": "Task Atualizada",
            "status": "Em Progresso"
        }
        
        dados_atualizacao = {
            "name": "Task Atualizada",
            "status": "Em Progresso"
        }
        
        result = atualizar_task("task_123", dados_atualizacao)
        
        self.assertEqual(result, {
            "id": "task_123",
            "name": "Task Atualizada",
            "status": "Em Progresso"
        })
        mock_client.put.assert_called_once_with("/task/task_123", dados_atualizacao)

if __name__ == '__main__':
    unittest.main() 