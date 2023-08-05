"""Pydantic Model - Bling."""
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


# ------------------------------------------------------------------------------------------------------------


class BlingPedidoCliente(BaseModel):
    """Dados do cliente do pedido."""

    nome: Optional[str]
    cnpj: str
    ie: Optional[str]
    rg: Optional[str]
    endereco: Optional[str]
    numero: Optional[str]
    complemento: Optional[str]
    cidade: Optional[str]
    bairro: Optional[str]
    cep: str
    uf: Optional[str]
    email: Optional[str]
    celular: Optional[str]
    fone: Optional[str]


class BlingPedidoItem(BaseModel):
    """Dados dos produtos de cada item do pedido."""

    codigo: Optional[str]
    descricao: Optional[str]
    quantidade: str
    valorunidade: str
    precocusto: Optional[str]
    desconto_item: Optional[str] = Field(None, alias="descontoItem")
    un: Optional[str]
    peso_bruto: Optional[str] = Field(None, alias="pesoBruto")
    largura: Optional[str]
    altura: Optional[str]
    profundidade: Optional[str]
    unidade_medida: Optional[str] = Field(None, alias="unidadeMedida")
    descricao_detalhada: Optional[str] = Field(None, alias="descricaoDetalhada")


class BlingPedidoItens(BaseModel):
    """Itens dos pedido."""

    item: BlingPedidoItem


class BlingPedidoFormaPagamento(BaseModel):
    """Dados sobre a forma de pagamento do pedido."""

    id: Optional[str]
    descricao: Optional[str]
    codigo_fiscal: Optional[str] = Field(None, alias="codigoFiscal")


class BlingPedidoParcela(BaseModel):
    """Dados das parcelas a serem pagas do pedido."""

    id_lancamento: Optional[str] = Field(None, alias="idLancamento")
    valor: Optional[str]
    data_vencimento: Optional[str] = Field(None, alias="dataVencimento")
    obs: Optional[str]
    destino: Optional[str]
    forma_pagamento: BlingPedidoFormaPagamento


class BlingPedidoParcelas(BaseModel):
    """Item com os dados das parcelas a serem pagas do pedido."""

    parcela: BlingPedidoParcela


class BlingPedidoNota(BaseModel):
    """Dados da Nota Fiscal do Pedido."""

    serie: Optional[str]
    numero: Optional[str]
    data_emissao: Optional[str] = Field(None, alias="dataEmissao")
    situacao: Optional[str]
    chave_acesso: Optional[str] = Field(None, alias="chaveAcesso")
    valor_nota: Optional[str] = Field(None, alias="valorNota")


class BlingPedidoRemessaItem(BaseModel):
    """Dados das Remessas do Pedido."""

    numero: Optional[str]
    data_criacao: Optional[str] = Field(None, alias="dataCriacao")


class BlingPedidoDimensoes(BaseModel):
    """Dados das Dimensões dos Volumes."""

    peso: Optional[str]
    altura: Optional[str]
    largura: Optional[str]
    comprimento: Optional[str]
    diametro: Optional[str]


class BlingPedidoVolume(BaseModel):
    """Dados dos Volumes do pedido."""

    id: Optional[str]
    id_servico: Optional[str] = Field(None, alias="idServico")
    servico: Optional[str]
    codigo_servico: Optional[str] = Field(None, alias="codigoServico")
    codigo_rastreamento: Optional[str] = Field(None, alias="codigoRastreamento")
    data_saida: Optional[str] = Field(None, alias="dataSaida")
    prazo_entrega_previsto: Optional[str] = Field(None, alias="prazoEntregaPrevisto")
    valor_frete_previsto: Optional[str] = Field(None, alias="valorFretePrevisto")
    valor_declarado: Optional[str] = Field(None, alias="valorDeclarado")
    remessa: Optional[BlingPedidoRemessaItem]
    dimensoes: Optional[BlingPedidoDimensoes]
    url_rastreamento: Optional[str] = Field(None, alias="urlRastreamento")


class BlingPedidoVolumes(BaseModel):
    """Item com os dados de volumes do pedido."""

    volume: Optional[BlingPedidoVolume]


class BlingPedidoEnderecoEntrega(BaseModel):
    """Dados de endereço de entrega."""

    nome: Optional[str]
    endereco: Optional[str]
    numero: Optional[str]
    complemento: Optional[str]
    cidade: Optional[str]
    bairro: Optional[str]
    cep: Optional[str]
    uf: Optional[str]


class BlingPedidoTransporte(BaseModel):
    """Dados de transporte do pedido."""

    transportadora: Optional[str]
    cnpj: Optional[str]
    tipo_frete: Optional[str]
    volumes: Optional[List[BlingPedidoVolumes]]
    endereco_entrega: Optional[BlingPedidoEnderecoEntrega] = Field(None, alias="enderecoEntrega")


class BlingPedidoPedido(BaseModel):
    """Dados do pedido registrado na Bling."""

    desconto: Optional[str]
    observacoes: Optional[str]
    observacaointerna: Optional[str]
    data: Optional[str]
    numero: str
    numero_pedido_loja: str = Field(..., alias="numeroPedidoLoja")
    vendedor: Optional[str]
    valorfrete: str = Field("0")
    totalprodutos: Optional[str]
    totalvenda: Optional[str]
    situacao: Optional[str]
    loja: Optional[str]
    data_prevista: Optional[str] = Field(None, alias="dataPrevista")
    tipo_integracao: Optional[str] = Field(None, alias="tipoIntegracao")
    cliente: BlingPedidoCliente
    itens: List[BlingPedidoItens]
    parcelas: Optional[List[BlingPedidoParcelas]]
    nota: Optional[BlingPedidoNota]
    transporte: Optional[BlingPedidoTransporte]


class BlingPedido(BaseModel):
    """Item `Pedido` da resposta da API de Pedido no Bling."""

    pedido: BlingPedidoPedido
