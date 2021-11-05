from kubernetes import client, config

config.load_kube_config()
v1_k8s_api = client.CoreV1Api()
all_pods = v1_k8s_api.list_pod_for_all_namespaces(watch=False)

for pod in all_pods.items:
    if pod.spec.host_network:
        print(pod.metadata.name)
