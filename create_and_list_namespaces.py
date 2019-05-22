from kubernetes import client, config

# Fetching and loading Kubernetes Information
config.load_kube_config()

v1 = client.CoreV1Api()

# Creating namespace
create_namespace = v1.create_namespace(client.V1Namespace(metadata=client.V1ObjectMeta(name="kube-client-test")))

# Listing pods in the namespace that we created
list_namespaces = v1.list_namespaced_pod("kube-client")

# Displaying Pod Information
for i in list_namespaces.items:
    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

