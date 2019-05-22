from kubernetes import client, config

# Fetching and loading Kubernetes Information
config.load_kube_config()

extension = client.ExtensionsV1beta1Api()

# Container
container = client.V1Container(
  name="oracle",
  image="ratanboddu/oracle-12c",
  image_pull_policy="IfNotPresent",
  ports=[client.V1ContainerPort(container_port=80)],

  lifecycle=client.V1Lifecycle(
    pre_stop=client.V1Handler(
       _exec=client.V1ExecAction(
           command=[
                    # Commands to be executed in the prestop hook
                    "echo \"Hello World\""
                   ]

              )#closing for V1ExecAction

          )#closing for V1Handler

     )#closing for V1Lifecycle
)

# Template
template = client.V1PodTemplateSpec(
  metadata=client.V1ObjectMeta(labels={"app": "oracle"}),
  spec=client.V1PodSpec(containers=[container]))


# Spec
spec = client.ExtensionsV1beta1DeploymentSpec(
  replicas=1,
  template=template)

#Deployment
deployment = client.ExtensionsV1beta1Deployment(
  api_version="extensions/v1beta1",
  kind="Deployment",
  metadata=client.V1ObjectMeta(name="oracle-deployment"),
  spec=spec)

# Creation of the Deployment in specified namespace
extension.create_namespaced_deployment(namespace="kube-client", body=deployment)
