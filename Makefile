setup: install pre-commit

install: 
	@echo "Installing dependencies..."
	poetry install

pre-commit:
	@echo "Setting up pre-commit..."
	poetry run pre-commit install

test:
	@echo "Running unit tests..."
	poetry run pytest

build:
	@echo "Building wheel in dist folder..."
	poetry build

publish:
	@echo "Publishing to pypi"
	poetry publish --build
