install:
	pip install -r requirements.txt

format:
	isort joladnijo/
	black -l 120 joladnijo/ --skip-string-normalization

flake:
	flake8 joladnijo/ --ignore=E203,W503

black:
	black -l 120 --check joladnijo/ --skip-string-normalization

typing:
	mypy --show-error-codes -p joladnijo

lint: black flake typing

unit:
	echo "todo"

test: lint unit
