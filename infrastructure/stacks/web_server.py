import os

from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_s3_assets as s3_assets,
    aws_iam as iam,
)

from constructs import Construct

class WebServerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2.Vpc(
            self, "tglanz-vpc",
            cidr="10.0.0.0/16")

        webserver_security_group = ec2.SecurityGroup(
            self, "tglanz-webserver-security-group",
            vpc=vpc,
            allow_all_outbound=True)

        webserver_security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(80))

        webserver_security_group.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(22))

        webserver_role = iam.Role(self, "tglanz-webserver-role",
            assumed_by=iam.ServicePrincipal('ec2.amazonaws.com')
        )

        webserver_instance_type = ec2.InstanceType.of(
            ec2.InstanceClass.BURSTABLE3,
            ec2.InstanceSize.MICRO)

        webserver_machine_image = ec2.MachineImage.generic_linux({
            # "eu-west-1": "ami-009c3f9c3bfcf00f0",
            "eu-west-1": "ami-00e7df8df28dfa791"
        })

        webserver_instance = ec2.Instance(
            self, 'tglanz-webserver-instance',
            instance_name="tglanz/development-server",
            role=webserver_role,
            security_group=webserver_security_group,
            instance_type=webserver_instance_type,
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            machine_image=webserver_machine_image,
            key_name="tglanz-rsa",
        )

        # Setup user data

        webserver_instance.user_data.add_commands(
            "snap install aws-cli --classic",
        )

        boot_asset = s3_assets.Asset(self, "tglanz-webserver-boot-asset",
            path=os.path.abspath("assets/web-server/boot.sh"))

        index_asset = s3_assets.Asset(self, "tglanz-webserver-index-asset",
            path=os.path.abspath("assets/web-server/index.html"))

        boot_local_path = webserver_instance.user_data.add_s3_download_command(
            bucket=boot_asset.bucket,
            bucket_key=boot_asset.s3_object_key
        )

        webserver_instance.user_data.add_execute_file_command(
            file_path=boot_local_path
        )

        webserver_instance.user_data.add_s3_download_command(
            local_file="/var/www/html/index.html",
            bucket=index_asset.bucket,
            bucket_key=index_asset.s3_object_key
        )

        boot_asset.grant_read(webserver_instance.role)
