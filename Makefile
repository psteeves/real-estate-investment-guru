-include .env

SOURCE_DIRECTORIES := project_real_estate scraper

format: 
	poetry run isort -y -rc $(SOURCE_DIRECTORIES)
	poetry run black $(SOURCE_DIRECTORIES)

serve-local:
	DATABASE_URL=$(DATABASE_URL) poetry run python -m project_real_estate.dash_app.app

serve: 
	DATABASE_URL=$(DATABASE_URL) gunicorn --chdir project_real_estate/dash_app/ app:server

train:
	DATABASE_URL=$(DATABASE_URL) poetry run python -m scripts.train_model -n rent_predictor
