# src/agents.py
# Definição dos agentes CrewAI (exemplo inicial)

from crewai import Agent

# Exemplo de agente para coletar dados do cliente
data_collector = Agent(
    name="Coletor de Dados",
    description="Coleta nome, e-mail e tipo de serviço do cliente via Telegram."
)

# Outros agentes podem ser definidos conforme o fluxo
