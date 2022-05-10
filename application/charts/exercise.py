from select import select
import cdk8s
from constructs import Construct
from cdk8s import Chart

from imports import k8s

class ExerciseChart(Chart):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        label = {
            "app": "tglanz-exercise"
        }

        # Create the application pod (running the containers)

        application_pod_spec = k8s.PodSpec(
            containers=[
                k8s.Container(
                    name="tglanz-exercise-container",
                    image="epsagon/hello-python:latest",
                    ports=[
                        k8s.ContainerPort(container_port=5000)
                    ],
                    env=[
                        k8s.EnvVar(name="EPSAGON_TOKEN", value="5d919629-8bc1-46af-9130-841c664b32ac"),
                        k8s.EnvVar(name="EPSAGON_APP_NAME", value="Kubernetes Exercise"),
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
            replicas=1,
            selector=k8s.LabelSelector(match_labels=label),
            template=application_pod_template_spec
        )

        deployment = k8s.KubeDeployment(self, 'tglanz-test-deployment',
            spec=deployment_spec,
        )

        # Create a service the provide reliable access to the deployment

        service_spec = k8s.ServiceSpec(
            type='LoadBalancer',
            ports=[
                k8s.ServicePort(
                    port=80, # exposed port
                    target_port=k8s.IntOrString.from_number(5000)
                )
            ],
            selector=label
        )

        service = k8s.KubeService(self, "tglanz-exercise-service",
            spec=service_spec,
            metadata={
                "name": "tglanz-exercise-service"
            },
        )

        ## # Create the relevant namespaces

        ## test_namespace = k8s.KubeNamespace(self, "tglanz-test-namespace",
        ##     metadata={
        ##         "name": "tglanz-test-namespace"
        ##     },
        ## )
