deps:
	python -m pip install --upgrade pip -r requirements.txt
black:
	python -m black .

isort:
	python -m isort .

clean: deps black isort