.PHONY: help install test run build clean

help:
	@echo "Guitar Tuner - Build System"
	@echo "============================"
	@echo ""
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Test module imports"
	@echo "  make run        - Run application directly"
	@echo "  make build      - Build standalone executable"
	@echo "  make clean      - Clean build artifacts"
	@echo ""

install:
	@echo "Installing dependencies..."
	pip3 install -r requirements.txt
	@echo "Done!"

test:
	@echo "Testing modules..."
	python3 test_modules.py

run:
	@echo "Starting Guitar Tuner..."
	python3 main.py

build:
	@echo "Building executable..."
	python3 build.py

clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/ dist/ __pycache__/ *.spec
	rm -rf *.pyc .pytest_cache/
	@echo "Clean complete!"
