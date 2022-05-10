from select import select
from constructs import Construct
from cdk8s import Chart

from imports import k8s

class FirstChart(Chart):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        label = {
            "app": "tglanz-first"
        }

        # Create the application pod (running the containers)

        application_pod_spec = k8s.PodSpec(
            containers=[
                k8s.Container(
                    name="tglanz-first-container",
                    image="paulbouwer/hello-kubernetes:1.7",
                    ports=[
                        k8s.ContainerPort(container_port=8080)
                    ]
                )
            ],
        )

        application_pod_template_spec = k8s.PodTemplateSpec(
            metadata=k8s.ObjectMeta(labels=label),
            spec=application_pod_spec,
        )

        # Create the workload controller

        deployment_spec = k8s.DeploymentSpec(
            replicas=2,
            selector=k8s.LabelSelector(match_labels=label),
            template=application_pod_template_spec
        )

        deployment = k8s.KubeDeployment(self, 'tglanz-first-deployment',
            spec=deployment_spec
        )

        # Create a service the provide reliable access to the deployment

        service_spec = k8s.ServiceSpec(
            type='LoadBalancer',
            ports=[
                k8s.ServicePort(
                    port=8080, # exposed port
                    target_port=k8s.IntOrString.from_number(8080)
                )
            ],
            selector=label
        )

        service = k8s.KubeService(self, "tglanz-first-service",
            spec=service_spec,
            metadata={
                "name": "tglanz-first-service"
            },
        )
