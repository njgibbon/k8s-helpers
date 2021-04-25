
"""
Find Conainer Resource Requests and Limits for all Pods in a K8s Cluster.
"""
from kubernetes import client, config

config.load_kube_config()
v1_k8s_api = client.CoreV1Api()
all_pods = v1_k8s_api.list_pod_for_all_namespaces(watch=False)
controllers = []

for pod in all_pods.items:
    # Output metadata for the pod
    try:
        controller_name = pod.metadata.owner_references[0].name
        controller_kind = pod.metadata.owner_references[0].kind
        # Only output once per controller object
        # Special case for Node pods
        if controller_name in controllers and controller_kind != "Node":
            continue
        print(controller_name + " - " + pod.metadata.namespace + " - " + controller_kind)
        controllers.append(pod.metadata.owner_references[0].name)
    except Exception as e:
        print(pod.metadata.name + " - " + pod.metadata.namespace + " - Pod")

    # Output resource info for all containers of the pod
    containers = pod.spec.containers
    for container in containers:
        print(container.name + " - " + str(container.resources))
    print("")
