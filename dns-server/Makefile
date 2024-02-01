
VENV = .venv
PYTHON = $(VENV)/bin/python3

build:
ifeq (,$(wildcard $(VENV)))
	@echo "Creating virtualenv..."
	python3 -m venv $(VENV)
endif

run-server: build
	@echo "Activating virtualenv..."
	. $(VENV)/bin/activate
	@echo "Running server..."
	$(PYTHON) src/dns_server.py

clean:
	@echo "Cleaning virtualenv..."
	rm -rf $(VENV)