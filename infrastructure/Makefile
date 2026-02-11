VENV_PATH := venv/$(shell uname -s)
SOURCES := $(shell echo src/*.py)
TARGETS := $(patsubst src/%.py,templates/%.json,$(SOURCES))

all: clean $(TARGETS)

.PHONY: clean
clean:
	rm -rf $(TARGETS)

.PHONY: cleanvenv
cleanvenv:
	rm -rf venv

templates/%.json: src/%.py $(VENV_PATH)/infra
	$(VENV_PATH)/infra/bin/python3 $< > $@

$(VENV_PATH)/infra: requirements.txt
	python3 -m venv $@
	$@/bin/pip3 install --upgrade pip setuptools wheel
	$@/bin/pip3 install -r requirements.txt
