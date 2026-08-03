# Private project handlers for flext-tap-oracle.
# Strict extension: only `_custom_<verb>_<what>` handlers and `(pre|post)-<verb>[-<what>]`
# hooks. Public targets, toolchain vars, .DEFAULT_GOAL, includes, and help are
# invalid (base.mk owns those). Invoke via `make run WHAT=<what>`.
.PHONY: _custom_run_tap _custom_run_discover
_custom_run_tap: ## make run WHAT=tap — run tap with config.json
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run tap-oracle --config config.json
_custom_run_discover: ## make run WHAT=discover — tap discovery mode
	$(Q)PYTHONPATH=$(SRC_DIR) $(POETRY) run tap-oracle --config config.json --discover
