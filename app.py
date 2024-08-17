#!/usr/bin/env python3
import os

import aws_cdk as cdk

from minecraft_eks_cdk.minecraft_eks_cdk_stack import MinecraftEksCdkStack


app = cdk.App()
MinecraftEksCdkStack(app, "MinecraftEksCdkStack",

    )

app.synth()
