from kubernetes import client, config


def main():
    # Fetching and loading Kubernetes Information
    config.load_kube_config()
    # For incluster details
    # config.load_incluster_config()

    extensions_v1_beta1 = client.ExtensionsV1beta1Api()

    body = client.ExtensionsV1beta1Ingress(
        api_version="networking.k8s.io/v1beta1",
        kind="Ingress",
        metadata=client.V1ObjectMeta(name="ingress-example", annotations={"nginx.ingress.kubernetes.io/rewrite-target": "/"}),
        spec=client.ExtensionsV1beta1IngressSpec(
            rules=[client.ExtensionsV1beta1IngressRule(
                host="abc.xyz.com",
                http=client.ExtensionsV1beta1HTTPIngressRuleValue(
                    paths=list[client.ExtensionsV1beta1HTTPIngressPath(
                        path="/api",
                        backend=client.ExtensionsV1beta1IngressBackend(
                            service_name="ingress",
                            service_port=5000

                        )
                    )]
                )   
            )
            ]
        )
    )

# Can specify a namespace that you have created
    extensions_v1_beta1.create_namespaced_ingress(
        namespace="default",
        body=body
    )


if __name__ == "__main__":
    main()
