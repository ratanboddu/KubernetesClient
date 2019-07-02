from kubernetes import client, config

# Fetching and loading Kubernetes Information
config.load_kube_config()

extension = client.ExtensionsV1beta1Api()

response = extension.delete_namespaced_deployment(
    # Name of the deployment to be deleted
    name="oracle-deployment",
    namespace="kube-client",
    body=client.V1DeleteOptions(
                    propagation_policy='Foreground',
                    grace_period_seconds=5))


