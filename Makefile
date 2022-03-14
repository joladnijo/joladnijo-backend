flake:
	flake8 joladnijo/ --ignore=E203,W503

lint: flake

unit:
	echo "todo"

test: lint unit
