# flext-tap-oracle - Oracle Singer Tap
PROJECT_NAME := flext-tap-oracle
ifneq ("$(wildcard ../base.mk)", "")
include ../base.mk
else
include base.mk
endif

# === PROJECT-SPECIFIC TARGETS ===
.PHONY: tap-run tap-discover test-unit test-integration build shell

tap-run: ## Run tap with config
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run tap-oracle --config config.json

tap-discover: ## Run discovery mode
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run tap-oracle --config config.json --discover

.DEFAULT_GOAL := help
