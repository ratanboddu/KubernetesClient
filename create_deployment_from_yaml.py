from os import path
import yaml
from kubernetes import client, config, utils

# Fetching and loading Kubernetes Information
config.load_kube_config()

with open(path.join(path.dirname(__file__), "test.yaml")) as f:
    dep = yaml.safe_load(f)
    k8s_beta = client.ExtensionsV1beta1Api()
    resp = k8s_beta.create_namespaced_deployment(
        body=dep, namespace="kube-client")
    print("Deployment created status='%s'" % str(resp.status))


