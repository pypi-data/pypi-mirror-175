"""CDK Stack - Core NFe na rede (Lambda Layer)."""
from os import path

from aws_cdk import Tags
from aws_cdk import aws_certificatemanager as cm
from aws_cdk import aws_dax as dax
from aws_cdk import aws_dynamodb as dynamodb
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_lambda_python_alpha as lambda_python
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_sns as sns
from constructs import Construct

from .base import CDKBaseStack


# ------------------------------------------------------------------------------------------------------------
class InfraStack(CDKBaseStack):
    """Infraestrutura de todo sistema NFe na rede.

    Define TUDO que é necessário para o sistema (VPC, Subnets, Security Groups, etc...).
    """

    # --------------------------------------------------------------------------------------------------------
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:  # type: ignore
        """Método construtor."""
        super().__init__(scope, construct_id, **kwargs)

        self.vpc = self.vpc_def()
        self.external_sg = self.external_sg_def()
        self.internal_sg = self.internal_sg_def()
        self.bastion = self.bastion_def()
        self.dbt_nfenarede = self.dbt_nfenarede_def()
        self.dbt_integracao = self.dbt_integracao_def()
        self.dax = self.dax_def()
        self.mysql_lambda = self.mysql_lambda_layer_def()
        self.route = self.route53_def()
        self.certificate = self.certificate_def()

    # --------------------------------------------------------------------------------------------------------
    def vpc_def(self) -> ec2.Vpc:
        """Dados da VPC criada para esta aplicação.

        Para que todo o sistema trabalhe dentro de uma rede virtual fechada (garantindo maior segurança),
        uma VPC deve ser criada. Neste método está todas as definições necessárias para que a VPC seja
        criada e configurada, além de disponibilizar os dados para as outras stacks que forem criadas.

        Returns:
            ec2.Vpc: Classe `ecs.Vpc` do AWS CDK.
        """
        # Cria a VPC e as Subnets
        vpc = ec2.Vpc(
            self,
            f"{self.app_name}-{self.env}-vpc",
            max_azs=1,
            cidr="192.168.0.0/16",
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name=f"{self.app_name}-{self.env}-vpc-subnet-public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                ),
                ec2.SubnetConfiguration(
                    name=f"{self.app_name}-{self.env}-vpc-subnet-private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                    cidr_mask=24,
                ),
            ],
            nat_gateways=1,
        )

        # Tags
        Tags.of(vpc).add("app-aws-service", "VPC")

        # Flow log
        vpc.add_flow_log(f"{self.app_name}-{self.env}-vpc-flow-log")

        # Salva o ID da VPC no SSM
        self.novo_ssm_parameter("vpc-id", vpc.vpc_id)
        self.novo_output("vpc-id", vpc.vpc_id)

        # Salva os IDs das Subnets Públicas no SSM
        public_subnets = vpc.public_subnets
        for idx, subnet in enumerate(public_subnets):
            self.novo_ssm_parameter(f"vpc-subnet-public-{idx}-id", subnet.subnet_id)
            self.novo_output(f"vpc-subnet-public-{idx}-id", subnet.subnet_id)

        # Salva os IDs das Subnets Privadas no SSM
        private_subnets = vpc.private_subnets
        for idx, subnet in enumerate(private_subnets):
            self.novo_ssm_parameter(f"vpc-subnet-private-{idx}-id", subnet.subnet_id)
            self.novo_output(f"vpc-subnet-private-{idx}-id", subnet.subnet_id)

        return vpc

    # --------------------------------------------------------------------------------------------------------
    def external_sg_def(self) -> ec2.SecurityGroup:
        """Dados do Security Group com acesso externo criada para esta aplicação.

        Para que seja possível acessar os recursos que estão dentro de uma rede interna fechada para
        o acesso externo, utilizamos uma máquina de acesso remoto (bastion) com regras bem definidas
        garantindo uma boa segurança.

        Returns:
            ec2.SecurityGroup: Classe `ec2.SecurityGroup` do AWS CDK.
        """
        # Cria o Security Group
        security_group = ec2.SecurityGroup(
            self,
            f"{self.app_name}-{self.env}-external-security-group",
            vpc=self.vpc,
        )

        # Tags
        Tags.of(security_group).add("app-aws-service", "EC2 Security Group")

        # Inclui regra para acesso ao DAX
        security_group.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(22), "Acesso SSH do Bastion")

        # Salva o ID do Security Group no SSM
        self.novo_ssm_parameter("vpc-external-sg", security_group.security_group_id)
        self.novo_output("vpc-external-sg", security_group.security_group_id)

        return security_group

    # --------------------------------------------------------------------------------------------------------
    def internal_sg_def(self) -> ec2.SecurityGroup:
        """Dados do Security Group com acesso interno criada para esta aplicação.

        Pensando na segurança, devemos restringir o acesso aos recursos da melhor maneira possível.
        Uma das formas de restringir o acesso e melhorar nível de segurança é mapear os IPs e portas
        que podem ser acessadas dentro da VPC. Dessa forma, qualquer vulnerabilidade que houver em
        portas desconhecidas ficam fechadas para o acesso. As regras aqui descritas serão utilizadas
        dentro do ambiente privado da VPC.

        Returns:
            ec2.SecurityGroup: Classe `ec2.SecurityGroup` do AWS CDK.
        """
        # Cria o Security Group
        security_group = ec2.SecurityGroup(
            self,
            f"{self.app_name}-{self.env}-internal-security-group",
            vpc=self.vpc,
        )

        # Tags
        Tags.of(security_group).add("app-aws-service", "EC2 Security Group")

        # Inclui regra para acesso ao DAX
        security_group.add_ingress_rule(
            ec2.Peer.ipv4("192.168.0.0/16"),
            ec2.Port.tcp(8111),
            "DAX - Permite o acesso dentro da VPC",
        )

        # Salva o ID do Security Group no SSM
        self.novo_ssm_parameter("vpc-internal-sg", security_group.security_group_id)
        self.novo_output("vpc-internal-sg", security_group.security_group_id)

        return security_group

    # --------------------------------------------------------------------------------------------------------
    def bastion_def(self) -> ec2.BastionHostLinux:
        """Dados do Bastion para acesso aos recursos do Sistema.

        Aqui fica a definição de todos os dados da máquina Bastion. Ela irá permitir o acesso
        aos recursos do Sistema dentro da AWS que estão dentro do ambiente privado. Isso acrescenta
        uma camada de segurança já que o acesso só poderá ser feito por uma chave.

        Returns:
            ec2.BastionHostLinux: Classe `ec2.BastionHostLinux` do AWS CDK.
        """
        bastion_host = ec2.BastionHostLinux(
            self,
            f"{self.app_name}-Bastion-Host",
            vpc=self.vpc,
            security_group=self.internal_sg,
            subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
        )

        # Salva o ID da Instância do Bstion no SSM
        self.novo_ssm_parameter("bastion-instance-id", bastion_host.instance_id)
        self.novo_output("bastion-instance-id", bastion_host.instance_id)

        return bastion_host

    # --------------------------------------------------------------------------------------------------------
    def dbt_nfenarede_def(self) -> dynamodb.Table:
        """Criação da tabela no DynamoDB para o NFe na rede.

        Para esta aplicação nós utilizamos o DynamoDB como banco de dados primário. O DynamoDB oferece
        alta disponibilidade e escalabilidade, que permite que todo o sistema possa crescer sem causar
        grandes problemas no futuro. Apenas uma tabela será criada utilizando o Single-Table Design.

        Returns:
            dynamodb.Table: Classe `dynamodb.Table` do AWS CDK.
        """
        # Cria a tabela no DynamoDB
        dynamodb_table = dynamodb.Table(
            self,
            f"nfenarede-{self.env}",
            table_class=dynamodb.TableClass.STANDARD,
            partition_key=dynamodb.Attribute(name="pk", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="sk", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            stream=dynamodb.StreamViewType.NEW_AND_OLD_IMAGES,
            time_to_live_attribute="ttl",
        )

        # Tags
        Tags.of(dynamodb_table).add("app-aws-service", "DynamoDB Table")

        # Salva o ID da VPC no SSM
        self.novo_ssm_parameter("dbt-nfenarede", dynamodb_table.table_name)
        self.novo_output("dbt-nfenarede", dynamodb_table.table_name)

        return dynamodb_table

    # --------------------------------------------------------------------------------------------------------
    def dbt_integracao_def(self) -> dynamodb.Table:
        """Criação da tabela no DynamoDB para integração de dados com os Marketplaces e ERPs.

        Tabela para armzenamento de dados relaionados às integrações de Marketplaces como Mercado Livre,
        Magalu, Shoppee, B2W, entre outros... Também para integrações com outros ERPs como G3, Bling. etc.

        Returns:
            dynamodb.Table: Classe `dynamodb.Table` do AWS CDK.
        """
        # Cria a tabela no DynamoDB
        dynamodb_table = dynamodb.Table(
            self,
            f"integracao-{self.env}",
            table_class=dynamodb.TableClass.STANDARD,
            partition_key=dynamodb.Attribute(name="pk", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="sk", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            stream=dynamodb.StreamViewType.NEW_IMAGE,
            time_to_live_attribute="ttl",
        )

        # Tags
        Tags.of(dynamodb_table).add("app-aws-service", "DynamoDB Table")
        Tags.of(dynamodb_table).add("app-service", "Integracao", priority=300)

        # Salva o ID da VPC no SSM
        self.novo_ssm_parameter("dbt-integracao", dynamodb_table.table_name)
        self.novo_output("dbt-integracao", dynamodb_table.table_name)

        return dynamodb_table

    # --------------------------------------------------------------------------------------------------------
    def dax_def(self) -> dax.CfnCluster:
        """Dados do cluster DAX criado para esta aplicação.

        Um cluster do DynamoDB Accelerator (DAX) é um conjunto de máquinas que operam em conjunto
        para ler e escrever dados diretamente no DynamoDB. Além de distrubuir o acesso à mais de
        uma máquina (o que aumenta a performance e escalabilidade), o DAX possuí por característica
        principal um excelente serviço de cache totalmente automático gerenciado pela própria AWS.

        Returns:
            dax.CfnCluster: Classe `dax.CfnCluster` do AWS CDK.
        """
        # Recursos necessários para a montagem do cluster
        dax_role = self.obter_dax_iam_role()
        dax_events_topic = self.obter_dax_events_topic()
        dax_subnet_group = self.obter_dax_subnet_group()

        # Cria o cluster DAX
        dax_cluster = dax.CfnCluster(
            self,
            f"{self.app_name}-{self.env}-dax-cluster",
            iam_role_arn=dax_role.role_arn,
            # node_type="dax.t3.small" if self.env.lower() != "prod" else "dax.r5.large",
            # replication_factor=1 if self.env.lower() != "prod" else 3,
            node_type="dax.t3.small",
            replication_factor=1,
            notification_topic_arn=dax_events_topic.topic_arn,
            subnet_group_name=dax_subnet_group.subnet_group_name,
            security_group_ids=[self.internal_sg.security_group_id],
            preferred_maintenance_window="mon:00:00-mon:01:00",
        )

        # Tags
        Tags.of(dax_cluster).add("app-aws-service", "DAX")

        # Dependências
        dax_cluster.add_depends_on(dax_subnet_group)

        # Salva o ARN do Cluster no SSM
        self.novo_ssm_parameter("dax-cluster-arn", dax_cluster.attr_arn)
        self.novo_output("dax-cluster-arn", dax_cluster.attr_arn)

        # Salva o Endpoint do Cluster no SSM
        self.novo_ssm_parameter("dax-cluster-endpoint", dax_cluster.attr_cluster_discovery_endpoint)
        self.novo_output("dax-cluster-endpoint", dax_cluster.attr_cluster_discovery_endpoint)

        # Salva o ARN do Tópico de Eventos do Cluster no SSM
        self.novo_ssm_parameter("dax-cluster-events-topic", dax_events_topic.topic_arn)
        self.novo_output("dax-cluster-events-topic", dax_events_topic.topic_arn)

        return dax_cluster

    # --------------------------------------------------------------------------------------------------------
    def obter_dax_iam_role(self) -> iam.Role:
        """Dados do IAM criado para autorização do uso do DAX no DynamoDB.

        Para que o DAX possa acessar, ler e escrever dados no DynamoDB, é necessário criar
        um usuário interno que tenha as devidas permissões de acesso. Aqui é configurado
        um perfil com todas essas permissões.

        Returns:
            iam.Role: Classe `iam.Role` do AWS CDK.
        """
        # Cria a regra para o IAM
        iam_rule = iam.Role(
            self,
            f"{self.app_name}-{self.env}-dax-to-dynamodb-fullaccess",
            assumed_by=iam.ServicePrincipal("dax.amazonaws.com"),
        )

        # Dá o acesso ao DynamoDB
        dax_policy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=["arn:aws:dynamodb:*"],
            actions=["dynamodb:*"],
        )

        iam_rule.add_to_policy(dax_policy)
        return iam_rule

    # --------------------------------------------------------------------------------------------------------
    def obter_dax_events_topic(self) -> sns.Topic:
        """Dados do tópico de notificação de eventos do Cluster DAX.

        Durante o ciclo de vida do cluster, diversos eventos podem acontecer pelos mais
        diversos motivos!. Todos eles serão disparados para um tópico de notificação que
        poderá ser acompanhado por alguma rotina, caso seja necessário.

        Returns:
            sns.Topic: Classe `sns.Topic` do AWS CDK.
        """
        # Cria o tópico para notificação
        sns_topic = sns.Topic(
            self,
            f"{self.app_name}-{self.env}-dax-events-topic",
        )

        return sns_topic

    # --------------------------------------------------------------------------------------------------------
    def obter_dax_subnet_group(self) -> dax.CfnSubnetGroup:
        """Dados da Subnet que será utilizada pelo Cluster DAX.

        Como o cluster poderá ser composto por uma ou mais máquinas virtuais, elas precisam de
        uma subnet dentro da VPC para ter uma via de acesso entre todos os recursos do sistema.

        Returns:
            dax.CfnSubnetGroup: Classe `dax.CfnSubnetGroup` do AWS CDK.
        """
        # Obtem as subnets privadas
        private_subnets = self.vpc.private_subnets

        # Cria a configuração do CloudFormation com as subnets do Cluster DAX
        dax_subnet_group = dax.CfnSubnetGroup(
            self,
            f"{self.app_name}-{self.env}-dax-subnetgroup",
            subnet_ids=[subnet.subnet_id for subnet in private_subnets],
            description="Subnet group for DAX Cluster",
            subnet_group_name=f"{self.app_name}-{self.env}-dax-subnetgroup",
        )

        return dax_subnet_group

    # --------------------------------------------------------------------------------------------------------
    def mysql_lambda_layer_def(self) -> lambda_python.PythonLayerVersion:
        """Criação do Lambda Layer para o MySQL.

        Um dos grandes problemas que temos para trabalhar com funções lambdas é o seu tamanho
        (em MB). Outro problema é a falta de módulos que trabalhem corretamente com o MySQL no
        Python. Uma forma de tentar contornar isso é disponibilizar um layer apenas com o módulo
        do Mysql separadamente.

        Returns:
            lambda_python.PythonLayerVersion: Classe `lambda_python.PythonLayerVersion` do AWS CDK.
        """
        # Define a pasta com o código que será enviado para o layer
        lambda_dir = path.normpath(path.join(path.abspath(path.dirname(__file__)), "..", "layers/mysql"))

        # Cria a Layer
        lambda_layer = lambda_python.PythonLayerVersion(
            self,
            f"{self.app_name}-{self.env}-mysql-lambda-layer",
            entry=lambda_dir,
            description="Layer MySQL: Layer apenas com o módulo MySQL que é muito pesado...",
            compatible_architectures=[_lambda.Architecture.ARM_64],
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9],
        )

        # Tags
        Tags.of(lambda_layer).add("app-aws-service", "Lambda Layer")

        # Salva o ARN do Lambda no SSM
        self.novo_ssm_parameter("lambda-layer-mysql-arn", lambda_layer.layer_version_arn)
        self.novo_output("lambda-layer-mysql-arn", lambda_layer.layer_version_arn)

        return lambda_layer

    # --------------------------------------------------------------------------------------------------------
    def route53_def(self) -> route53.IHostedZone:
        """Obtem osdados da Route53 para poder gerar o certificado.

        Returns:
            route53.IHostedZone: Classe `route53.IHostedZone` do AWS CDK.
        """
        route = route53.HostedZone.from_hosted_zone_id(
            self,
            f"{self.app_name}-{self.env}-route53-hostedzone",
            "Z06083552X93J7ZCOD88E",
        )

        return route

    # --------------------------------------------------------------------------------------------------------
    def certificate_def(self) -> cm.Certificate:
        """Cria o certificado que será utilizado dentro do sistema para criar subdomínios HTTPS.

        Returns:
            cm.Certificate: Classe `cm.Certificate` do AWS CDK.
        """
        certificate = cm.Certificate(
            self,
            f"{self.app_name}-{self.env}-certificate",
            domain_name=self.gerar_subdominio("*"),
            validation=cm.CertificateValidation.from_dns(self.route),
        )

        # Tags
        Tags.of(certificate).add("app-aws-service", "Certification Manager")

        # Salva o ARN do Lambda no SSM
        self.novo_ssm_parameter("certificate-arn", certificate.certificate_arn)
        self.novo_output("certificate-arn", certificate.certificate_arn)

        return certificate


# ------------------------------------------------------------------------------------------------------------
