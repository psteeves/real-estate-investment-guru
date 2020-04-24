SOURCE_DIRECTORIES := project_real_estate scraper

format: 
	poetry run isort -y -rc $(SOURCE_DIRECTORIES)
	poetry run black $(SOURCE_DIRECTORIES)

serve: 
	gunicorn --chdir project_real_estate/dash_app/ app:server
