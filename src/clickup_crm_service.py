from .clickup_client import ClickUpClient
from .clickup_models import Cliente, Task
from typing import List, Optional
import os

# IDs e nomes podem ser parametrizados via config/env
CLICKUP_API_TOKEN = os.getenv("CLICKUP_API_TOKEN", "SUA_API_KEY_AQUI")
SPACE_ID = os.getenv("CLICKUP_SPACE_ID", "SUA_SPACE_ID_AQUI")
FOLDER_ID = os.getenv("CLICKUP_FOLDER_ID", None)  # Opcional
CRM_LIST_NAME = os.getenv("CLICKUP_CRM_LIST_NAME", "CRM Clientes")

client = ClickUpClient(CLICKUP_API_TOKEN)

def seed_crm_list() -> str:
    """Cria a lista de CRM se não existir e retorna o ID da lista."""
    # Busca listas existentes no espaço/pasta
    if FOLDER_ID:
        endpoint = f"/folder/{FOLDER_ID}/list"
    else:
        endpoint = f"/space/{SPACE_ID}/list"
    listas = client.get(endpoint)
    for lista in listas.get("lists", []):
        if lista["name"] == CRM_LIST_NAME:
            return lista["id"]
    # Cria lista se não existir
    data = {"name": CRM_LIST_NAME}
    if FOLDER_ID:
        endpoint = f"/folder/{FOLDER_ID}/list"
    else:
        endpoint = f"/space/{SPACE_ID}/list"
    nova_lista = client.post(endpoint, data)
    return nova_lista["id"]

def buscar_opcoes_servico(list_id: str) -> List[str]:
    """Busca opções de serviço disponíveis nos custom fields da lista."""
    endpoint = f"/list/{list_id}/field"
    fields = client.get(endpoint)
    opcoes = []
    for field in fields.get("fields", []):
        if field["name"].lower() == "tipo de serviço" and "options" in field["type_config"]:
            opcoes = [opt["name"] for opt in field["type_config"]["options"]]
    return opcoes

def criar_task_cliente(list_id: str, cliente: Cliente) -> Task:
    """Cria uma nova task para o cliente na lista de CRM."""
    data = {
        "name": cliente.nome,
        "description": f"E-mail: {cliente.email}\nTipo de serviço: {cliente.tipo_servico}",
        # Adicionar custom_fields conforme necessário
        # "custom_fields": [...],
    }
    endpoint = f"/list/{list_id}/task"
    resp = client.post(endpoint, data)
    return Task(id=resp["id"], nome=resp["name"])  # Expandir conforme necessário

def atualizar_task(task_id: str, dados: dict):
    """Atualiza uma task existente com novos dados."""
    endpoint = f"/task/{task_id}"
    return client.put(endpoint, dados) 