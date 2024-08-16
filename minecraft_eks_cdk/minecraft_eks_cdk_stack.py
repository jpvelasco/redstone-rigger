from aws_cdk import (
    Stack,
    aws_eks as eks,
    aws_ec2 as ec2,
)
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

        # Deploy Minecraft server to EKS
        cluster.add_manifest("minecraft-server", {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {"name": "minecraft-server"},
            "spec": {
                "replicas": 1,
                "selector": {"matchLabels": {"app": "minecraft-server"}},
                "template": {
                    "metadata": {"labels": {"app": "minecraft-server"}},
                    "spec": {
                        "containers": [{
                            "name": "minecraft-server",
                            "image": "itzg/minecraft-server:latest",
                            "ports": [{"containerPort": 25565}],
                            "env": [
                                {"name": "EULA", "value": "TRUE"},
                                {"name": "TYPE", "value": "PAPER"},
                                {"name": "MEMORY", "value": "1G"}
                            ]
                        }]
                    }
                }
            }
        })

        # Create a Kubernetes Service to expose the Minecraft server
        cluster.add_manifest("minecraft-service", {
            "apiVersion": "v1",
            "kind": "Service",
            "metadata": {"name": "minecraft-service"},
            "spec": {
                "selector": {"app": "minecraft-server"},
                "ports": [{"port": 25565, "targetPort": 25565}],
                "type": "LoadBalancer"
            }
        })