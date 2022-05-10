from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_eks as eks,
    aws_autoscaling as autoscaling,
)

from constructs import Construct
from custom_constructs.eks_cluster import EksCluster

class EksStackV2(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        EksCluster(self, "eks-cluster")
