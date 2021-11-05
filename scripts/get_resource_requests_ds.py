"""
Find Resource Requests for all DaemonSets to help with cluster sizing.
"""
import re
from kubernetes import client, config

config.load_kube_config()
v1_k8s_api = client.CoreV1Api()
all_pods = v1_k8s_api.list_pod_for_all_namespaces(watch=False)
controllers = []
total_container_memory_requests = 0
total_container_cpu_requests = 0
ds_count = 0

print("DaemonSet - Resource Request Configuration")
print("-----")
print("Working")
print("-----")

for pod in all_pods.items:
    try:
        controller_name = pod.metadata.owner_references[0].name
        controller_kind = pod.metadata.owner_references[0].kind
        if controller_kind == "DaemonSet":
            if controller_name not in controllers:
                ds_count += 1
                print(pod.metadata.namespace + " - " + controller_name)
                controllers.append(pod.metadata.owner_references[0].name)
            else:
                continue
        else:
            continue

        containers = pod.spec.containers
        for container in containers:
            print(container.name)
            print(str(container.resources))

            container_cpu_request_original = container.resources.requests["cpu"]
            container_memory_request_original = container.resources.requests["memory"]
            container_cpu_request_number = re.sub("[^0-9]", "", container_cpu_request_original)
            container_memory_request_number = re.sub("[^0-9]", "", container_memory_request_original)
            container_cpu_request_int = int(container_cpu_request_number)
            container_memory_request_int = int(container_memory_request_number)

            if container_cpu_request_original == str(container_cpu_request_int):
                container_cpu_request_int = container_cpu_request_int * 1000

            if "Gi" in container_memory_request_original:
                container_memory_request_int = container_memory_request_int * 1000

            total_container_cpu_requests += container_cpu_request_int
            total_container_memory_requests += container_memory_request_int

            print("CPU Request: " + container_cpu_request_original + ", " + str(container_cpu_request_int))
            print("Memory Request: " + container_memory_request_original + ", " + str(container_memory_request_int))
            print("")

    except Exception as e:
        print(str(e))


print("-----")
print("Totals")
print("-----")
print("DaemonSets: " + str(ds_count))
print("CPU Requests: " + str(total_container_cpu_requests) + "m")
print("Memory Requests: " + str(total_container_memory_requests) + "Mi")


# Note tat this has been done roughly and would need to be adjusted depending on how resource values have been set.
# We expect these formats: Memory 100Mi and CPU 100m.
# We have special cases for memory given as Gi and CPU given as Int.
# But nothing further has been added
# https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
