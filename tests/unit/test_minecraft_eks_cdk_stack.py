import aws_cdk as core
import aws_cdk.assertions as assertions

from minecraft_eks_cdk.minecraft_eks_cdk_stack import MinecraftEksCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in minecraft_eks_cdk/minecraft_eks_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MinecraftEksCdkStack(app, "minecraft-eks-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
