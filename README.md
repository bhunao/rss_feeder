# RSS Feeder 0.1

## About the Project

## Features
### Articles Feed
The Articles Feed allows you to read articles sourced from [RSS](https://www.rssboard.org/rss-specification) URLs added to the sources database. The news feed displays the latest articles from all sources and lets users subscribe to specific sources and categories, providing a dedicated page for articles from these subscriptions. The news crawler extracts the title, subtitle, and summary from RSS source URLs, ensuring no duplicate articles are created by checking the database before adding new ones. You can create new sources by adding the URL on the sources page, specifying only the URL for the RSS feed source.

## Configuration
All configurations are stored in the `src.core.config.py` file.

## Running the Project
### run docker
`docker compose build`
`docker compose up -d`

### Run Tests
pytest -vv
