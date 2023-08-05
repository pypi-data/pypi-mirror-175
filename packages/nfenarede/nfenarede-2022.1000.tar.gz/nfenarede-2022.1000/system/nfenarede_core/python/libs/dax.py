"""LIBS - DAX."""
from typing import Any
from typing import Dict

import amazondax

from ..utils.ambiente import Variaveis


# ------------------------------------------------------------------------------------------------------------
class DAX:
    """Classe com os principais métodos de acesso ao DynamoDB (CRUD)."""

    # --------------------------------------------------------------------------------------------------------
    def __init__(self) -> None:
        """Método construtor da classe DAX.

        Construtor que já faz a conexão com o DynamoDB e disponibiliza os
        recursos necessários para o a utilização do mesmo.
        """
        self.dax = amazondax.AmazonDaxClient.resource(endpoint_url=Variaveis.dax_cluster_endpoint)

    # --------------------------------------------------------------------------------------------------------
    def put_item(self, item: Dict[str, Dict[str, Any]]) -> None:
        """Salva os dados dentro do DynamoDB.

        Args:
            item (Dict[str, Dict[str, Any]]): Dicionário no formato `Item`, utilizado pelo DynamoDB
        """
        self.dax.put_item(Table=Variaveis.dynamodb_table, Item=item)


# ------------------------------------------------------------------------------------------------------------
