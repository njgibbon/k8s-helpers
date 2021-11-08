# Useful Prometheus Queries
```
rate(container_cpu_usage_seconds_total{pod=~".*",namespace="test",pod!="",container!="POD",container!=""}[5m])
container_memory_working_set_bytes{pod=~".*",namespace="test",pod!="",container!="POD",container!=""}
```
