"""UTILS - Configuração das variáveis de ambiente."""
from pydantic import BaseSettings


# ------------------------------------------------------------------------------------------------------------
class Variaveis(BaseSettings):
    """Classe de configuração do pydantic que controla as variáveis de ambiente."""

    # Variáveis do SSM
    dynamodb_table: str
    dax_cluster_endpoint: str


# ------------------------------------------------------------------------------------------------------------
