from aws_cdk import (
    Stack,
    aws_eks as eks,
    aws_ec2 as ec2,
)
import yaml
from constructs import Construct

class MinecraftEksCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create VPC
        vpc = ec2.Vpc(self, "MinecraftVPC", max_azs=2)

        # Create EKS cluster
        cluster = eks.Cluster(self, "MinecraftCluster",
            vpc=vpc,
            version=eks.KubernetesVersion.V1_28,
            default_capacity=2
        )

        # Load the manifest from the YAML file
        with open('minecraft_server_manifest.yaml', 'r') as file:
            minecraft_manifest = yaml.safe_load(file)
        
        # Deploy Minecraft server to EKS using the loaded manifest
        cluster.add_manifest("minecraft-server", minecraft_manifest)

        # Load the service manifest from the YAML file
        with open('minecraft_service_manifest.yaml', 'r') as file:
            minecraft_service_manifest = yaml.safe_load(file)

        # Deploy Minecraft service to EKS using the loaded manifest
        cluster.add_manifest("minecraft-service", minecraft_service_manifest)