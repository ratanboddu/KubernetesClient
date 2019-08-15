from kubernetes import client, config

# Fetching and loading Kubernetes Information
config.load_kube_config()

batch_v1 = client.BatchV1Api()
core_v1 = client.CoreV1Api

# Volume
volume = client.V1Volume(
      name="test-volume",
      empty_dir=client.V1EmptyDirVolumeSource(medium=""))

# Container
container = client.V1Container(
  name="pi",
  image="perl",
  command=[
      "perl",
      "-Mbignum=bpi",
      "-wle",
      "print bpi(2000)"
  ],
  image_pull_policy="IfNotPresent",
  ports=[client.V1ContainerPort(container_port=80)],
  volume_mounts=[client.V1VolumeMount(name=volume.name, mount_path="/kube-example")]
)

# Init-Container
init_container = client.V1Container(
  name="init-container",
  image="alpine",
  image_pull_policy="IfNotPresent",
  volume_mounts=[client.V1VolumeMount(name=volume.name, mount_path="/kube-example")]
)

# Template
template = client.V1PodTemplateSpec(
    metadata=client.V1ObjectMeta(labels={"app": "pi"}),
    spec=client.V1PodSpec(init_containers=[init_container],
                          containers=[container], volumes=[volume], restart_policy="Never")
)

# Spec
spec_pod = client.V1JobSpec(
    ttl_seconds_after_finished=0,
    template=template
)

# job
job = client.V1Job(
    kind="Job",
    metadata=client.V1ObjectMeta(name="pi"),
    spec=spec_pod
)

batch_v1.create_namespaced_job(namespace="default", body=job)

pods = core_v1.list_namespaced_pod(namespace="default")


for i in pods.items:
    if i.metadata.labels["job-name"] == "pi":
        pod_id = i.metadata.name
        core_v1.read_namespaced_pod_log(name=pod_id, namespace="default")



