from kubernetes import client, config

config.load_kube_config()
k8s_core_v1_api_client = client.CoreV1Api()
all_pods = k8s_core_v1_api_client.list_pod_for_all_namespaces(watch=False)

for pod in all_pods.items:
    print(pod.metadata.name)
    print(pod.spec.priority)
    print(pod.spec.priority_class_name)
    print("")
