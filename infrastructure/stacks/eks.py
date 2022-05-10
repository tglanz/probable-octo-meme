from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_eks as eks,
    aws_autoscaling as autoscaling,
)
from constructs import Construct

class EksStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        kubernetes_version = eks.KubernetesVersion.V1_21

        vpc = ec2.Vpc(self, "tglanz-simple-cluster-vpc",
            cidr="10.0.0.0/16"
        )

        worker_role = iam.Role(self, "tglanz-simple-cluster-worker-role",
            assumed_by=iam.ServicePrincipal('ec2.amazonaws.com')
        )

        worker_instance_type = ec2.InstanceType.of(
            ec2.InstanceClass.BURSTABLE3,
            ec2.InstanceSize.MEDIUM,
        )

        worker_machine_image = eks.EksOptimizedImage(
            kubernetes_version="1.21",
            node_type=eks.NodeType.STANDARD,
        )


        cluster = eks.Cluster(self, "tglanz-simple-cluster",
            vpc=vpc,
            default_capacity=0,
            version=kubernetes_version,
        )

        asg = autoscaling.AutoScalingGroup(self, "tglanz-simple-cluster-auto-scaling-group",
            vpc=vpc,
            role=worker_role,
            min_capacity=1,
            max_capacity=10,
            instance_type=worker_instance_type,
            machine_image=worker_machine_image,
            update_policy=autoscaling.UpdatePolicy.rolling_update()
        )

        cluster.connect_auto_scaling_group_capacity(asg)

