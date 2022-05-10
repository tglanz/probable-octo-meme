#!/usr/bin/env python3
import os

import aws_cdk as cdk

from stacks.web_server import WebServerStack
from stacks.web_server_v2 import WebServerStackV2
from stacks.eks import EksStack
from stacks.eks_v2 import EksStackV2

app = cdk.App()
WebServerStack(app, "tglanz-web-server-stack")
WebServerStackV2(app, "tglanz-web-server-stack-v2")
EksStack(app, "tglanz-eks-stack")
EksStackV2(app, "tglanz-eks-stack-v2")

app.synth()
