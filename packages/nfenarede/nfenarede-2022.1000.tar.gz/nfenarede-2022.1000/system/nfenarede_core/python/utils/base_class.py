"""UTILS - Base com métodos utilizados em todas as entidades."""
import os
import uuid
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Dict

import simplejson as json  # type: ignore
from aws_lambda_powertools.logging.logger import Logger

from ..libs.dax import DAX


# ------------------------------------------------------------------------------------------------------------
class Base(ABC):
    """Classe com configurações e métodos básicos das entidades do sistema.

    Essa classe será a base (ba-dum-tss) das classes de todas as entidades
    do sistema. Dessa forma, ao herdar os métodos e atributos dessa classe,
    a entidade terá tudo o que for necessário para poder trabalhar de forma
    correta!
    """

    data: Any

    # --------------------------------------------------------------------------------------------------------
    def __init__(self, modulo: str = "base") -> None:
        """Método construtor da classe Base.

        Esse construtor apenas prepara os métodos que serão utilizados
        (Ex: json, os, uuid, etc...), bem como configura o log dos dados
        no AWS Cloudwatch utilizando o `aws_lambda_powertools`.

        Args:
            modulo (str): Nome do módulo para identificação nos logs.
        """
        self.uuid = uuid
        self.json = json
        self.os = os
        self.log = Logger(service=modulo)
        self.dax = DAX()

    # --------------------------------------------------------------------------------------------------------
    """Decorator para propiedades abstratas que serão implementados pelos herdeiros."""

    @property
    @abstractmethod
    def _pk(self) -> str:
        ...

    @property
    @abstractmethod
    def _sk(self) -> str:
        ...

    # --------------------------------------------------------------------------------------------------------
    @property
    def item(self) -> Dict[str, Dict[str, Any]]:
        """Obtem os dados da entidade em formato `Item` (DynamoDB).

        Cada entidade terá sua representação de estrutura de dados montada por um model do pydantic.
        O DynamoDB, por sua vez, utiliza um mapa com nomes e valores, denominado `AttributeValue`.
        Essa função faz a manipulação dos dados para o formato `Item` utilizado pelo DynamoDB.

        Returns:
            dict[str, dict[str, Any]]: Dicionário no formato `Item`, utilizado pelo DynamoDB
        """
        item = self.keys()

        for name, value in self.data:
            item[name] = self.to_attribute_value(value)

        return item

    # --------------------------------------------------------------------------------------------------------
    def keys(self) -> Dict[str, Dict[str, str]]:
        """Retorna a chave primária do registro.

        Esse método é utilizado sempre que for necessário obter a chave primária
        do registro que está sendo trabalhado. A chave primária sempre será
        composta pela PK (chave de partição) e SK (chave de ordenação).

        Returns:
            dict[str, dict[str, str]]: Dicionário com a chave primária (PK + SK)
        """
        return {"pk": {"S": self._pk}, "sk": {"S": self._sk}}

    # --------------------------------------------------------------------------------------------------------
    def to_attribute_value(self, value: Any) -> Dict[str, Any]:
        """Transforma um atributo de um modelo em um `AttributeValue` do DynamoDB.

        Método para facilitar a transformação dos dados, mapeando cada elemento e o modificando
        conforme seu tipo.

        Args:
            value (Any): Valor do atributo.

        Raises:
            ValueError: Em caso do valor não se encaixar em nenhum dos formatos aceitos.

        Returns:
            dict[str, Any]: Dicionário no formato `AttributeValue`, utilizado pelo DynamoDB
        """
        if value is None:
            return {"NULL": True}
        if value is True or value is False:
            return {"BOOL": value}
        if isinstance(value, (int, float)):
            return {"N": json.dumps(value)}
        if isinstance(value, str):
            return {"S": value}
        if isinstance(value, list):
            return {"L": [self.to_attribute_value(v) for v in value]}
        if isinstance(value, dict):
            return {"M": {k: self.to_attribute_value(v) for k, v in value.items()}}
        raise ValueError(f"Unknown value type: {type(value).__name__}")

    # --------------------------------------------------------------------------------------------------------
    def salvar(self) -> None:
        """Salva os dados da entidade.

        Método para salvar novos dados no sistema. Todos os dados precisam estar
        de acordo com o formato do schema definido na entidade.
        """
        self.log.info("Salvando dados no DynamoDB...", extra={"data": self.item})
        self.dax.put_item(self.item)


# ------------------------------------------------------------------------------------------------------------
