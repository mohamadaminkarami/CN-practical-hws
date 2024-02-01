
VENV = .venv
PYTHON = $(VENV)/bin/python3

build:
ifeq (,$(wildcard $(VENV)))
	@echo "Creating virtualenv..."
	python3 -m venv $(VENV)
endif

run: build
	@echo "Activating virtualenv..."
	. $(VENV)/bin/activate
	@echo "running client and server wrapper"
	$(PYTHON) src/main.py

run-lossy-link:
	@echo "Running lossy_link on 8000 and 8080..."
	$ ./lossy_link-linux 127.0.0.1:8000 127.0.0.1:8080
clean:
	@echo "Cleaning virtualenv..."
	rm -rf $(VENV)