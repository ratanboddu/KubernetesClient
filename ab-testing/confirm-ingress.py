from kubernetes import client, config

# Fetching and loading Kubernetes Information
config.load_kube_config()

extension_v1_beta1 = client.ExtensionsV1beta1Api()

body = client.V1beta1Ingress(
    api_version="extensions/v1beta1",
    kind="Ingress",
    metadata=client.V1ObjectMeta(name="dep1-ingress", labels={"app": "canary"},
                                 annotations={"kubernetes.io/ingress.class": "nginx"}),
    spec=client.V1beta1IngressSpec(
        rules=[client.V1beta1IngressRule(
            host="canary.k8.lti-mosaic.com",
            http=client.V1beta1HTTPIngressRuleValue(
                paths=[client.V1beta1HTTPIngressPath(
                    backend=client.V1beta1IngressBackend(
                        service_port=5000,
                        service_name="dep2-service")

                )]
            )
        )
        ]
    )
)

extension_v1_beta1.delete_namespaced_deployment(name="dep1", namespace="ratanb")

core_v1 = client.CoreV1Api()
core_v1.delete_namespaced_service(name="dep1-service", namespace="ratanb")

extension_v1_beta1.delete_namespaced_ingress(name="dep2-ingress-canary", namespace="ratanb")
extension_v1_beta1.patch_namespaced_ingress(
    name="dep1-ingress",
    namespace="ratanb",
    body=body
)