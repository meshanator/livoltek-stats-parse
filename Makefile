deps:
	python -m pip install --upgrade pip 
	python -m pip install -r requirements.txt

black:
	python -m black .

isort:
	python -m isort .

clean: black isort

run:
	python main.py
