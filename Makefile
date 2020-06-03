-include .env

SOURCE_DIRECTORIES := project_real_estate scraper

format: 
	poetry run isort -y -rc $(SOURCE_DIRECTORIES)
	poetry run black $(SOURCE_DIRECTORIES)

serve-local:
	DB_URI=$(DB_URI) poetry run python -m project_real_estate.dash_app.app

serve: 
	DB_URI=$(DB_URI) gunicorn --chdir project_real_estate/dash_app/ app:server
