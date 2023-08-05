"""CDK Stack - Integrações (Funções Lambdas)."""
from os import path

from aws_cdk import Duration
from aws_cdk import Tags
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_events as events
from aws_cdk import aws_events_targets as event_targets
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_lambda_python_alpha as lambda_python
from aws_cdk import aws_logs as logs
from constructs import Construct

from .base import CDKBaseStack
from .infra import InfraStack
from .nfenarede_core import NFenaredeCoreStack


# ------------------------------------------------------------------------------------------------------------
class IntegracaoStack(CDKBaseStack):
    """Integração NFe na rede.

    Funções Lambda que irão fazer as integrações com os Marketplaces e os ERPs.
    """

    infra: InfraStack
    nfe_core: NFenaredeCoreStack

    # --------------------------------------------------------------------------------------------------------
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:  # type: ignore
        """Método construtor."""
        super().__init__(scope, construct_id, **kwargs)

        self.integracao_bling_lambda = self.integracao_bling_lambda_def()

    # --------------------------------------------------------------------------------------------------------
    def integracao_bling_lambda_def(self) -> lambda_python.PythonFunction:
        """Função que busca e cadastras os pedidos em aberto no Bling.

        Todos os pedidos que serão gerados pelos Markeplaces, são importados dentro do Bling
        com um status "Em Aberto". Esta função irá buscar a cada intervalo de tempo os dados
        dos pedidos e irá disparar os eventos adiante, dando continuidade no fluxo.

        Returns:
            lambda_python.PythonFunction: Classe `lambda_python.PythonFunction` do AWS CDK.
        """
        # Define a pasta com o código que será enviado para o function
        lambda_dir = path.normpath(path.join(path.abspath(path.dirname(__file__)), "..", "integracao/bling"))

        # Define as variáveis de ambiente que serão utilizadas
        environment = {
            "DYNAMODB_TABLE": self.infra.dbt_integracao.table_name,
            "DAX_CLUSTER_ENDPOINT": self.infra.dax.attr_cluster_discovery_endpoint,
            "MYSQLG3_USER": self.obter_ssm_parameter("mysqlg3_user"),
            "MYSQLG3_PASS": self.obter_ssm_parameter("mysqlg3_pass"),
            "MYSQLG3_HOST": self.obter_ssm_parameter("mysqlg3_host"),
        }

        # Cria a function
        lambda_function = lambda_python.PythonFunction(
            self,
            f"{self.app_name}-{self.env}-integracao-bling-lambda",
            entry=lambda_dir,
            description="Rotina de Integração para o Bling (Importar Pedidos)",
            index="cron.py",
            handler="handler",
            timeout=Duration.minutes(5),
            architecture=_lambda.Architecture.ARM_64,
            runtime=_lambda.Runtime.PYTHON_3_9,
            vpc=self.infra.vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            log_retention=logs.RetentionDays.ONE_MONTH,
            environment=environment,
            layers=[self.infra.mysql_lambda],
        )

        # Cria a evento que irá disparar as importações a cada 5 minutos
        event_rule = events.Rule(
            self,
            f"{self.app_name}-{self.env}-integracao-bling-event-cron",
            description="Evento que dispara a execução do Lambda de Integração com a Bling",
            schedule=events.Schedule.rate(Duration.minutes(5)),
        )

        event_rule.add_target(event_targets.LambdaFunction(lambda_function))  # type: ignore

        # Tags
        Tags.of(lambda_function).add("app-aws-service", "Lambda Function")

        # Salva o ARN do Lambda no SSM
        self.novo_ssm_parameter("lambda-integracao-bling-arn", lambda_function.function_arn)
        self.novo_output("lambda-integracao-bling-arn", lambda_function.function_arn)
        self.novo_ssm_parameter("event-integracao-bling-arn", event_rule.rule_arn)
        self.novo_output("event-integracao-bling-arn", event_rule.rule_arn)

        return lambda_function


# ------------------------------------------------------------------------------------------------------------
