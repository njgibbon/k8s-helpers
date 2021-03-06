from kubernetes import client, config

config.load_kube_config()
k8s_core_v1_api_client = client.CoreV1Api()
all_pods = k8s_core_v1_api_client.list_pod_for_all_namespaces(watch=False)

for pod in all_pods.items:
    if pod.spec.host_network:
        print(pod.metadata.name)
