"""Integração - Bling - Classe Principal."""
import os
import re
import time
from typing import Any
from typing import List
from typing import Optional

import MySQLdb  # type: ignore
import requests  # type: ignore
from aws_lambda_powertools.logging.logger import Logger

from .exception import AlreadySavedError
from .exception import APIError
from .exception import EndOfPaginationError
from .exception import IntegrationError
from .model import BlingPedidoCliente
from .model import BlingPedidoItem
from .model import BlingPedidoPedido


# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(os.path.dirname(SCRIPT_DIR))


# ------------------------------------------------------------------------------------------------------------
# CONSTANTES

BLING_SITUACAO = {"EM_ABERTO": 6, "EM_ANDAMENTO": 15}


# ------------------------------------------------------------------------------------------------------------
class Bling:
    """Classe de implementação do Bling dentro da API."""

    apikey: str
    g3_empr_codi: int
    g3_clie_grup: int
    version: str
    page: int

    # --------------------------------------------------------------------------------------------------------
    def __init__(
        self,
        apikey: str,
        g3_empr_codi: int,
        g3_clie_grup: int,
        version: str = "v2",
    ) -> None:
        """Método Construtor - Configurações Gerais."""
        self.apikey = apikey
        self.g3_empr_codi = g3_empr_codi
        self.g3_clie_grup = g3_clie_grup
        self.version = version
        self.log = Logger(service="integracao/bling")

    # --------------------------------------------------------------------------------------------------------
    def mysql_connect(self) -> None:
        """Faz a conexão com o banco de dados do G3."""
        self.mysql_cnx = MySQLdb.connect(
            user=os.getenv("MYSQLG3_USER"),
            passwd=os.getenv("MYSQLG3_PASS"),
            host=os.getenv("MYSQLG3_HOST"),
            db=f"G3_G{self.g3_clie_grup:04d}",
        )
        self.mysql = self.mysql_cnx.cursor()

    # --------------------------------------------------------------------------------------------------------
    def mysql_disconnect(self) -> None:
        """Faz a conexão com o banco de dados do G3."""
        self.mysql.close()
        # self.mysql_cnx.close()

    # --------------------------------------------------------------------------------------------------------
    def bling_request(
        self,
        method: str,
        resource: str,
        page: int = 1,
        data: Any = None,
        retorno: Any = None,
        filters: Any = None,
    ) -> Any:
        """Faz a request dos dados na Bling de acordo com o método solicitado.

        _extended_summary_

        Args:
            method (str): Métodos de requisição HTTP
            resource (str): Recurso que será solicitado
            page (int): Número da página. (Padrão: 1)
            data (Any): Dados enviados para a requisição. (Padrão: None)
            retorno (Any): Tipo de retorno esperado. (Padrão: None)
            filters (Any): Filtros de busca. (Padrão: None)

        Raises:
            EndOfPaginationError: Quando chegar à última página de resultados.
            APIError: Para erros retornados pela própria Bling.
            IntegrationError: Para quando não houver algum dado de retorno na resposta.

        Returns:
            Any: Retorno do Bling em JSON
        """
        # Obtem a URL correta de acordo com os parâmetros
        url = self.bling_url(method, resource, page, data, filters)

        # Apaga os dados caso seja um método GET
        if method in ("POST", "PUT", "PATCH"):
            data["apikey"] = self.apikey  # type: ignore
        else:
            data = None

        self.log.info("Fazendo requisição para Bling!", extra={"method": method, "url": url, "data": data})
        request = requests.request(method, url, data=data)
        result = request.json()
        self.log.info("Resposta da Bling", extra={"result": result})

        # Verifica se houve erro no retorno
        if "erros" in result.get("retorno", {}):
            try:
                if result["retorno"]["erros"][0]["erro"]["cod"] == 14:
                    raise EndOfPaginationError()
                raise APIError()

            except KeyError as err:
                raise APIError() from err

        # Verifica se há dados do recurso solicitado
        if not retorno:
            retorno = resource

        if retorno not in result.get("retorno", {}):
            raise IntegrationError()

        # Retorna os registros
        return result["retorno"][retorno]

    # --------------------------------------------------------------------------------------------------------
    def bling_url(self, method: str, resource: str, page: int, data: Any, filters: Any) -> str:
        """Monta a URL da API Bling.

        Args:
            method (str): Método HTTP (GET, POST, PUT, DELETE..)
            resource (str): Recurso que será acessado
            page (int): Número da página.
            data (Any): Dados enviados para a requisição
            filters (Any): Filtros de busca

        Returns:
            str: URL completa da API Bling.
        """
        # Monta URL com a API Key
        if page > 1:
            url = f"https://bling.com.br/Api/{self.version}/{resource}/page={page}/json/"
        else:
            url = f"https://bling.com.br/Api/{self.version}/{resource}/json/"

        # Retorna a URL nesse formato caso não seja GET
        if method != "GET":
            return url

        # Insere a APIKey para métodos GET
        url = f"{url}?apikey={self.apikey}"

        # Monta parametros caso exista
        if data is not None and len(data) > 0:
            for key, value in data.items():
                url = f"{url}&{key}={value}"

        # Monta filtros caso exista (filters=nome_do_filtro1[valor1];nome_do_filtro_2[valor2])
        if filters is not None and len(filters) > 0:
            filter_arr = []
            separator = ";"
            for key, value in filters.items():
                filter_arr.append(f"{key}[{value}]")
            url = f"{url}&filters={separator.join(filter_arr)}"

        return url

    # --------------------------------------------------------------------------------------------------------
    def normalize(self, text: Optional[str]) -> Optional[str]:
        """Normaliza uma string retirando os espaços, acentos e deixando tudo minúsculo.

        Args:
            text (Optional[str]): String para ser normalizada

        Returns:
            Optional[str]: String normalizada
        """
        if text:
            return text.upper()
        return None

    # --------------------------------------------------------------------------------------------------------
    def bling_importar_pedidos(self) -> Any:
        """Importa todos os pedidos em aberto do Bling.

        Faz uma busca através da API do Bling para puxar todos os dados de pedidos que estão em aberto
        (status "Em aberto" no Bling) e importa os dados para o Sistema G3.

        Returns:
            Any: _description_
        """
        # Prepara todas variáveis para processamento
        page = 1
        response = []

        # Faz a conexão com o banco de dados G3
        self.mysql_connect()

        # Busca todos os pedidos no Bling
        while True:
            try:
                result: List[dict] = self.bling_request(
                    "GET", "pedidos", page, filters={"idSituacao": BLING_SITUACAO["EM_ABERTO"]}
                )
                page += 1

                # Lê todos os pedidos
                for pedido_bling in result:
                    try:
                        # Monta o objeto Pydantic, importa e faz o commit
                        pedido = BlingPedidoPedido(**pedido_bling["pedido"])
                        task = self.bling_importar_pedido_individual(pedido)
                        response.append(task)
                        self.mysql_cnx.commit()

                    except AlreadySavedError:
                        # Quando já tem o pedido salvo, apenas muda o status para "Em Andamento"
                        numero = pedido_bling["pedido"]["numero"]
                        numero_pedido_loja = pedido_bling["pedido"].get("numero_pedido_loja", "#")
                        self.log.exception(
                            "Pedido já foi incluído anteriormente!",
                            extra={"numero": numero, "v001_pedi_clie": numero_pedido_loja},
                        )
                        self.bling_atualiza_status_pedido(numero, BLING_SITUACAO["EM_ANDAMENTO"])
                        self.mysql_cnx.rollback()

                time.sleep(0.5)

            # Quando não houver mais páginas para ler do Bling, cai nessa exception e encerra o loop
            except EndOfPaginationError:
                break
            finally:
                # Desconecta o banco de dados G3
                self.mysql_disconnect()

        # Retorna os resultados das requisições
        return response

    # --------------------------------------------------------------------------------------------------------
    def bling_importar_pedido_individual(self, pedido: BlingPedidoPedido) -> Any:
        """Grava os dados de cada pedido individualmente."""
        # 1. Dados do Cliente
        clie_codi = self.g3_grava_comprador(pedido.cliente)

        # 2. Dados do pedido
        v001_id = self.g3_grava_vendas01(
            clie_codi, pedido.numero_pedido_loja, pedido.valorfrete, pedido.tipo_integracao
        )

        # 3. Itens do pedido
        for i in pedido.itens:
            self.g3_grava_vendas02(v001_id, i.item)

        # 4. Totais do pedido
        self.g3_atualiza_vendas01(v001_id)

        # 5. Atualizar status do pedido na Bling
        self.bling_atualiza_status_pedido(pedido.numero, BLING_SITUACAO["EM_ANDAMENTO"])

    # --------------------------------------------------------------------------------------------------------
    def g3_grava_comprador(self, cliente: BlingPedidoCliente) -> Any:
        """Grava os dados do comprador."""
        # Obtem os dados do comprador
        comprador = {
            "cada_empr": self.g3_empr_codi,
            "cada_fant": self.normalize(cliente.nome),
            "cada_nome": self.normalize(cliente.nome),
            "cada_end2": self.normalize(f"{cliente.endereco}, {cliente.numero} {cliente.complemento}".strip()),
            "cada_bair": self.normalize(cliente.bairro),
            "cada_cida": self.normalize(cliente.cidade),
            "cada_uf": self.normalize(cliente.uf),
            "cada_cep": re.sub(r"\D", "", cliente.cep),
            "cada_tel1": cliente.fone,
            "cada_tel2": cliente.celular,
            "cada_tel3": None,
            "cada_tipo": "F",
            "cada_cnpj": cliente.cnpj,
            "cada_insc": "NÃO CONTRIBUINTE",
            "cada_home": None,
            "cada_email": cliente.email,
        }

        # Endereço não foi encontrado/informado no Pedido: indica Endereço Não Encontrado/Cadastrado
        if comprador["cada_end2"] == ",":
            comprador["cada_end2"] = "XYZ123"

        if len(cliente.cnpj) > 11:
            comprador["cada_tipo"] = "J"
            comprador["cada_insc"] = cliente.ie

        # Verifica se o usuário já está cadastrado
        query = "SELECT cada_codi FROM mob_cada WHERE cada_empr = %s AND cada_cnpj = %s"
        self.mysql.execute(query, (comprador["cada_empr"], comprador["cada_cnpj"]))
        result = self.mysql.fetchone()  # type: ignore

        if not result:
            query = "SELECT IFNULL(MAX(cada_codi)+1, 1) AS cada_codi FROM mob_cada WHERE cada_empr = %s"
            self.mysql.execute(query, (comprador["cada_empr"],))
            result = self.mysql.fetchone()  # type: ignore
            cada_codi = result[0]  # type: ignore
            comprador["cada_codi"] = cada_codi

            # Salva os dados no banco de dados G3
            query = """
                INSERT INTO mob_cada (cada_empr, cada_codi, cada_fant, cada_nome, cada_end2,
                                      cada_bair, cada_cida, cada_uf, cada_cep, cada_tel1,
                                      cada_tipo, cada_cnpj, cada_insc, cada_email, cada_data)
                VALUES (%(cada_empr)s, %(cada_codi)s, %(cada_fant)s, %(cada_nome)s, %(cada_end2)s,
                        %(cada_bair)s, %(cada_cida)s, %(cada_uf)s, %(cada_cep)s, %(cada_tel1)s,
                        %(cada_tipo)s, %(cada_cnpj)s, %(cada_insc)s, %(cada_email)s, NOW())
            """
            self.mysql.execute(query, comprador)
        else:
            cada_codi = result[0]  # type: ignore
            comprador["cada_codi"] = cada_codi
            query = """
                UPDATE mob_cada SET cada_fant = %(cada_fant)s,
                                    cada_nome = %(cada_nome)s,
                                    cada_end2 = %(cada_end2)s,
                                    cada_bair = %(cada_bair)s,
                                    cada_cida = %(cada_cida)s,
                                    cada_uf = %(cada_uf)s,
                                    cada_cep = %(cada_cep)s,
                                    cada_tel1 = %(cada_tel1)s,
                                    cada_tipo = %(cada_tipo)s,
                                    cada_cnpj = %(cada_cnpj)s,
                                    cada_insc = %(cada_insc)s,
                                    cada_email = %(cada_email)s,
                                    cada_data = NOW()
                WHERE cada_empr = %(cada_empr)s AND cada_codi = %(cada_codi)s
            """

        return cada_codi

    # --------------------------------------------------------------------------------------------------------
    def g3_grava_vendas01(
        self, clie_codi: Any, v001_pedi_clie: str, v001_total_st: str, v001_trans_total: Optional[str]
    ) -> Any:
        """Grava os dados do Vendas01."""
        # Verifica se o usuário já está cadastrado
        query = "SELECT v001_id FROM mob_v001 WHERE v001_empr = %s AND v001_pedi_clie = %s"
        self.mysql.execute(query, (self.g3_empr_codi, v001_pedi_clie))
        v001_id = self.mysql.fetchone()  # type: ignore

        if v001_id:
            raise AlreadySavedError()

        lojas = {
            "Shopee": 4,
            "IntegraCommerce": 5,
            "SkyHub": 6,
        }

        v001 = {
            "v001_empr": self.g3_empr_codi,
            "v001_clie": clie_codi,
            "v001_pedi_clie": v001_pedi_clie,
            "v001_obs": "PEDIDO GERADO VIA INTEGRAÇÃO KOMU - BLING",
            "v001_pedi": "0",
            "v001_total_st": v001_total_st,
            "v001_tran": lojas.get(v001_trans_total, "9"),  # type: ignore
        }

        query = """
            INSERT INTO mob_v001 (v001_empr, v001_clie, v001_pedi_clie, v001_obs,
                                  v001_pedi, v001_total_st, v001_tran, v001_data)
            VALUES (%(v001_empr)s, %(v001_clie)s, %(v001_pedi_clie)s, %(v001_obs)s,
                    %(v001_pedi)s, %(v001_total_st)s, %(v001_tran)s, NOW())
        """
        self.mysql.execute(query, v001)
        v001_id = self.mysql.lastrowid

        return v001_id

    # --------------------------------------------------------------------------------------------------------
    def g3_grava_vendas02(self, v001_id: Any, item: BlingPedidoItem) -> Any:
        """Grava os dados do Vendas02."""
        if not item.codigo:
            item.codigo = "SEMCODIGO"

        v002_valor_geral = float(item.quantidade) * float(item.valorunidade)

        v002 = {
            "v001_id": v001_id,
            "v002_prod": item.codigo,
            "v002_qtde": item.quantidade,
            "v002_valor_prod": float(item.valorunidade),
            "v002_valor_geral": v002_valor_geral,
        }

        query = """
            INSERT INTO mob_v002 (v001_id, v002_prod, v002_qtde, v002_valor_prod_ca, v002_valor_prod_gr,
                                  v002_ipi, v002_valor_geral_ca, v002_valor_geral_gr)
            VALUES (%(v001_id)s, %(v002_prod)s, %(v002_qtde)s, %(v002_valor_prod)s,
                    %(v002_valor_prod)s, 0, %(v002_valor_geral)s, %(v002_valor_geral)s)
        """
        self.mysql.execute(query, v002)

    # --------------------------------------------------------------------------------------------------------
    def g3_atualiza_vendas01(self, v001_id: Any) -> None:
        """Atualiza os valores totais do Vendas01."""
        query = """
            UPDATE mob_v001 v1
            INNER JOIN
            (SELECT v001_id, SUM(v002_valor_prod_ca * v002_qtde) total
                FROM mob_v002
                WHERE v001_id = %s
                GROUP BY v001_id) v2 ON v1.v001_id = v2.v001_id
            SET v1.v001_total_prod_ca  = v2.total,
                v1.v001_total_prod_gr  = v2.total,
                v1.v001_total_geral_ca = v2.total,
                v1.v001_total_geral_gr = v2.total;
        """
        self.mysql.execute(query, (v001_id,))

    # --------------------------------------------------------------------------------------------------------
    def bling_atualiza_status_pedido(self, pedido: str, situacao: int) -> Any:
        """Atualiza o status do pedido dentro da Bling."""
        data = dict(
            xml=f"""<?xml version="1.0" encoding="UTF-8"?><pedido><idSituacao>{situacao}</idSituacao></pedido>"""
        )
        result = self.bling_request("PUT", f"pedido/{pedido}", 0, data, "pedidos")
        return result


# ------------------------------------------------------------------------------------------------------------
