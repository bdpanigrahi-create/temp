DOCKER_TAG_VERSION_DEVELOPER_TOOLS := 1.25
DOCKER_IMAGE_DEVELOPER_TOOLS := cft/developer-tools
REGISTRY_URL := gcr.io/cloud-foundation-cicd

# Generate documentation
.PHONY: docker_generate_docs
docker_generate_docs:
	docker run --rm -it \
		-e ENABLE_BPMETADATA=1 \
		-v $(CURDIR):/workspace \
		$(REGISTRY_URL)/${DOCKER_IMAGE_DEVELOPER_TOOLS}:${DOCKER_TAG_VERSION_DEVELOPER_TOOLS} \
		/bin/bash -c 'source /usr/local/bin/task_helper_functions.sh && generate_docs --per-module-requirements'

# Alias for backwards compatibility
.PHONY: generate_docs
generate_docs: docker_generate_docs