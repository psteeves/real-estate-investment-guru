-include .env

SOURCE_DIRECTORIES := project_real_estate scraper

format: 
	poetry run isort -y -rc $(SOURCE_DIRECTORIES)
	poetry run black $(SOURCE_DIRECTORIES)

serve-local:
	DB_URL=$(DB_URL) poetry run python -m project_real_estate.dash_app.app

serve: 
	DB_URL=$(DB_URL) gunicorn --chdir project_real_estate/dash_app/ app:server

train:
	DB_URL=$(DB_URL) poetry run python -m scripts.train_model -n rent_predictor
