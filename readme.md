# AWS Into

__infrastructure__ folder contains the CDK app with stack to deploy the web server (exercice 1) and the eks cluster (exercise 2)

The stacks has a v2 variant which are the same semantically but they utilize the Constructs mehcanism better as suggested.

The CDK application is environment agnostic. An AWS profile needs to be provided when deploying, e.g

    cdk deploy --profile {some-profile}

__application__ folder contains the cdk8s project and kubernetes manifests required for the k8s cluster as part of exercice 2
