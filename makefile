.DEFAULT_GOAL: help

all: help
.PHONY: all

help:
	@echo "run ./main"
.PHONY: help

clean:
	rm -rf *.log
.PHONY: clean
