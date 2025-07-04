# src/tasks.py
# Definição das tarefas CrewAI (exemplo inicial)

from crewai import Task

# Exemplo de tarefa para registrar dados em uma planilha
google_sheets_task = Task(
    name="Registrar Dados",
    description="Registra os dados do cliente no Google Sheets."
)

# Outros tasks podem ser definidos conforme o fluxo
