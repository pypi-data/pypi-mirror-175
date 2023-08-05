"""Microservices - Cobrança de Clientes no ContaAzul."""
import os
from datetime import datetime
from typing import List

import requests  # type: ignore
import simplejson as json  # type: ignore
from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver
from aws_lambda_powertools.event_handler import Response
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext
from requests_oauthlib import OAuth2Session  # type: ignore


# ------------------------------------------------------------------------------------------------------------
# AWS Lambda Power Tools
logger = Logger()
app = APIGatewayHttpResolver()

# ------------------------------------------------------------------------------------------------------------
# Constantes
client_id = os.getenv("CONTAAZUL_CLIENT_ID")
client_secret = os.getenv("CONTAAZUL_CLIENT_SECRET")
redirect_uri = os.getenv("CONTAAZUL_REDIRECT_URI")
scope = ["sales"]
conta_azul = {
    "auth": "https://api.contaazul.com/auth/authorize",
    "token": "https://api.contaazul.com/oauth2/token",
    "sale": "https://api.contaazul.com/v1/sales",
}

# ------------------------------------------------------------------------------------------------------------


@app.get("/auth")
def auth() -> Response:
    """Rota de autenticação OAuth2 do Conta Azul.

    A API da Conta Azul utiliza o OAuth2 como modo de autenticação. Para isso é necessário
    seguir os protocolos corretamente. Aqui há dois processos internos: 1) Solicitação de
    autorização / 2) Após autorização, processamento dos dados.

    Returns:
        Response: Resposta do LambdaPowerTools.
    """
    # Instancia a clase para OAuth2.0
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)

    # Verifica se foi informado o parametro `code` na URL
    code = app.current_event.get_query_string_value(name="code", default_value=None)
    if not code:
        authorization_url, state = oauth.authorization_url(conta_azul["auth"])
        return Response(status_code=302, headers={"Location": authorization_url})

    # Obtem o token
    token = oauth.fetch_token(
        conta_azul["token"],
        code=code,
        client_secret=client_secret,
    )

    # Obtem as faturas
    faturas = obter_faturas()
    body = {"token": token, "faturas": []}

    # Processa as faturas
    for fatura in faturas:
        cobranca = montar_cobranca(fatura)
        payload = json.dumps(cobranca)
        headers = {"Authorization": f'Bearer {token.get("access_token", None)}', "Content-Type": "application/json"}
        r = requests.request("POST", conta_azul["sale"], headers=headers, data=payload)
        body["faturas"].append(r.json())

    return Response(status_code=200, body=json.dumps(body))


@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_HTTP)  # type: ignore
def handler(event: dict, context: LambdaContext) -> dict:
    """Função de entrada para o API Gateway HTTP utilizando AWS PowerTools.

    Essa função apenas recebe os dados passados via API Gateway e reencaminha para a função
    com o decorator que corresponde à rota correspondente. Também já injeta os dados recebidos
    para o log.

    Args:
        event (dict): Dados de entrada da função Lambda.
        context (LambdaContext): Contexto da função Lambda.

    Returns:
        dict: Resposta enviada pela função da rota correspondente.
    """
    return app.resolve(event, context)


# ------------------------------------------------------------------------------------------------------------
def montar_cobranca(fatura: dict) -> dict:
    """Monta o objeto de cobrança de acordo com o esquema da API Conta Azul.

    Args:
        fatura (dict): Dados da cobrança obtido no banco de dados.

    Returns:
        dict: Objeto de cobrança formatado para API Conta Azul.
    """
    # Monta as variáeis
    mes = fatura.get("mes", None)
    total = fatura.get("total", 0)
    nfe = fatura.get("nfe", 0)
    pdf = fatura.get("pdf", 0)
    hora = datetime.now()

    return {
        "emission": hora.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "status": "COMMITTED",
        "customer_id": fatura.get("contaazul_id", None),
        "services": [
            {
                "description": f"NFe na rede - Período de {mes} - {total} (NFE = {nfe} / PDF = {pdf})",
                "quantity": 1,
                "service_id": obter_id_servico(total),
                "value": fatura.get("valor", 0),
            }
        ],
        "payment": {
            "type": "CASH",
            "method": "BANKING_BILLET",
            "installments": [
                {
                    "number": 1,
                    "value": fatura.get("valor", 0),
                    "due_date": f"{fatura.get('vencimento')}T23:59:59.999Z",
                    "status": "PENDING",
                }
            ],
        },
    }


# ------------------------------------------------------------------------------------------------------------
def obter_id_servico(qtde: int) -> str:
    """Retorna o ID do serviço cadastrado no Conta Azul de acordo com número de notas enviadas.

    Args:
        qtde (int): Quantidade de notas e PDFs enviados.

    Returns:
        str: Código do serviço cadastrado no Conta Azul.
    """
    if qtde > 0 and qtde < 101:
        return "85830c12-c080-4325-a950-d1a17235040c"
    elif qtde > 100 and qtde < 201:
        return "11c64ee9-98c9-4a47-af4b-027b5caa0295"
    elif qtde > 200 and qtde < 501:
        return "a8531cf3-f0f1-4f0c-beb0-541787037e67"
    elif qtde > 500 and qtde < 1001:
        return "96187bc8-87e4-42eb-86ea-b621c11fa90d"
    elif qtde > 1000 and qtde < 2001:
        return "0a8286f7-2227-461c-9e45-029ae72e914c"
    else:
        return "89f181e3-f632-464b-8f30-95079aa5144b"


# ------------------------------------------------------------------------------------------------------------
def obter_faturas() -> List[dict]:
    """Obtem as faturas que foram salvas no banco de dados.

    Atualmente vamos pegar diretamente do banco de dados MySQL as faturas que já
    foram processadas pelo sistema anterior. Em breve iremos fazer a rotina completa
    aqui mesmo.

    Returns:
        List[dict]: Lista de dicionários com os dados das faturas.
    """
    return [
        {
            "contaazul_id": "0419dd13-2c2b-49c6-ab82-72e07d1c4c31",
            "mes": "10/2022",
            "total": 521,
            "nfe": 0,
            "pdf": 521,
            "valor": 300.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "d2a9348b-8c9d-41e2-b1ad-f33d040cf1c0",
            "mes": "10/2022",
            "total": 1,
            "nfe": 1,
            "pdf": 0,
            "valor": 50.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "25f44412-21e9-4913-900f-1f4796b986e4",
            "mes": "10/2022",
            "total": 54,
            "nfe": 27,
            "pdf": 27,
            "valor": 50.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "902c3af0-2369-4d36-8536-8edafb5acbbc",
            "mes": "10/2022",
            "total": 35,
            "nfe": 34,
            "pdf": 1,
            "valor": 50.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "fe7fb688-3389-4d82-b3a6-2ebfb85d282d",
            "mes": "10/2022",
            "total": 126,
            "nfe": 39,
            "pdf": 87,
            "valor": 85.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "a23898fe-f222-4bf9-8daa-3d67dc200b38",
            "mes": "10/2022",
            "total": 43,
            "nfe": 43,
            "pdf": 0,
            "valor": 50.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "cd9555bf-b72a-4054-bf7d-c1a36c4e948c",
            "mes": "10/2022",
            "total": 47,
            "nfe": 47,
            "pdf": 0,
            "valor": 50.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "d720a3d8-92c0-465c-a7b8-f1bb21b11ea7",
            "mes": "10/2022",
            "total": 68,
            "nfe": 68,
            "pdf": 0,
            "valor": 50.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "d713c3a6-e2e7-4a7e-b390-3c071d716eb3",
            "mes": "10/2022",
            "total": 78,
            "nfe": 78,
            "pdf": 0,
            "valor": 50.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "880b4281-e626-4164-9f9a-4356cdfc81c4",
            "mes": "10/2022",
            "total": 167,
            "nfe": 167,
            "pdf": 0,
            "valor": 85.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "0289c151-6547-4ec6-a2e5-e32575bdd3bf",
            "mes": "10/2022",
            "total": 106,
            "nfe": 106,
            "pdf": 0,
            "valor": 85.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "53d265e9-5096-4733-b2e8-722b7a05d537",
            "mes": "10/2022",
            "total": 119,
            "nfe": 119,
            "pdf": 0,
            "valor": 85.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "4e32ffe8-b03c-4c09-8a4d-fc86628f37a9",
            "mes": "10/2022",
            "total": 121,
            "nfe": 121,
            "pdf": 0,
            "valor": 85.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "75983ee7-ebe3-4003-87e0-781e5584d92a",
            "mes": "10/2022",
            "total": 128,
            "nfe": 128,
            "pdf": 0,
            "valor": 85.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "a89d9915-ed22-419f-b0eb-f30f16c0e54a",
            "mes": "10/2022",
            "total": 302,
            "nfe": 134,
            "pdf": 168,
            "valor": 180.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "75341a73-52e5-4063-97fb-794983363816",
            "mes": "10/2022",
            "total": 191,
            "nfe": 191,
            "pdf": 0,
            "valor": 85.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "1cc58174-37a9-4ddf-828c-cff25dace795",
            "mes": "10/2022",
            "total": 151,
            "nfe": 151,
            "pdf": 0,
            "valor": 85.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "505d624f-4a3c-41f2-b972-f47754830a00",
            "mes": "10/2022",
            "total": 157,
            "nfe": 157,
            "pdf": 0,
            "valor": 85.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "24f96e20-dad2-4135-a610-5a86804efc7b",
            "mes": "10/2022",
            "total": 331,
            "nfe": 178,
            "pdf": 153,
            "valor": 180.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "b37c230e-3c53-4a81-b23e-c0956628e00b",
            "mes": "10/2022",
            "total": 704,
            "nfe": 357,
            "pdf": 347,
            "valor": 300.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "0e61780f-3b01-4311-9e70-7320f8b5959b",
            "mes": "10/2022",
            "total": 252,
            "nfe": 252,
            "pdf": 0,
            "valor": 180.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "a9df83fd-2d51-41c7-8719-7dede809ed0c",
            "mes": "10/2022",
            "total": 526,
            "nfe": 304,
            "pdf": 222,
            "valor": 300.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "74ab6970-59c8-4976-b2ec-11deb613cc5f",
            "mes": "10/2022",
            "total": 584,
            "nfe": 437,
            "pdf": 147,
            "valor": 300.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "8c799936-8c62-4588-b151-0fe6f92b8e16",
            "mes": "10/2022",
            "total": 317,
            "nfe": 317,
            "pdf": 0,
            "valor": 180.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "1d630f5d-214b-4119-b9fa-56d38ccf1565",
            "mes": "10/2022",
            "total": 361,
            "nfe": 361,
            "pdf": 0,
            "valor": 180.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "ab4faa6e-a711-40af-bb51-a0f8731684cc",
            "mes": "10/2022",
            "total": 400,
            "nfe": 400,
            "pdf": 0,
            "valor": 180.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "a534f4cb-e004-4902-9d79-20676982dacc",
            "mes": "10/2022",
            "total": 423,
            "nfe": 423,
            "pdf": 0,
            "valor": 180.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "4800cf09-80a5-4836-9262-019cc1f877fa",
            "mes": "10/2022",
            "total": 608,
            "nfe": 608,
            "pdf": 0,
            "valor": 300.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "6736ec43-8d68-422c-a48f-fa367f5375dc",
            "mes": "10/2022",
            "total": 809,
            "nfe": 809,
            "pdf": 0,
            "valor": 300.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "12da1888-1aed-4db3-990e-1969a530e012",
            "mes": "10/2022",
            "total": 1710,
            "nfe": 855,
            "pdf": 855,
            "valor": 475.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "35e4a924-3c92-40d8-a0dc-37314937aec4",
            "mes": "10/2022",
            "total": 1480,
            "nfe": 1480,
            "pdf": 0,
            "valor": 475.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "d6b03f43-742e-4af0-8e3d-9c8d0e9905a6",
            "mes": "10/2022",
            "total": 862,
            "nfe": 862,
            "pdf": 0,
            "valor": 300.00,
            "vencimento": "2022-11-15",
        },
        {
            "contaazul_id": "b5dd4bbc-7b86-406c-b33a-fa16929ceb90",
            "mes": "10/2022",
            "total": 947,
            "nfe": 947,
            "pdf": 0,
            "valor": 300.00,
            "vencimento": "2022-11-15",
        },
    ]
