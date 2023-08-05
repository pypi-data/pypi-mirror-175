"""CDK Stack - Base com métodos utilizados em todas stacks."""
import simplejson as json  # type: ignore
from aws_cdk import CfnOutput
from aws_cdk import Stack
from aws_cdk import aws_apigateway as apigw
from aws_cdk import aws_apigatewayv2_alpha as apigwv2
from aws_cdk import aws_certificatemanager as cm
from aws_cdk import aws_logs as logs
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_ssm as ssm
from aws_cdk.aws_apigateway import MethodLoggingLevel
from constructs import Construct


# ------------------------------------------------------------------------------------------------------------
class CDKBaseStack(Stack):
    """Classe para criação de novas Stacks do CDK com métodos úteis utilizados na definição de serviços."""

    DOMAIN_NAME = "nfenarede.com.br"
    STAGE_DEV = "dev"
    STAGE_TEST = "test"
    STAGE_STAGING = "staging"
    STAGE_PRODUCTION = "prod"

    # --------------------------------------------------------------------------------------------------------
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:  # type: ignore
        """Método construtor."""
        # Retira os kwargs que não são usados pelo CDK Stack
        self.infra = kwargs.pop("infra", None)
        self.nfe_core = kwargs.pop("nfe_core", None)

        super().__init__(scope, construct_id, **kwargs)

        self.app_name = "NFenarede"
        self.env = self.node.try_get_context("stage")

    # --------------------------------------------------------------------------------------------------------
    def criar_api(self, nome_api: str, descricao: str) -> apigw.RestApi:
        """Função auxiliar para criação de API Gateway v1 (REST).

        Para poder criar endpoints para as funções Lambdas, é necessário configurar o serviço
        do API Gateway. Aqui já abstraímos o máximo de propriedades do recurso, facilitando
        a criação de novas APIs REST.

        Args:
            nome_api (str): Nome da API.
            descricao (str): Descrição completa do uso da API.

        Returns:
            apigw.RestApi: Classe `apigw.RestApi` do AWS CDK.
        """
        log_group_name = f"/aws/api-gateway/{self.app_name}-{self.env}-{nome_api}"
        log_group = logs.LogGroup(
            self,
            f"{self.app_name}-{self.env}-{nome_api}-apilog",
            log_group_name=log_group_name,
        )
        log_level = MethodLoggingLevel.INFO if self.env != self.STAGE_PRODUCTION else MethodLoggingLevel.ERROR

        return apigw.RestApi(
            self,
            f"{self.app_name}-{self.env}-{nome_api}-restapi",
            description=descricao,
            endpoint_types=[apigw.EndpointType.REGIONAL],
            deploy_options=apigw.StageOptions(
                stage_name=self.env,
                logging_level=log_level,
                data_trace_enabled=True if self.env != self.STAGE_PRODUCTION else False,
                metrics_enabled=True if self.env != self.STAGE_PRODUCTION else False,
                access_log_destination=apigw.LogGroupLogDestination(log_group),
                access_log_format=apigw.AccessLogFormat.custom(
                    json.dumps(
                        {
                            "requestId": apigw.AccessLogField.context_request_id(),
                            "source_ip": apigw.AccessLogField.context_identity_source_ip(),
                            "user": apigw.AccessLogField.context_identity_user(),
                            "caller": apigw.AccessLogField.context_identity_caller(),
                            "requestTime": apigw.AccessLogField.context_request_time(),
                            "httpMethod": apigw.AccessLogField.context_http_method(),
                            "resourcePath": apigw.AccessLogField.context_resource_path(),
                            "status": apigw.AccessLogField.context_status(),
                            "protocol": apigw.AccessLogField.context_protocol(),
                            "responseLength": apigw.AccessLogField.context_response_length(),
                            "error": apigw.AccessLogField.context_error_message(),
                        }
                    )
                ),
            ),
        )

    # --------------------------------------------------------------------------------------------------------
    def criar_api_v2(self, nome: str, descricao: str, subdominio: str) -> apigwv2.HttpApi:
        """Função auxiliar para criação de API Gateway v2 (HTTP).

        Para poder criar endpoints para as funções Lambdas, é necessário configurar o serviço
        do API Gateway. Aqui já abstraímos o máximo de propriedades do recurso, facilitando
        a criação de novas APIs HTTP.

        Args:
            nome (str): Nome da API.
            descricao (str): Descrição completa do uso da API.
            subdominio (str): Subdomínio que será associado à API.

        Returns:
            apigwv2.HttpApi: Classe `apigwv2.HttpApi` do AWS CDK.
        """
        route = route53.HostedZone.from_hosted_zone_id(
            self,
            f"{self.app_name}-{self.env}-route53-hostedzone",
            "Z06083552X93J7ZCOD88E",
        )

        certificate = cm.Certificate(
            self,
            f"{self.app_name}-{self.env}-certificate",
            domain_name=self.gerar_subdominio("*"),
            validation=cm.CertificateValidation.from_dns(route),
        )

        dominio = apigwv2.DomainName(
            self,
            f"{self.app_name}-{self.env}-{nome}-domain-name",
            domain_name=self.gerar_subdominio(subdominio),
            certificate=certificate,
        )

        http_api = apigwv2.HttpApi(
            self,
            f"{self.app_name}-{self.env}-{nome}-httpapi",
            description=descricao,
            default_domain_mapping=apigwv2.DomainMappingOptions(domain_name=dominio),
        )

        return http_api

    # --------------------------------------------------------------------------------------------------------
    def novo_ssm_parameter(self, parameter_name: str, value: str) -> bool:
        """Adiciona um parâmetro no SSM.

        Faz a inclusão de um novo parâmetro no SSM, permitindo que essa variável
        seja acessada por todo o sistema. É um ótimo recurso para guardar
        variáveis de ambientes como: nome de tabelas, endpoints, senhas, etc.

        Args:
            parameter_name (str): Nome do parâmetro em que será armazenado o valor.
            value (str): Valor do parâmetro.

        Returns:
            bool: Verdadeiro ou falso para a criação do elemento
        """
        try:
            ssm.StringParameter(
                self,
                f"{self.app_name}-{self.env}-{parameter_name}",
                parameter_name=f"/{self.app_name}/{self.env}/{parameter_name}".lower(),
                string_value=value,
            )
            return True
        except Exception:
            return False

    # --------------------------------------------------------------------------------------------------------
    def obter_ssm_parameter(self, parameter_name: str) -> str:
        """Lê o valor de um parâmetro no SSM.

        Faz a leitura de um valor armazenado em um parâmetro do SSM. O SSM é um
        ótimo recurso para guardar variáveis de ambientes como: nome de tabelas,
        endpoints, senhas, etc.

        Args:
            parameter_name (str): Nome do parâmetro em que será lido o valor.

        Returns:
            str: Valor do parâmetro encontrado.
        """
        parameter_name_search = f"/{self.app_name}/{self.env}/{parameter_name}".lower()
        return ssm.StringParameter.value_from_lookup(self, parameter_name_search)

    # --------------------------------------------------------------------------------------------------------
    def novo_output(self, output_name: str, value: str) -> None:
        """Cria um CfnOutput para essa stack.

        Args:
            output_name (str): Nome da saída
            value (str): Valor de saída
        """
        CfnOutput(
            self,
            f"{self.app_name}-{self.env}-{output_name}-output".lower(),
            value=value,
            export_name=output_name,
        )

    # --------------------------------------------------------------------------------------------------------
    def gerar_subdominio(self, subdominio: str) -> str:
        """Obtem um subdomínio completo e correto.

        Args:
            subdominio (str): Subdomínio desejado

        Returns:
            str: Subdomínio completo e formatado.
        """
        return subdominio + "." + self.DOMAIN_NAME


# ------------------------------------------------------------------------------------------------------------
