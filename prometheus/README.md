# Useful Prometheus Queries
```
rate(container_cpu_usage_seconds_total{pod=~"aws-node.*",container!="POD"}[1m])
rate(container_cpu_usage_seconds_total{namespace="test",pod!="",container!="POD",container!=""}[5m])
container_memory_working_set_bytes{namespace="test",pod!="",container!="POD",container!=""}
```
