black:
	python -m black .

isort:
	python -m isort .

clean: black isort