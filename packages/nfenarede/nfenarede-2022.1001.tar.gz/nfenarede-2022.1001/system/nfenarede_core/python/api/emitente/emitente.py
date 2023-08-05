"""Entidade - Emitente."""

from ...utils.base_class import Base
from . import model


# ------------------------------------------------------------------------------------------------------------
class Emitente(Base):
    """Emitente - Empresa que utiliza o sistema e portanto emite notas fiscais."""

    def __init__(self, emitente: model.Emitente) -> None:
        """Método construtor."""
        super().__init__("emitente")
        self.data = emitente

    def _pk(self) -> str:
        """Chave de partição da tabela dentro do DynamoDB."""
        return f"EMITENTE#{self.data.id}"

    def _sk(self) -> str:
        """Chave de ordenação da tabela dentro do DynamoDB."""
        return "_DADOSCADASTRAIS"


# ------------------------------------------------------------------------------------------------------------
