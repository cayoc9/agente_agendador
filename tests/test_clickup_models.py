import unittest
from src.clickup_models import Cliente, Task

class TestClickUpModels(unittest.TestCase):
    
    def test_cliente_creation(self):
        """Testa criação de um cliente"""
        cliente = Cliente(
            nome="João Silva",
            email="joao@email.com",
            tipo_servico="Desenvolvimento Web"
        )
        
        self.assertEqual(cliente.nome, "João Silva")
        self.assertEqual(cliente.email, "joao@email.com")
        self.assertEqual(cliente.tipo_servico, "Desenvolvimento Web")
        self.assertEqual(cliente.status, "Novo")  # Valor padrão

    def test_cliente_with_custom_status(self):
        """Testa criação de cliente com status personalizado"""
        cliente = Cliente(
            nome="Maria Santos",
            email="maria@email.com",
            tipo_servico="Consultoria",
            status="Em Andamento"
        )
        
        self.assertEqual(cliente.status, "Em Andamento")

    def test_task_creation(self):
        """Testa criação de uma task"""
        task = Task(
            id="task_123",
            nome="Nova Task"
        )
        
        self.assertEqual(task.id, "task_123")
        self.assertEqual(task.nome, "Nova Task")
        self.assertEqual(task.custom_fields, {})  # Valor padrão
        self.assertEqual(task.assignees, [])  # Valor padrão
        self.assertIsNone(task.status)  # Valor padrão

    def test_task_with_custom_fields(self):
        """Testa criação de task com campos customizados"""
        custom_fields = {
            "email": "cliente@email.com",
            "telefone": "11999999999"
        }
        
        task = Task(
            id="task_456",
            nome="Task com Campos",
            custom_fields=custom_fields,
            assignees=["user_123"],
            status="Em Progresso"
        )
        
        self.assertEqual(task.custom_fields, custom_fields)
        self.assertEqual(task.assignees, ["user_123"])
        self.assertEqual(task.status, "Em Progresso")

    def test_task_without_id(self):
        """Testa criação de task sem ID (para novas tasks)"""
        task = Task(
            id=None,
            nome="Nova Task sem ID"
        )
        
        self.assertIsNone(task.id)
        self.assertEqual(task.nome, "Nova Task sem ID")

if __name__ == '__main__':
    unittest.main() 