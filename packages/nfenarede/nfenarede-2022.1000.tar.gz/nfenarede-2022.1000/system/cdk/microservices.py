"""CDK Stack - Microservices (Funções Lambdas)."""
from os import path

from aws_cdk import Duration
from aws_cdk import Tags
from aws_cdk import aws_apigatewayv2_alpha as apigwv2
from aws_cdk import aws_apigatewayv2_integrations_alpha as apigwv2_alpha
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_lambda_python_alpha as lambda_python
from aws_cdk import aws_logs as logs
from constructs import Construct

from .base import CDKBaseStack
from .infra import InfraStack
from .nfenarede_core import NFenaredeCoreStack


# ------------------------------------------------------------------------------------------------------------
class MicroservicesStack(CDKBaseStack):
    """Stack de Microserviços.

    Em uma arquitetura orientada a eventos, os microserviços são essenciais! São eles quem de fato
    executam as tarefas simples e dentro de um fluxo bem definido. Cada microserviço está dentro
    de um contexto que vai ajudar o todo, são as formiguinhas que fazem o trabalho pesado.
    """

    infra: InfraStack
    nfe_core: NFenaredeCoreStack

    # --------------------------------------------------------------------------------------------------------
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:  # type: ignore
        """Método construtor."""
        super().__init__(scope, construct_id, **kwargs)

        self.micro_cobranca_clientes_lambda = self.micro_cobranca_clientes_lambda_def()
        self.micro_cobranca_clientes_api = self.micro_cobranca_clientes_api_def()

    # --------------------------------------------------------------------------------------------------------
    def micro_cobranca_clientes_lambda_def(self) -> lambda_python.PythonFunction:
        """Função Lambda que irá fazer a integração de cobranca com o ContaAzul.

        Para enviar os dados de cobrança para o ContaAzul, todos os meses o sistema irá fazer
        o faturamento e aqui nesta rotina iremos enviar os dados para que o ContaAzul gere
        e envie as cobranças para cada cliente.

        Returns:
            lambda_python.PythonFunction: Classe `lambda_python.PythonFunction` do AWS CDK.
        """
        # Define a pasta com o código que será enviado para o function
        lambda_dir = path.normpath(
            path.join(path.abspath(path.dirname(__file__)), "..", "microservices/cobranca_clientes")
        )

        # Define as variáveis de ambiente que serão utilizadas
        environment = {
            "contaazul_client_id": self.obter_ssm_parameter("contaazul_client_id"),
            "contaazul_client_secret": self.obter_ssm_parameter("contaazul_client_secret"),
            "contaazul_redirect_uri": self.obter_ssm_parameter("contaazul_redirect_uri"),
        }

        # Cria a function
        lambda_function = lambda_python.PythonFunction(
            self,
            f"{self.app_name}-{self.env}-cobranca-clientes-lambda",
            entry=lambda_dir,
            description="Função para fazer a integração de cobranca com o ContaAzul",
            index="index.py",
            handler="handler",
            timeout=Duration.seconds(15),
            architecture=_lambda.Architecture.ARM_64,
            runtime=_lambda.Runtime.PYTHON_3_9,
            vpc=self.infra.vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            log_retention=logs.RetentionDays.ONE_MONTH,
            environment=environment,
        )

        # Tags
        Tags.of(lambda_function).add("app-aws-service", "Lambda Function")

        # Salva o ARN do Lambda no SSM
        self.novo_ssm_parameter("lambda-cobranca-cliente-arn", lambda_function.function_arn)
        self.novo_output("lambda-cobranca-cliente-arn", lambda_function.function_arn)

        return lambda_function

    # --------------------------------------------------------------------------------------------------------
    def micro_cobranca_clientes_api_def(self) -> apigwv2.HttpApi:
        """Cria a API Gateway para poder acessar o microserviço de cobrança.

        Returns:
            apigwv2.HttpApi: Classe `apigwv2.HttpApi` do AWS CDK.
        """
        http_api = self.criar_api_v2(
            "Cobranca-Clientes",
            "HTTP API utilizada para integração de cobranca com o ContaAzul",
            "contaazul",
        )

        integration = apigwv2_alpha.HttpLambdaIntegration(
            f"{self.app_name}-{self.env}-cobranca-clientes-integration",
            self.micro_cobranca_clientes_lambda,  # type: ignore
        )

        http_api.add_routes(path="/auth", methods=[apigwv2.HttpMethod.GET], integration=integration)

        return http_api


# ------------------------------------------------------------------------------------------------------------
