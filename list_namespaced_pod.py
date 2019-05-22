from kubernetes import client, config

# Fetching and loading Kubernetes Information
config.load_kube_config()

v1=client.CoreV1Api()

# Listing pods in the specified namespace
list_pod = v1.list_namespaced_pod("kube-client")
for i in list_pod.items:
    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

# For listing pods in all namesapces
# list_pod_all_namespaces = v1.list_pod_for_all_namespaces()


