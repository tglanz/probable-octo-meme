import os

from aws_cdk import (
    aws_ec2 as ec2,
    aws_s3_assets as s3_assets,
    aws_iam as iam
)

from constructs import Construct

def scoped_id(scope: Construct, id: str) -> str:
    # return f"{scope.node.id}/{id}"
    # it seems that cdk scopes the ids by itself
    return id

def create_default_vpc(scope: Construct) -> ec2.Vpc:
    return ec2.Vpc(scope, scoped_id(scope, "vpc"), cidr="10.0.0.0/16")

def create_default_instance(scope: Construct, vpc: ec2.Vpc) -> ec2.Instance:
    security_group = ec2.SecurityGroup(
        scope, scoped_id(scope, "security-group"),
        vpc=vpc,
        allow_all_outbound=True)

    security_group.add_ingress_rule(
        ec2.Peer.any_ipv4(),
        ec2.Port.tcp(80))

    security_group.add_ingress_rule(
        ec2.Peer.any_ipv4(),
        ec2.Port.tcp(22))

    role = iam.Role(scope, scoped_id(scope, "role"),
        assumed_by=iam.ServicePrincipal('ec2.amazonaws.com')
    )

    instance_type = ec2.InstanceType.of(
        ec2.InstanceClass.BURSTABLE3,
        ec2.InstanceSize.MICRO)

    machine_image = ec2.MachineImage.generic_linux({
        # "eu-west-1": "ami-009c3f9c3bfcf00f0",
        "eu-west-1": "ami-00e7df8df28dfa791"
    })

    instance = ec2.Instance(
        scope, scoped_id(scope, "instance"),
        instance_name=scoped_id(scope, "instance"),
        role=role,
        security_group=security_group,
        instance_type=instance_type,
        vpc=vpc,
        vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
        machine_image=machine_image,
        key_name="tglanz-rsa", # TODO: based on the id / parameter
    )

    return instance

class WebServer(Construct):
    def __init__(
            self, scope: Construct, id: str, *, prefix=None,
            vpc=None, instance=None,
            **kwargs):
        super().__init__(scope, id)

        vpc = vpc or create_default_vpc(self)

        instance = instance or create_default_instance(self, vpc)

        # Setup user data

        instance.user_data.add_commands(
            "snap install aws-cli --classic",
        )

        boot_asset = s3_assets.Asset(self, scoped_id(scope, "boot-asset"), 
            path=os.path.abspath("assets/web-server/boot.sh"))

        index_asset = s3_assets.Asset(self, scoped_id(scope, "index-asset"),
            path=os.path.abspath("assets/web-server/index.html"))

        boot_local_path = instance.user_data.add_s3_download_command(
            bucket=boot_asset.bucket,
            bucket_key=boot_asset.s3_object_key
        )

        instance.user_data.add_execute_file_command(
            file_path=boot_local_path
        )

        instance.user_data.add_s3_download_command(
            local_file="/var/www/html/index.html",
            bucket=index_asset.bucket,
            bucket_key=index_asset.s3_object_key
        )

        boot_asset.grant_read(instance.role)
