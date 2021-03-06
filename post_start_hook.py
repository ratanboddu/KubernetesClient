from kubernetes import client, config

# Fetching and loading Kubernetes Information
config.load_kube_config()

extension = client.ExtensionsV1beta1Api()

# Container
container = client.V1Container(
  name="hooktest",
  image="nginx:1.7.9",
  image_pull_policy="IfNotPresent",
  ports=[client.V1ContainerPort(container_port=80)],

  lifecycle=client.V1Lifecycle(
    post_start=client.V1Handler(
       _exec=client.V1ExecAction(
           command=[
                 'echo \'Hello World\''
                   ]

              )#closing for V1ExecAction

          )#closing for V1Handler

     )#closing for V1Lifecycle
)

# Template
template = client.V1PodTemplateSpec(
  metadata=client.V1ObjectMeta(labels={"app": "hook-test"}),
  spec=client.V1PodSpec(containers=[container]))


# Spec
spec = client.ExtensionsV1beta1DeploymentSpec(
  replicas=1,
  template=template)

# Deployment
deployment = client.ExtensionsV1beta1Deployment(
  api_version="extensions/v1beta1",
  kind="Deployment",
  metadata=client.V1ObjectMeta(name="hook-test-deployment"),
  spec=spec)

# Creation of the Deployment in specified namespace
# Can specify the namespace that you have created
extension.create_namespaced_deployment(namespace="default", body=deployment)

