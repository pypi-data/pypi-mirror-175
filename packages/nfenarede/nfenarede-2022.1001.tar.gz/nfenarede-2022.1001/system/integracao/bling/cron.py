"""Integração - Bling - Handler."""

from src.bling import Bling


# ------------------------------------------------------------------------------------------------------------
def handler(event: dict, context: dict) -> None:
    """Busca e incluí no G3 os pedidos que estão no Bling.

    Como a Bling não faz o envio de Webhook para pedidos que são gerados via Marketplaces,
    temos que ir buscar os dados diretamente via API a cada período.

    Args:
        event (dict): Dados enviados para do evento, montado pelo Lambda.
        context (dict): Dados sobre o contexto da função, informação sobre a execução.
    """
    integradora = Bling("e282bc3f61e72e47618f9448ba6754f92f647db9a8032fc79478f0f11ccedddace65fe33", 230, 200)
    integradora.bling_importar_pedidos()
