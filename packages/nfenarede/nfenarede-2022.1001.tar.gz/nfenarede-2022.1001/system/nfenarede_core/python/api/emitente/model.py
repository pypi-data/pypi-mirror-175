"""Pydantic Model - Emitente."""
import re
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import ConstrainedStr
from pydantic import EmailStr
from pydantic import Field
from pydantic import HttpUrl


# ------------------------------------------------------------------------------------------------------------


class EmitenteDadosTelefone(ConstrainedStr):
    """Classe especial para indicar REGEX em uma lista."""

    regex = re.compile(r"\d{11}")


class EmitenteDadosEndereco(BaseModel):
    """Dados de endereço do Emitente."""

    logradouro: str = Field(..., description="Nome da Rua/Avenida/etc.")
    numero: int = Field(..., description="Numero do Endereço", ge=0)
    complemento: Optional[str] = Field(None, description="Complemento adicional")
    bairro: str = Field(..., description="Bairro")
    cep: str = Field(..., description="CEP (Código de Endereçamento Postal)", regex=r"\d{8}")
    cidade: str = Field(..., description="Cidade")
    uf: str = Field(..., description="UF (Unidade da Federeção)", regex=r"[A-Z]{2}")
    ibge: int = Field(..., description="Código IBGE do Município", regex=r"\d{7}")


class Emitente(BaseModel):
    """Dados principais do Emitente."""

    pk: str = Field(..., description="Partition Key ('Emitente' + ID)")
    sk: str = Field(..., description="Sort Key")
    id: int = Field(..., description="ID do Emitente")
    razao: str = Field(..., description="Razão Social")
    nome: str = Field(..., description="Nome Fantasia")
    documento: str = Field(..., description="CPF ou CNPJ", regex=r"\d{14}|\d{11}")
    ie: str = Field(..., description="Inscrição Estadual")
    endereco: EmitenteDadosEndereco = Field(..., description="Endereço Completo")
    telefone: Optional[List[EmitenteDadosTelefone]] = Field(None, description="Lista de Telefones")
    url: Optional[HttpUrl] = Field(None, description="Endereço Internet")
    email: Optional[List[EmailStr]] = Field(None, description="Lista de E-mails")


# ------------------------------------------------------------------------------------------------------------
