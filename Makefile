-include .env

SOURCE_DIRECTORIES := project_real_estate scraper

format: 
	poetry run isort -y -rc $(SOURCE_DIRECTORIES)
	poetry run black $(SOURCE_DIRECTORIES)

serve-local:
	DB_URI=$(DB_URI) python -m project_real_estate.dash_app.app

serve: 
	gunicorn --chdir project_real_estate/dash_app/ app:server
