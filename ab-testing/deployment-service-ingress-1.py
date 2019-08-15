from kubernetes import client, config

# Fetching and loading Kubernetes Information
config.load_kube_config()

extension = client.ExtensionsV1beta1Api()

# Container
container = client.V1Container(
    name="canary",
    image="registry.lti-aiq.in:443/mosaic-ai-logistics/mosaic-ai-templates-ga:Canary-Dep-1",
    image_pull_policy="Never",
    env=[client.V1EnvVar(name="VERSION", value="v1.0.0")],
)
# Template
template = client.V1PodTemplateSpec(
    metadata=client.V1ObjectMeta(labels={"app": "canary", "version": "v1.0.0"}),
    spec=client.V1PodSpec(containers=[container]))

# Spec
spec = client.ExtensionsV1beta1DeploymentSpec(
    replicas=1,
    selector=client.V1LabelSelector(match_labels={"app": "canary", "version": "v1.0.0"}),
    template=template)

# Deployment
deployment = client.ExtensionsV1beta1Deployment(
    api_version="extensions/v1beta1",
    kind="Deployment",
    metadata=client.V1ObjectMeta(name="dep1", labels={"app": "canary"}),
    spec=spec)

# Creation of the Deployment in specified namespace
extension.create_namespaced_deployment(namespace="ratanb", body=deployment)

extension_svc = client.CoreV1Api()

body = client.V1Service(
    api_version="v1",
    kind="Service",
    metadata=client.V1ObjectMeta(
        name="dep1-service", labels={"app": "canary"}
    ),
    spec=client.V1ServiceSpec(
        selector={"app": "canary", "version": "v1.0.0"},
        ports=[client.V1ServicePort(
            port=5000,
            target_port=5000
        )]
    )
)
extension_svc.create_namespaced_service(namespace="ratanb", body=body)

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
                        service_name="dep1-service")

                )]
            )
        )
        ]
    )
)

extension_v1_beta1.create_namespaced_ingress(
    namespace="ratanb",
    body=body
)