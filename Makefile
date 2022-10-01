run:
	py -3.10 main.py
setup: requirements.txt
	pip3 install -r requirements.txt
test:
	py.test tests
clean:
	py -3.10 -Bc "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]"
	py -3.10 -Bc "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]"
