"""CDK Stack - Core NFe na rede (Lambda Layer)."""
from os import path

from aws_cdk import Tags
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_lambda_python_alpha as lambda_python
from constructs import Construct

from .base import CDKBaseStack


# ------------------------------------------------------------------------------------------------------------
class NFenaredeCoreStack(CDKBaseStack):
    """Core NFe na rede.

    Define TUDO que é necessário para o sistema (VPC, Subnets, Security Groups, etc...).
    Também define a Lambda Layer que tem todas as entidades e seus métodos que manipulam os dados (CRUD).
    """

    # --------------------------------------------------------------------------------------------------------
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:  # type: ignore
        """Método construtor."""
        super().__init__(scope, construct_id, **kwargs)

        self.core_lambda = self.core_lambda_layer_def()

    # --------------------------------------------------------------------------------------------------------
    def core_lambda_layer_def(self) -> lambda_python.PythonLayerVersion:
        """Dados da Lambda Layer que poderá ser importado por todos os microserviços.

        Aqui nós definimos um dos pontos mais importantes do sistema: a layer que irá manter
        o código mais importante de todo o sistema: o núcleo (core). O núcleo implementa toda
        a manipulação de dados e contêm todas as regras de negócio, permitindo que todos os
        serviços que herdarem este módulo possam trabalhar da maneira correta e evitando que
        trechos de código se repitam.

        Returns:
            lambda_python.PythonLayerVersion: Classe `lambda_python.PythonLayerVersion` do AWS CDK.
        """
        # Define a pasta com o código que será enviado para o layer
        lambda_dir = path.normpath(path.join(path.abspath(path.dirname(__file__)), "..", "nfenarede_core"))

        # Cria a Layer
        lambda_layer = lambda_python.PythonLayerVersion(
            self,
            f"{self.app_name}-{self.env}-core-lambda-layer",
            entry=lambda_dir,
            description="NFe na rede Core: Núcleo que faz o verdadeiro trabalho de manipulação dos dados",
            compatible_architectures=[_lambda.Architecture.ARM_64],
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9],
        )

        # Tags
        Tags.of(lambda_layer).add("app-aws-service", "Lambda Layer")

        # Salva o ARN do Lambda no SSM
        self.novo_ssm_parameter("lambda-layer-core-arn", lambda_layer.layer_version_arn)
        self.novo_output("lambda-layer-core-arn", lambda_layer.layer_version_arn)

        return lambda_layer


# ------------------------------------------------------------------------------------------------------------
