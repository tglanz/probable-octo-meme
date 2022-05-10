import os

from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_s3_assets as s3_assets,
    aws_iam as iam,
)

from constructs import Construct
from custom_constructs.web_server import WebServer

class WebServerStackV2(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        web_server = WebServer(self, "tglanz-webserver")
