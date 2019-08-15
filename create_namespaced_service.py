from kubernetes import client, config


def main():
    # Fetching and loading Kubernetes Information
    config.load_kube_config()
    # For incluster details
    # config.load_incluster_config()

    extension = client.CoreV1Api()

    body = client.V1Service(
        api_version="v1",
        kind="Service",
        metadata=client.V1ObjectMeta(
            name="service-example"
        ),
        spec=client.V1ServiceSpec(
            selector={"app": "myapp"},
            ports=[client.V1ServicePort(
                port=80,
                target_port=6785
            )]
        )
    )
    extension.create_namespaced_service(namespace="default", body=body)


if __name__ == '__main__':
    main()


