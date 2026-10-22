import aws_cdk as core
import aws_cdk.assertions as assertions

from minecraft_eks_cdk.minecraft_eks_cdk_stack import MinecraftEksCdkStack


def test_cluster_uses_supported_kubernetes_version():
    app = core.App()
    stack = MinecraftEksCdkStack(app, "minecraft-eks-cdk")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties(
        "Custom::AWSCDK-EKS-Cluster",
        {"Config": assertions.Match.object_like({"version": "1.33"})},
    )


def test_manifests_are_applied_to_the_cluster():
    app = core.App()
    stack = MinecraftEksCdkStack(app, "minecraft-eks-cdk")
    template = assertions.Template.from_stack(stack)

    for name in ("minecraft-server", "minecraft-service"):
        template.has_resource_properties(
            "Custom::AWSCDK-EKS-KubernetesResource",
            {"Manifest": assertions.Match.string_like_regexp(rf'"name":"{name}"')},
        )
