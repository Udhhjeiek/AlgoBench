PYTHON ?= python
PIP ?= $(PYTHON) -m pip

.PHONY: install run test test-engine plots clean

install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) -m streamlit run app.py

test:
	$(PYTHON) -m pytest -q tests

test-engine:
	$(PYTHON) test.py --no-demo

plots:
	@test -n "$(CSV)" || (echo "Usage: make plots CSV=results/file.csv" && exit 1)
	$(PYTHON) visualization/gnuplot_runner.py "$(CSV)"

clean:
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	rm -rf .pytest_cache
