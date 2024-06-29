# RSS Feeder

## About the Project

## Features
### Articles Feed

The Articles Feed allows you to read articles sourced from [RSS](https://www.rssboard.org/rss-specification) URLs added to the sources database. The news feed displays the latest articles from all sources and lets users subscribe to specific sources and categories, providing a dedicated page for articles from these subscriptions. The news crawler extracts the title, subtitle, and summary from RSS source URLs, ensuring no duplicate articles are created by checking the database before adding new ones. You can create new sources by adding the URL on the sources page, specifying only the URL for the RSS feed source.

### TODO Features
- add error responses (like in login when password is wrong)
- add structured logging
- add REST design
- ADD migrations (again...)
- add return types to Database class methods 
  - add mypy
- see how to do template blocks to not repeat html code
- make templates only return code block when request has `HX-Request == true`
- add cooldown to refresh source
- fix some dates that are coming empty and code is set to datetime.now()
- add content to page after signup
- pages
  - categories
  - subscriptions


## Configuration

All configurations are stored in the `src.core.config.py` file.

## Running the Project
### run docker
`docker compose build`
`docker compose up -d`

### Run Tests
pytest -vv
