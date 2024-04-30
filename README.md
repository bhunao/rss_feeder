# RSS Feeder

## TODO
- get news
- asd
- fix user login
    - keys are in cookies
    - a lot of fields i don't know what they do
- add tests

## Run container
1. build the image
2. run the container with the volume for reload
`docker build -t rss_feeder . && docker run -p 80:80 --volume ./:/app rss_feeder`

## run docker
`docker compose up -d`

## Run Tests
not working
`docker compose run web pytest`
