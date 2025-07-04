import unittest
from unittest.mock import patch, Mock
import requests
from src.clickup_client import ClickUpClient

class TestClickUpClient(unittest.TestCase):
    def setUp(self):
        self.api_token = "test_token_123"
        self.client = ClickUpClient(self.api_token)

    def test_init(self):
        """Testa se o cliente é inicializado corretamente"""
        self.assertEqual(self.client.api_token, self.api_token)
        self.assertIn("Authorization", self.client.headers)
        self.assertIn("Content-Type", self.client.headers)

    @patch('requests.get')
    def test_get_request(self, mock_get):
        """Testa requisição GET"""
        # Mock da resposta
        mock_response = Mock()
        mock_response.json.return_value = {"status": "success"}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Teste
        result = self.client.get("/test-endpoint")
        
        # Verificações
        mock_get.assert_called_once()
        self.assertEqual(result, {"status": "success"})

    @patch('requests.post')
    def test_post_request(self, mock_post):
        """Testa requisição POST"""
        # Mock da resposta
        mock_response = Mock()
        mock_response.json.return_value = {"id": "123", "name": "Test Task"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        # Teste
        data = {"name": "Test Task"}
        result = self.client.post("/test-endpoint", data)
        
        # Verificações
        mock_post.assert_called_once()
        self.assertEqual(result, {"id": "123", "name": "Test Task"})

    @patch('requests.put')
    def test_put_request(self, mock_put):
        """Testa requisição PUT"""
        # Mock da resposta
        mock_response = Mock()
        mock_response.json.return_value = {"status": "updated"}
        mock_response.raise_for_status.return_value = None
        mock_put.return_value = mock_response

        # Teste
        data = {"name": "Updated Task"}
        result = self.client.put("/test-endpoint", data)
        
        # Verificações
        mock_put.assert_called_once()
        self.assertEqual(result, {"status": "updated"})

    @patch('requests.get')
    def test_get_with_params(self, mock_get):
        """Testa requisição GET com parâmetros"""
        # Mock da resposta
        mock_response = Mock()
        mock_response.json.return_value = {"tasks": []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        # Teste
        params = {"limit": 10, "page": 0}
        result = self.client.get("/tasks", params)
        
        # Verificações
        mock_get.assert_called_once()
        self.assertEqual(result, {"tasks": []})

if __name__ == '__main__':
    unittest.main() 