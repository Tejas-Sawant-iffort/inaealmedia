# Default target
all: install run

# Install dependencies globally
install:
	pip install --upgrade pip
	pip install -r requirements.txt

# Run the Flask app
run:
	python3 main.py

# Clean caches
clean:
	rm -rf __pycache__