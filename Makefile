run:
	python main.py
setup: requirements.txt
	pip install -r requirements.txt
test:
	py.tests tests
clean:
	python-Bc "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
	python -Bc "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"
