yq e ".metadata.name = \"${APP}\""  - |
yq e ".metadata.labels.name = \"${APP}\""  - |
yq e ".metadata.labels.app = \"${APP}\""  - |
yq e ".spec.selector.matchLabels.app = \"${APP}\""  - |
yq e ".spec.template.metadata.labels.app = \"${APP}\""  - |
yq e ".spec.template.spec.containers[].name = \"${APP}\""  - |
yq e ".spec.template.spec.containers[].image = \"${CONTAINER_IMAGE}\""  - |
yq e ".spec.template.spec.containers[].resources.requests.cpu = \"${CPU}\""  - | 
yq e ".spec.template.spec.containers[].resources.requests.memory = \"${MEM}\""  - |
yq e ".spec.template.spec.containers[].livenessProbe.httpGet.path = \"${PROBE_CONTEXT}\""  - |
yq e ".spec.template.spec.containers[].startupProbe.httpGet.path = \"${PROBE_CONTEXT}\""  -