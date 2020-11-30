.DEFAULT_GOAL: help

all: help
.PHONY: all

help:
	@echo "run ./main"
.PHONY: help

clean:
	@echo "removing all log files"
	rm -rf *.log
.PHONY: clean
