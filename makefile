.DEFAULT_GOAL: help

.PHONY: all
all: help

.PHONY: help
help:
	@echo "run ./main"

.PHONY: clean
clean:
	@echo "removing all log files"
	rm -rf logs/*.log
