yq e ".metadata.name = \"${APP}\""  - |
yq e ".metadata.labels.name = \"${APP}\""  - |
yq e ".spec.selector.app = \"${APP}\""  - 