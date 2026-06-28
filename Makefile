.PHONY: lint test format run

lint:
	ruff check src tests

format:
	ruff format src tests

test:
	pytest tests/ -v    
          --cov=src/us_accidents_etl
          --cov-report=term-missing
          --cov-report=xml

run:
	python main.py 